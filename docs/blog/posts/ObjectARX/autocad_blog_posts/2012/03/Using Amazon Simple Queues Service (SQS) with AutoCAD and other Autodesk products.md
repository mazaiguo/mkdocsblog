---
title: "Using Amazon Simple Queues Service (SQS) with AutoCAD and other Autodesk products"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Python
description: "Hello and welcome to the first installment in a series of blog posts related to cloud and mobile technologies. More specifically, we will talk abou..."
author: Autodesk
---
# Using Amazon Simple Queues Service (SQS) with AutoCAD and other Autodesk products

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/using-amazon-simple-queues-service-sqs-with-autocad-and-other-autodesk-products.html

## 文章内容

By Gopinath Taget
Hello and welcome to the first installment in a series of blog posts related to cloud and mobile technologies. More specifically, we will talk about various established and evolving cloud and mobile technologies and concepts and how they can be used with Autodesk products and services.
In this blog post I will talk about Amazon Simple Queue Service, Amazon’s persistent, semi-permanent cloud based messaging system. I say semi-permanent because the messages in the queues have a life time associated with them. i.e., they “expire” after a predetermined amount of time.
Using this Amazon SQS system, you will be able to exchange messages between different software applications, no matter where they live: on your local machine, on a remote machine in your network, on a mobile device or on the cloud.
The messages live on the Amazon cloud and are not “tied” to any one application or software. So once a message is posted, the application/software that posted that message can shut down while the message lives on. This makes it very easy for applications to communicate with each other “asynchronously”.
Now  because this is a message “queue”, the messages are treated as FIFO (First In First Out). So, when an application tries to access messages from a queue, the oldest available message needs to be accessed first, before moving on to the next oldest and so on.
Before you proceed to access the Amazon SQS service to create and manage queues programmatically with your application, you will need a Amazon Web Services (AWS) account. I see that AWS is currently offering free membership (for new customers) for a year with certain limitations. This would be a good place to start for new AWS users.
The SQS service itself is very simple to use. AWS provides several SDKs that work with different frameworks, including Java, Python, .NET. I am using the .NET SDK because it is a popular framework with AutoCAD. The AWS .NET SDK can be downloaded and installed from here. Once you have the SDK, you can use the AWS API in your .NET application by referencing in AWSSDK.dll. This .NET reference, provides APIs for accessing and managing all AWS services including Amazon SQS.
The first step is to create an object that will let you access Amazon SQS infrastructure:
AmazonSQS sqs = AWSClientFactory.CreateAmazonSQSClient(<Access Key placeholder>,  <Secret Key placeholder>);
You will have to replace your own access key and secret key with the place holders above. For more information on generating access keys and secret keys, please check here. Note: You will need a valid AWS account to be able to generate the access and secret keys. I will talk about the subtleties of the access key and secret key in a later post
The next step is to create a queue.
//Creating a queue
CreateQueueRequest sqsRequest = new CreateQueueRequest();
  sqsRequest.QueueName = "AcadJobQueue";
CreateQueueResponse createQueueResponse = sqs.CreateQueue(sqsRequest);
  String myQueueUrl;
myQueueUrl = createQueueResponse.CreateQueueResult.QueueUrl;
In the code above, we create a queue and assign a name to it, “AcadJobQueue”. This name uniquely identifies the queue in our account. If two applications tries to create a queue with the same name (in the same AWS account), the first application to create it wins. No exception is thrown in the second application if the queue already exists. It just gets access to the existing queue. The Queue URL, stored in the “myQueryUrl” string is a unique web path that identifies the queue.
Once we have the queue URL, we can manage it. This mainly means, creating and deleting queues and creating and deleting messages in these queues. the AWS .NET SDK comes with a good sample, typically located at path “Program Files\AWS SDK for .NET\Samples\AmazonSQS_Sample”, that shows these different operations. Here is a simple piece of code that shows how to create and post a message to the message queue:
//Sending a message
SendMessageRequest sendMessageRequest = new SendMessageRequest();
sendMessageRequest.QueueUrl = myQueueUrl; //URL from initial queue creation
sendMessageRequest.MessageBody = "This can be any message";
sqs.SendMessage(sendMessageRequest);
A couple of points to note here:
1) A message in a message queue can exist for up to 14 days. Of course you can delete a message before it expires.
2) The actual message in a message body cannot be more than 64 KB of text. Now this does not mean it has to be text. The bottom line is that the body can contain 64 KB of data. This could be binary data that is stored as text.
So how can you use the message queue in AutoCAD? A typical use of the queue would be as a job queue. i.e., one application posts tasks to be performed to the queue while another application can pick up the job if it is free and can work on the job. For instance, a client application running on your machine could post information about a model on which Finite Element Analysis needs to be performed. Then, worker applications typically running on the cloud would pick up this job, perform the Finite Element Analysis, post the result at a pre-determined location and delete the job items from the queue.
AutoCAD and other Autodesk applications could also use the queue to post jobs and execute them. For instance, I created a small WPF application that posts jobs to the “AcadJobQueue” of my AWS account. The jobs in this case are just requests to “Draw line” and “Draw circle”:
  using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Amazon.SQS;
using Amazon;
using Amazon.SQS.Model;
  namespace TestingAwsQueues
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
          private void button1_Click(object sender,
                                   RoutedEventArgs e)
        {
            AmazonSQS sqs =
                AWSClientFactory.CreateAmazonSQSClient(
                <Access Key placeholder>, 
                <Secret Key placeholder>
                 );
              try
            {
                //Creating a queue if it does not exist
                CreateQueueRequest sqsRequest =
                  new CreateQueueRequest();
                sqsRequest.QueueName = "AcadJobQueue";
                CreateQueueResponse createQueueResponse =
                    sqs.CreateQueue(sqsRequest);
                String myQueueUrl;
                myQueueUrl = createQueueResponse.
                             CreateQueueResult.QueueUrl;
                  //post a message to draw a line
                SendMessageRequest sendMessageRequest =
                    new SendMessageRequest();
                sendMessageRequest.QueueUrl =
                    myQueueUrl; 
                sendMessageRequest.MessageBody = "Draw line";
                sqs.SendMessage(sendMessageRequest);
                  //post a message to draw a circle
                sendMessageRequest =
                                  new SendMessageRequest();
                sendMessageRequest.QueueUrl =
                    myQueueUrl;
                sendMessageRequest.MessageBody =
                                              "Draw circle";
                sqs.SendMessage(sendMessageRequest);
              }
            catch (AmazonSQSException ex)
            {
              }
            }
    }
}
  And here is AutoCAD code that reads the queue and processes these messages to draw the lines and circles. once it is done with one message, it deletes that message from the queue:
  static Point3d lnStartPt = new Point3d(10, 10, 0);
static Point3d crCen = new Point3d(5, 15, 0);
  // Modal Command with localized name
[CommandMethod("AWSRelatedCommands", "_dojobs", "dojobs", CommandFlags.Modal)]
public void MyCommand() // This method can have any name
{
    // Get the objects representing the drawing and editor
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      // Get the queue client
    AmazonSQS sqs =
        AWSClientFactory.CreateAmazonSQSClient(
        <Access Key placeholder>, 
        <Secret Key placeholder>
         );
      try
    {
        //Confirming the queue exists
        ListQueuesRequest listQueuesRequest =
            new ListQueuesRequest();
        ListQueuesResponse listQueuesResponse =
            sqs.ListQueues(listQueuesRequest);
          string qURL = "";
          if(listQueuesResponse.IsSetListQueuesResult())
        {
            ListQueuesResult listQueuesResult =
                listQueuesResponse.ListQueuesResult;
            foreach (String queueUrl in
                     listQueuesResult.QueueUrl)
            {
                if(queueUrl.Contains("AcadJobQueue"))
                {
                    qURL = queueUrl;
                    break;
                }
            }
        }
            if(qURL.Length > 0)
        {
            // We know the queue exists
            using (Transaction trans =
                doc.TransactionManager.StartTransaction())
            {
                int numMessages = 0;
                BlockTableRecord btr =
                    (BlockTableRecord)trans.GetObject(
                    db.CurrentSpaceId,
                    OpenMode.ForWrite);
                  // get all the attributes of the queue and
                // find the number of messages in the queue
                GetQueueAttributesRequest req =
                    new GetQueueAttributesRequest();
                List<String> attributeNames =
                    new List<String>();
                attributeNames.Add("All");
                req.AttributeName = attributeNames;
                req.QueueUrl = qURL;
                GetQueueAttributesResponse res =
                    sqs.GetQueueAttributes(req);
                  if(res.IsSetGetQueueAttributesResult())
                {
                    GetQueueAttributesResult attRes=
                        res.GetQueueAttributesResult;
                    numMessages =
                        attRes.ApproximateNumberOfMessages;
                }
                  if(numMessages > 0)
                {
                    do
                    {
                        //Receiving a message
                        ReceiveMessageRequest
                            receiveMessageRequest =
                            new ReceiveMessageRequest();
                        receiveMessageRequest.QueueUrl =
                            qURL;
                        ReceiveMessageResponse
                            receiveMessageResponse =
                            sqs.ReceiveMessage
                               (receiveMessageRequest);
                        if(receiveMessageResponse.
                            IsSetReceiveMessageResult())
                        {
                            ReceiveMessageResult
                                receiveMessageResult =
                                  receiveMessageResponse.
                                  ReceiveMessageResult;
                              foreach (Message message in
                                receiveMessageResult.Message)
                            {
                                // Draw the entities as
                                // per the job requests
                                if(message.IsSetBody())
                                {
                                    if (message.Body.
                                        Equals("Draw line"))
                                    {
                                        Line ln = new Line(
                                            lnStartPt,
                                            lnStartPt +
                                            new Vector3d(
                                                5, 0, 0
                                                )
                                                );
                                        lnStartPt =
                                            lnStartPt +
                                            new Vector3d(
                                                1, 1, 0) * 5;
                                          btr.AppendEntity(ln);
                                        trans.
                                 AddNewlyCreatedDBObject
                                       (ln, true);
                                    }
                                    else if (message.Body.
                                        Equals(
                                          "Draw circle"
                                           ))
                                    {
                                        Circle cir =
                                            new Circle(crCen,
                                            Vector3d.ZAxis,
                                            5);
                                        crCen = crCen + 
                                         new Vector3d
                                         (1, 1, 0) * 5;
                                          btr.AppendEntity(
                                               cir
                                                );
                                        trans.
                                   AddNewlyCreatedDBObject
                                        (cir, true);
                                    }
                                }
                                  // Deleting a message
                                // since we have
                                // already worked on it
                                DeleteMessageRequest
                                deleteRequest
                                = new DeleteMessageRequest();
                                deleteRequest.QueueUrl =
                                                      qURL;
                                String messageRecieptHandle =
                                    message.ReceiptHandle;
                                deleteRequest.ReceiptHandle =
                                    messageRecieptHandle;
                                sqs.DeleteMessage(
                                      deleteRequest);
                              }
                          }
                        // Check again how many
                        // messages remain
                        req = new
                             GetQueueAttributesRequest();
                        // get all the attributes
                        // of the queue
                        req.AttributeName = attributeNames;
                        req.QueueUrl = qURL;
                        res = sqs.GetQueueAttributes(req);
                          if (res.
                             IsSetGetQueueAttributesResult())
                        {
                            GetQueueAttributesResult attRes =
                                res.GetQueueAttributesResult;
                            numMessages =
                            attRes.
                            ApproximateNumberOfMessages;
                        }
                      // continue until all messages are gone
                    } while (numMessages > 0);
                }
                    trans.Commit();
            }
        }
        }
    catch (AmazonSQSException ex)
    {
      }
  }
  I have intentionally not performed a lot of error checking or exception handling in the code above. This was to keep the code snippets as simple as possible.
Coming back to the uses of Amazon SQS with Autodesk products, it does not have to be a job queue. It can have several uses and is only limited by your imagination. For instance:
1) It could be a message board that logs the progress on a project.
2) It could be comments from participants collaborating on a design document.
3) It could be instructions from a manager to his delegates on a project that is ready to start.
4) It could hold small Dxf streams (less than 64 kb) of a Dxf file that describes a small CAD model.
And the list could go on. The bottom line is that Amazon SQS is a simple message exchange service that is easy to use and flexible enough for using any way you want.

## 评论

**内容**: Moynul Islam said...
Best 4g Dumb Phone
Are you looking for the Best 4g Dumb Phone? then check out today’s post on the top 5 Best Dumb Phone for this year. There are many models of dumb phones available in the market. But which is the best option for you? Don’t worry, in this post we listed the Best 5 models of 4g Dumb Phone for you.
https://bestonefind.com/best-4g-dumb-phone/
Reply
05/07/2022 at 03:05 AM

---
