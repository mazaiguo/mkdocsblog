---
title: "Transfer Objects to AutoCAD through Windows Azure Queue Storage"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Unicode
description: "My colleague Gopinath Taget posted a post about using Amazon Simple Queues Service (SQS) with AutoCAD a few days ago, in this post, I will demonstr..."
author: Autodesk
---
# Transfer Objects to AutoCAD through Windows Azure Queue Storage

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/transfer-objects-to-autocad-through-windows-azure-queue-storage.html

## 文章内容

By Daniel Du
My colleague Gopinath Taget posted a post about using Amazon Simple Queues Service (SQS) with AutoCAD a few days ago, in this post, I will demonstrate you how to do the same thing with Windows Azure queue storage. Windows Azure Queue storage is a service for storing large numbers of messages that can be accessed from anywhere in the world via authenticated calls using HTTP or HTTPS. To develop with Windows Azure, you need to download and install the Windows Azure SDK for .NET if you have not already done so.
In Windows Azure Queue storage. A message can be a string, and it can be other types of data, an object for instance. In this post I will show you how to pass a class/object through cloud. What I need to do is, pass an object(myCircle) from a stand-alone application to AutoCAD, then draw it in AutoCAD model space. 
Here is the custom class I defined, it is the data contact I need to pass through cloud, it defines the position and radius of the circle.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
  namespace MyDataContract
{
    public class MyCircle
    {
        public double CenterX { get; set; }
        public double CenterY { get; set; }
        public double Radious { get; set; }
          public MyCircle()
        {
          }
          public MyCircle(double x, double y, double r)
        {
            CenterX = x;
            CenterY = y;
            Radious = r;
        }
    }
}
  Now let’s create the sender application. To make it simple, I create one console application as message sender. To use Windows Azure Queue Storage, we need to add reference to Microsoft.WindowsAzure.StorageClient.dll, which can be found in Windows Azure SDK. Since I am trying to transfer an object through cloud, I need to serialize it so that it can be put into a message of Windows Azure Queue Storage. I use JSON serialization, so I also need to add references to System.Web.Extension.dll.
As a start, I’d rather using Windows Azure Simulator for development and test. Please note the Azure Storage Simulator uses SQL Server Express, you need to start up your SQL Express service.
Here is the code snippet of sender application:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
  using Microsoft.WindowsAzure.StorageClient;
using Microsoft.WindowsAzure;
  //Reference System.web.extension.dll
using System.Web.Script.Serialization;
  //My custom data contact
using MyDataContract;
    namespace Sender
{
    class Program
    {
        static void Main(string[] args)
        {
            //development enviroment
              var storageAccount = CloudStorageAccount
                .DevelopmentStorageAccount;
              var queueStorage = storageAccount
                .CreateCloudQueueClient();
              var queue = queueStorage
                .GetQueueReference("helloworldqueue");
            queue.CreateIfNotExist();
              Console.WriteLine("sender is running。。。。");
              while (true)
            {
                Random rand = new Random();
                double x = rand.NextDouble() * 100;
                double y = rand.NextDouble() * 100;
                double r = rand.NextDouble() * 50;
                MyCircle circle = new MyCircle(x, y, r);
                  //Serialize the custom object to JSON
                  JavaScriptSerializer jss =
                           new JavaScriptSerializer();
                string msgJson = jss.Serialize(circle);
                  // put the JSON string to message
                // and put into queue
                  var msg = new CloudQueueMessage(msgJson);
                queue.AddMessage(msg);
                  Thread.Sleep(3000);
            }
          }
    }
  }
  Now let’s work on the receive, an AutoCAD .net plug-in, I create it with AutoCAD.net wizard, which helps me create an AutoCAD.net plug-in project even faster. similarly, I also need to add reference to Microsoft.WindowsAzure.StorageClient.dll to communicate with Windows Azure, and reference to System.Web.Extension.dll, so that I can deserialize the string message to custom object.
  I created a custom command “DoJobFromAzureQueue” in myCommands.cs :
// (C) Copyright 2012 by Autodesk
//
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.EditorInput;
  using Microsoft.WindowsAzure.StorageClient;
using Microsoft.WindowsAzure;
  //Reference System.web.extension.dll
using System.Web.Script.Serialization;
  //My custom data contact
using MyDataContract;
    // This line is not mandatory, but improves loading performances
[assembly: CommandClass(typeof(AutoCAD_Receiver.MyCommands))]
  namespace AutoCAD_Receiver
{
      // This class is instantiated by AutoCAD for each document when
    // a command is called by the user the first time in the context
    // of a given document. In other words, non static data in this class
    // is implicitly per-document!
    public class MyCommands
    {
        [CommandMethod("DoJobFromAzureQueue")]
        public void DoJobFromAzureQueue()
        {
            Document doc = Application.DocumentManager
                .MdiActiveDocument;
            Editor ed = doc.Editor;
              //development enviroment, working with simulator
              var storageAccount = CloudStorageAccount
                .DevelopmentStorageAccount;
                var queueStorage = storageAccount
                .CreateCloudQueueClient();
              var queue = queueStorage
                .GetQueueReference("helloworldqueue");
            queue.CreateIfNotExist();
              ed.WriteMessage("Receiver is running.... \n");
              CloudQueueMessage msg = null;
              do
            {
                msg = queue.GetMessage();
                if (msg != null)
                {
                    string msgStr = msg.AsString;
                    JavaScriptSerializer jss =
                        new JavaScriptSerializer();
                      MyCircle myC =
                       jss.Deserialize<MyCircle>(msgStr);
                      //Handle message, display the
                    // position/radius
                    ed.WriteMessage(string.Format(
                       "Circle received:X:{0},Y:{1},R:{2}\n",
                            myC.CenterX.ToString(),
                            myC.CenterY.ToString(),
                            myC.Radious.ToString()));
                      //draw circle in AutoCAD
                    DrawCircle(myC.CenterX,
                               myC.CenterY, 
                               myC.Radious);
                      queue.DeleteMessage(msg);
                }
              }
            while (msg != null);
        }
          private void DrawCircle(double x, double y, double r)
        {
            Document doc = Application.DocumentManager
                .MdiActiveDocument;
            Database db = doc.Database;
              using (Transaction trans = db.TransactionManager
                                        .StartTransaction())
            {
                BlockTableRecord modelSpace =
                        trans.GetObject(
                            db.CurrentSpaceId,
                            OpenMode.ForWrite)
                        as BlockTableRecord;
                using (Circle ent = new Circle())
                {
                    ent.Center = new Point3d(x, y, 0);
                    ent.Radius = r;
                      modelSpace.AppendEntity(ent);
                    trans.AddNewlyCreatedDBObject(ent, true);
                }
                  trans.Commit();
            }
          }
      }
  }
  OK, we are ready to run it now. Firstly I start the sender console application, it will send a random circle through message to cloud(simulator in this case) every 30 seconds. As I said earlier, the Azure Storage Simulator uses SQL Express, if you connect to the SQL Express with SQL Server 2008 Management Studio, you will see the queue message stored in database.
Then I start AutoCAD, load the plug-in by “netload” command, and run the custom command “DoJobFromAzureQueue”, the message can be retrieve from cloud then draw circle entities in AutoCAD.
  I just use Windows Azure Storage Simulator for development and debugging, once it works well locally, I can deploy it into cloud  environment now. I need to create a Windows Azure Storage account first. This procedure is introduced in here, I copy/paste it as below for your convenience:
To use storage operations, you need a Windows Azure storage account. You can create a storage account by following these steps. (You can also create a storage account using the REST API.)
Log into the Windows Azure Management Portal.
In the navigation pane, click Hosted Services, Storage Accounts & CDN.
At the top of the navigation pane, click Storage Accounts.
On the ribbon, in the Storage group, click New Storage Account.

The Create a New Storage Account dialog box opens.
In Choose a Subscription, select the subscription that the storage account will be used with.
In Enter a URL, type a subdomain name to use in the URI for the storage account. The entry can contain from 3-24 lowercase letters and numbers. This value becomes the host name within the URI that is used to address Blob, Queue, or Table resources for the subscription.
Choose a region or an affinity group in which to locate the storage. If you will be using storage from your Windows Azure application, select the same region where you will deploy your application.
Click OK.
Click the View button in the right-hand column below to display and save the Primary access key for the storage account. You will need this in subsequent steps to access storage.
  Now let’s modify our code to use the cloud. We can parse the connect string to create a cloud storage account as below:
var storageAccount = CloudStorageAccount.Parse(connStr);
The connection string is similar like:
DefaultEndpointsProtocol=https;AccountName=<YourAccountName>;
AccountKey=<YourKey>
In this case, the account name is “mystorageaccount”, the key can be accessed by clicking “view” button above.
So, in sender project and AutoCAD plugin project, substitute
            //development enviroment, working with simulator
              var storageAccount = CloudStorageAccount
                .DevelopmentStorageAccount;
with
            //production enviroment, working with Azure cloud
              string connStr = "DefaultEndpointsProtocol=https;
                AccountName=<YourAccountName>;
                AccountKey=<YourKey>";
            var storageAccount = CloudStorageAccount
                 .Parse(connStr); 
Build and run, congratulations, you are transferring objects through Azure queue storage in cloud! All source code can be downloaded here Download AzureQueue.
Do you have any other ideas to use Windows Azure queue storage? We are always glad to see your comments.

## 评论

**内容**: xsyww said...
Thx, helps a lot.
Reply
05/03/2012 at 11:03 PM

---
**内容**: Daniel Du said...
Thank you for the comment, I am glad to hear that it helps! :-)
Reply
05/09/2012 at 08:49 PM

---
**内容**: jack said...
why we need use azure?
Reply
05/16/2012 at 11:09 PM

---
**内容**: Daniel Du said...
OK, you can also use Amazon if you prefer :)
If you are asking why we need to use cloud, I would say, it depends on your requirement. For example, you may have many clients working on the same drawing from different devices(PC, Pad, Cellphone...), from different places, at different time, a cloud based solution would be suitable for this case. I probably will write another post about the scenarios of cloud latter.
Reply
05/16/2012 at 11:54 PM

---
