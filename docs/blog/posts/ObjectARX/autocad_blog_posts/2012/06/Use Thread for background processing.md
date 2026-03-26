---
title: "Use Thread for background processing"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM Interop
  - Database
description: "From inside my command I'm starting a background thread that synchronizes with a database. Once that finishes I'd like to keep using the AutoCAD .N..."
author: Autodesk
---
# Use Thread for background processing

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-thread-for-background-processing.html

## 文章内容

By Adam Nagy
From inside my command I'm starting a background thread that synchronizes with a database. Once that finishes I'd like to keep using the AutoCAD .NET API to do some further modifications in the database. Unfortunately, when I'm calling the AutoCAD API functions from this thread things do not seem to work, e.g. the MdiActiveDocument is null.
Solution
The AutoCAD API's do not support multithreading. You should only call the API functions from the main thread.
If you are in a different thread then you have to marshal the call to the main thread. The simplest way to achieve that is creating a System.Windows.Forms.Control object on the main thread and call its Invoke() function to start the function that is doing the end processing.
Here is a sample to demonstrate this.
using System;
using Autodesk.AutoCAD.Runtime;
using System.Windows.Forms;
using Autodesk.AutoCAD.EditorInput;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
  namespace BackgroundProcess
{
  public class Commands : IExtensionApplication
  {
    static Control syncCtrl;
    public void Initialize()
    {
      // The control created to help with marshaling
      // needs to be created on the main thread
      syncCtrl = new Control();
      syncCtrl.CreateControl();
    }
      public void Terminate()
    {
    }
      void BackgroundProcess()
    {
      // This is to represent the background process
      System.Threading.Thread.Sleep(5000);
        // Now we need to marshall the call to the main thread
      // I don't see how this could ever be false in this context,
      // but I check it anyway
      if (syncCtrl.InvokeRequired)
        syncCtrl.Invoke(
          new FinishedProcessingDelegate(FinishedProcessing));
      else
        FinishedProcessing();
    }
      delegate void FinishedProcessingDelegate();
    void FinishedProcessing()
    {
      // If we want to modify the database, then we need to lock
      // the document since we are in session/application context
      Document doc = acApp.DocumentManager.MdiActiveDocument;
      using (doc.LockDocument())
      {
        using (Transaction tr =
          doc.Database.TransactionManager.StartTransaction())
        {
          BlockTable bt =
            (BlockTable)tr.GetObject(
            doc.Database.BlockTableId, OpenMode.ForRead);
            BlockTableRecord ms = (BlockTableRecord)tr.GetObject(
            bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);
            Line line =
            new Line(new Point3d(0, 0, 0), new Point3d(10, 10, 0));
          ms.AppendEntity(line);
          tr.AddNewlyCreatedDBObject(line, true);
            tr.Commit();
        }
      }
        // Also write a message to the command line
      // Note: using AutoCAD notification bubbles would be
      // a nicer solution :)
      // TrayItem/TrayItemBubbleWindow
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
      ed.WriteMessage("Finished the background process!\n");
    }
      [CommandMethod("ProcessInBackground")]
    public void ProcessBackground()
    {
      // Let's say we got some data from the drawing and
      // now we want to process it in a background thread
      System.Threading.Thread thread =
        new System.Threading.Thread(
          new System.Threading.ThreadStart(BackgroundProcess));
      thread.Start();
        Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
      ed.WriteMessage(
        "Started background processing. " + 
        "You can keep working as usual.\n");
    }
  }
}

## 评论

**内容**: Maxence said...
An alternative to avoid creating a control seems to be SynchronizationContext. There is a nice article here: http://www.codeproject.com/Articles/31971/Understanding-SynchronizationContext-Part-I
Reply
06/26/2012 at 12:22 PM

---
**内容**: Adam Nagy said...
Yes, it does look like a nice alternative to the above solution. Thank you for pointing that out. :)
Reply
06/26/2012 at 02:11 PM

---
**内容**: Daniel Vink said...
Lots of thanks for this post, helped me build an actually user-friendly integrated file synchronisation tool.
The SynchronizationContext turned out to be quite useful because it gives the choice between synchronous and asynchronous calls, but it also creates a new problem: by default, the main thread's SynchronizationContext.Current is null. Creating a Control, much like in the example, solved this problem.
Reply
12/21/2012 at 06:46 AM

---
