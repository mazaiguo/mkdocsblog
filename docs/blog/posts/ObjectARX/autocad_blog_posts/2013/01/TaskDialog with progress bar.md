---
title: "TaskDialog with progress bar"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I found the ShowProgressBar property of TaskDialog, but it's not clear how I could make use of it. Any samples?"
author: Autodesk
---
# TaskDialog with progress bar

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/taskdialog-with-progress-bar.html

## 文章内容

By Adam Nagy
I found the ShowProgressBar property of TaskDialog, but it's not clear how I could make use of it. Any samples?
Solution
You need to assign a callback function to the TaskDialog that can be called continously so you can do parts of the lengthy process you want to show a progress bar for. Here is a sample that shows how you can do it.
As you can see it from the comments below there are issues with this on 64 bit OS. My colleague Dianne Phillips looked into it and it turned out to be some issue with assigning your own data to the TaskDialog like so:
td.CallbackData = new MyData();
Her modified code circumvents the issue in two ways: either by using a global variable or assigning your data as an IntPtr. Both ways seem to work fine on 64 bit OS as well.
using System;
using Autodesk.Windows;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Windows;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  using System.Threading;
using System.Globalization;
using System.Runtime.InteropServices;
using WinForms = System.Windows.Forms; 
  [assembly: CommandClass(typeof(TaskDialogTest.Commands))]
[assembly: ExtensionApplication(typeof(TaskDialogTest.Module))]
  namespace TaskDialogTest
{
  // to make the AutoCAD managed runtime happy
  public class Module : IExtensionApplication
  {
    public void Initialize()
    {
    }
    public void Terminate()
    {
    }
  }
    public class Commands
  {
    public class MyVarOverride : IDisposable
    {
      object oldValue;
      string varName;
        public MyVarOverride(string name, object value)
      {
        varName = name;
        oldValue = acApp.GetSystemVariable(name);
        acApp.SetSystemVariable(name, value);
      }
        public void Dispose()
      {
        acApp.SetSystemVariable(varName, oldValue);
      }
    }
      public class MyData
    {
      public int counter = 0;
      public bool delay = true;
        // since the callback data can be reused, be sure
      // to reset it before invoking the task dialog
      public void Reset()
      {
        counter = 0;
        delay = true;
      }
    }
      #region HELPER METHODS
      // helper method for processing the callback both in the 
    // data-member case and the callback argument case
    private bool handleCallback(ActiveTaskDialog taskDialog,
                                TaskDialogCallbackArgs args,
                                MyData callbackData)
    {
      // This gets called continuously until we finished completely
      if (args.Notification == TaskDialogNotification.Timer)
      {
        // To make it longer we do some delay in every second call
        if (callbackData.delay)
        {
          System.Threading.Thread.Sleep(1000);
        }
        else
        {
          callbackData.counter += 10;
          taskDialog.SetProgressBarRange(0, 100);
          taskDialog.SetProgressBarPosition(
              callbackData.counter);
            // This is the main action - adding 100 lines 1 by 1
          Database db = HostApplicationServices.WorkingDatabase;
          Transaction tr = db.TransactionManager.TopTransaction;
          BlockTable bt = (BlockTable)tr.GetObject(
            db.BlockTableId, OpenMode.ForRead);
          BlockTableRecord ms = (BlockTableRecord)tr.GetObject(
            bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);
          Line ln = new Line(
            new Point3d(0, callbackData.counter, 0), 
            new Point3d(10, callbackData.counter, 0));
          ms.AppendEntity(ln);
          tr.AddNewlyCreatedDBObject(ln, true);
            // To make it appear on the screen - might be a bit costly
          tr.TransactionManager.QueueForGraphicsFlush();
          acApp.DocumentManager.MdiActiveDocument.Editor.Regen();
            // We are finished
          if (callbackData.counter >= 100)
          {
            // We only have a cancel button, 
            // so this is what we can press
            taskDialog.ClickButton(
              (int)WinForms.DialogResult.Cancel);
            return true;
          }
        }
          callbackData.delay = !callbackData.delay;
      }
      else if (
        args.Notification == TaskDialogNotification.ButtonClicked)
      {
        // we only have a cancel button
        if (args.ButtonId == (int)WinForms.DialogResult.Cancel)
        {
          return false;
        }
      }
        return true;
    }
      private TaskDialog CreateTaskDialog()
    {
      TaskDialog td = new TaskDialog();
      td.WindowTitle = "Adding lines";
      td.ContentText = "This operation adds 10 lines one at a " +
                      "time and might take a bit of time.";
      td.EnableHyperlinks = true;
      td.ExpandedText = "This operation might be lengthy.";
      td.ExpandFooterArea = true;
      td.AllowDialogCancellation = true;
      td.ShowProgressBar = true;
      td.CallbackTimer = true;
      td.CommonButtons = TaskDialogCommonButtons.Cancel;
      return td;
    }
      #endregion
      #region TASK DIALOG USING CALLBACK DATA ARGUMENT
      /////////////////////////////////////////////////////////////////
    // This sample uses a local instance of the callback data. 
    // Since the TaskDialog class needs to convert the callback data
    // to an IntPtr to pass it across the managed-unmanaged divide,
    // be sure to convert it to an IntPtr before passing it off
    // to the TaskDialog instance. 
    //
    // This case requires more code than the member-based sample 
    // below, but is useful when a callback is shared 
    // between multiple task dialogs.
    /////////////////////////////////////////////////////////////////
      // task dialog callback that uses the mpCallbackData argument
    public bool TaskDialogCallback(ActiveTaskDialog taskDialog,
                                    TaskDialogCallbackArgs args,
                                    object mpCallbackData)
    {
      // convert the callback data from an IntPtr to the actual
      // object using GCHandle
      GCHandle callbackDataHandle = 
        GCHandle.FromIntPtr((IntPtr)mpCallbackData);
      MyData callbackData = (MyData)callbackDataHandle.Target;
        // use the helper method to do the actual processing
      return handleCallback(taskDialog, args, callbackData);
    }
      [CommandMethod("ShowTaskDialog")]
    public void ShowTaskDialog()
    {
      Database db = HostApplicationServices.WorkingDatabase;
      using (
        Transaction tr = db.TransactionManager.StartTransaction())
      {
        // create the task dialog and initialize the callback method
        TaskDialog td = CreateTaskDialog();
        td.Callback = new TaskDialogCallback(TaskDialogCallback);
          // create the callback data and convert it to an IntPtr
        // using GCHandle
        MyData cbData = new MyData();
        GCHandle cbDataHandle = GCHandle.Alloc(cbData);
        td.CallbackData = GCHandle.ToIntPtr(cbDataHandle);
          // Just to minimize the "Regenerating model" messages
        using (new MyVarOverride("NOMUTT", 1))
        {
          td.Show(Application.MainWindow.Handle);
        }
          // If the dialog was not cancelled before it finished
        // adding the lines then commit transaction
        if (memberCallbackData.counter >= 100)
          tr.Commit();
          // be sure to clean up the gc handle before returning
        cbDataHandle.Free();
      }
    }
      #endregion
      #region TASK DIALOG USING DATA-MEMBER-BASED CALLBACK DATA
      /////////////////////////////////////////////////////////////////
    // This sample uses a data member for the callback data. 
    // This avoids having to pass the callback data as an IntPtr.
    /////////////////////////////////////////////////////////////////
      // member-based callback data - 
    // used with MemberTaskDialogCallback
    MyData memberCallbackData = new MyData();
      // task dialog callback that uses the callback data member; 
    // does not use mpCallbackData
    public bool TaskDialogCallbackUsingMemberData(
      ActiveTaskDialog taskDialog,
      TaskDialogCallbackArgs args,
      object mpCallbackData)
    {
      // use the helper method to do the actual processing
      return handleCallback(taskDialog, args, memberCallbackData);
    }
      [CommandMethod("ShowTaskDialogWithDataMember")]
    public void ShowTaskDialogWithDataMember()
    {
      Database db = HostApplicationServices.WorkingDatabase;
      using (
        Transaction tr = db.TransactionManager.StartTransaction())
      {
        // create the task dialog and initialize the callback method
        TaskDialog td = CreateTaskDialog();
        td.Callback = 
          new TaskDialogCallback(TaskDialogCallbackUsingMemberData);
          // make sure the callback data is initialized before 
        // invoking the task dialog
        memberCallbackData.Reset();
          // Just to minimize the "Regenerating model" messages
        using (new MyVarOverride("NOMUTT", 1))
        {
          td.Show(Application.MainWindow.Handle);
        }
          // If the dialog was not cancelled before it finished
        // adding the lines then commit transaction
        if (memberCallbackData.counter >= 100)
          tr.Commit();
      }
    }
      #endregion
  }
}

## 评论

**内容**: Fatman13 said...
Somehow I always get "Specified cast is not valid" exception when calling "td.show(...)", does anyone else encounter this problem?
Reply
07/05/2012 at 05:27 PM

---
**内容**: TimStalin said in reply to Fatman13...
I'm getting this too. On x86 it works fine. But for x64 it crashes 2011 and throws an invalid cast 2012 and 2013.
I really hope there is a simple workaround.
Reply
07/19/2012 at 08:31 PM

---
**内容**: PDOTeam said...
Any update to the invalid type cast error?
Reply
10/01/2012 at 10:50 AM

---
**内容**: Adam Nagy said...
Sorry I did not answer before.
On 64 bit OS I could reproduce this behaviour too. It is logged now in our system, but unfortunately I cannot give you a deadline for which it would be sorted out.
In the meantime you could create your own Task Dialog to show the progress on a 64 bit OS.
Reply
10/05/2012 at 10:11 AM

---
**内容**: Vlisp2NET said...
From a .NET novice...
Reading the code above, I am struggling to see how the TaskDialog gets closed when the processing has ended. Would someone please explain how this is achieved programmatically. Whenever I have seen or used a TaskDialog , it is always displayed until the user clicks a button.
I am coming from Visual Lisp & not quite upto speed with .NET.
Steve
Reply
05/01/2013 at 03:34 AM

---
**内容**: Adam Nagy said in reply to Vlisp2NET...
Hi Steve,
Inside the handleCallback function you can see that when the callbackData.Counter reaches 100 then the Cancel button is clicked using the ClickButton function.
Cheers,
Adam
Reply
05/04/2013 at 05:56 AM

---
**内容**: dan said...
i used your code to process some data selected in PromptSelectionResult
i add a variable in my data and pass PromptSelectionResult to it and then processed it. the program works but without progress bar it takes much much less time.
Reply
09/28/2014 at 12:05 AM

---
**内容**: D said...
It is not obvious to me how to use this in a loop. Appreciate any guidance. Thanks.
Reply
11/10/2015 at 06:00 PM

---
**内容**: Balaji said in reply to D...
You may also be interested in this blog post which should work from a for loop :
http://through-the-interface.typepad.com/through_the_interface/2007/05/displaying_a_pr.html
Regards,
Balaji
Reply
11/12/2015 at 10:17 PM

---
**内容**: Balaji said...
Hello,
I do not think it is possible to increment the progress bar position from inside a for loop.
The computations that are in a for loop will require to be moved to the callback attached to the TaskDialog.
When the TaskDialog.Show is called, it is left to the callback to determine when the task is done and to click on the cancel button to close it.
Regards,
Balaji
Reply
11/12/2015 at 10:08 PM

---
