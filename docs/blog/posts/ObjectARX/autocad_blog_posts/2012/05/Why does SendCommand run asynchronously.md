---
title: "Why does SendCommand run asynchronously"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM
  - COM Interop
description: "I'm using the ActiveX API from .NET to run some commands synchronously. According to the AutoCAD ActiveX API Reference if I provide all command par..."
author: Autodesk
---
# Why does SendCommand run asynchronously

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/why-does-sendcommand-run-asynchronously.html

## 文章内容

By Adam Nagy
I'm using the ActiveX API from .NET to run some commands synchronously. According to the AutoCAD ActiveX API Reference if I provide all command parameters, so that no user interaction is required, then SendCommand is synchronous.
Here is a sample that I used to check this:
using System;
using System.Windows.Forms;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Interop;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly: CommandClass(typeof(CsMgdAcad1.AEN1Commands))]
  namespace CsMgdAcad1
{
  public class AEN1Commands
  {
    [CommandMethod("AEN1Cmd1")]
    static public void Cmd1()
    {
      AcadApplication acadApp =
        (AcadApplication)acApp.AcadApplication;
        short newValue = (short)acApp.GetSystemVariable("FILEDIA");
      newValue = (newValue == 1) ? (short)0 : (short)1;
      acadApp.ActiveDocument.SendCommand(
        "_FILEDIA " + newValue + " ");
      short returnedValue =
        (short)acApp.GetSystemVariable("FILEDIA");
      if (newValue != returnedValue)
        MessageBox.Show("SendCommand was asynchronous!");
    }
  }
}
Solution
If SendCommand is synchronous or not also depends on the context in which your command runs. If it is running in Session Context (and you provided all the command parameters) then SendCommand will be synchronous. To achieve this, just add CommandFlags.Session to the CommandMethod attribute.
using System;
using System.Windows.Forms;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Interop;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly: CommandClass(typeof(CsMgdAcad1.AEN1Commands))]
  namespace CsMgdAcad1
{
  public class AEN1Commands
  {
    [CommandMethod("AEN1Cmd1", CommandFlags.Session)]
    static public void Cmd1()
    {
      AcadApplication acadApp =
        (AcadApplication)acApp.AcadApplication;
        short newValue =
        (short)acApp.GetSystemVariable("FILEDIA");
      newValue = (newValue == 1) ? (short)0 : (short)1;
      acadApp.ActiveDocument.SendCommand(
        "_FILEDIA " + newValue + " ");
      short returnedValue =
        (short)acApp.GetSystemVariable("FILEDIA");
      if (newValue != returnedValue)
        MessageBox.Show("SendCommand was asynchronous!");
    }
  }
}
Don't forget that in Session Context you need to lock the document before modifying it using the .NET API. You'll find more information about that in other DevNotes and the ObjectARX Reference help file under Document.LockDocument (or AcApDocManager::lockDocument)

