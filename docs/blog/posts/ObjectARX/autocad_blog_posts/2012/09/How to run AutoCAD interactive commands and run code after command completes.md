---
title: "How to run AutoCAD interactive commands and run code after command completes"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
description: "I need to run an AutoCAD command from my .NET command and allow the user be able to interactively input data. After I call this command I need to t..."
author: Autodesk
---
# How to run AutoCAD interactive commands and run code after command completes

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/how-to-run-autocad-interactive-commands-and-run-code-after-command-completes.html

## 文章内容

By Balaji Ramamoorthy
Issue
I need to run an AutoCAD command from my .NET command and allow the user be able to interactively input data. After I call this command I need to take further action. I am using ActiveX and SendCommand. My code runs before the AutoCAD command is completed by the user. Is there a way to cause my code to wait until the command is finished?
Solution
An approach to consider is to place the .NET code that needs to run after the AutoCAD command finishes in a separate .NET command. This command can be called after the AutoCAD command is complete. Here is a VB.NET example that shows this idea. It runs the LINE command and when the command is finished it runs a command named Test2:
Imports Autodesk.AutoCAD.Interop
Imports Autodesk.AutoCAD.Interop.Common
  <Autodesk.AutoCAD.Runtime.CommandMethod("Test1")> _
Public Shared Sub wbtest1()
      Dim oApp As AcadApplication = Autodesk.AutoCAD.ApplicationServices.Application.AcadApplication
    Dim cmdStr As String
      'this will allow for an open ended line command
    ' when the line command is finished the .NET command wbtest2 will run
    cmdStr = "(command ""Line"")(while(>(getvar ""cmdactive"")0)(command pause))(command ""test2"") "
    oApp.ActiveDocument.SendCommand(cmdStr)
      ' this is called before the LINE command is completed
    MsgBox("From Test1")
  End Sub
  <Autodesk.AutoCAD.Runtime.CommandMethod("Test2")> _
Public Shared Sub wbtest2()
    ' this is called after LINE command completes
    MsgBox("From Test2", MsgBoxStyle.Information)
End Sub

## 评论

**内容**: Andrey said...
Hi Balaji.
Are you checked, how this example works?
I have rewrote this sample to C#:
======================

using System;
//Autodesk namespaces ***************
using acad = Autodesk.AutoCAD.ApplicationServices.Application;
using AcApp = Autodesk.AutoCAD.ApplicationServices;
using AcRtm = Autodesk.AutoCAD.Runtime;
//************************************
[assembly: AcRtm.CommandClass(typeof(Ac2013Laboratory.Commands))]
namespace Ac2013Laboratory {
public partial class Commands {
[AcRtm.CommandMethod("Test1")]
public void Test1() {
AcApp.Document doc = acad.DocumentManager.MdiActiveDocument;
String cmdStr = @"(command ""Line"")(while(>(getvar ""cmdactive"")0)(command pause))(command ""test2"") ";
doc.SendStringToExecute(cmdStr, true, false, true);
acad.ShowAlertDialog("From Test1");
}
[AcRtm.CommandMethod("Test2")]
public void Test2() {
acad.ShowAlertDialog("From Test2");
}
}
}

======================
Sorry, but it ain't working correct.
The actions shall be executed in the following order:
1. Created Line.
2. Showed "From Test2" alert.
3. Showed "From Test1" alert.
But actually I receive other (incorrect) result:
1. Showed "From Test1" alert.
2. Created Line.
3. Showed "From Test2" alert.
Regards
Reply
09/17/2012 at 12:00 AM

---
**内容**: Andrey said...
I apologise Balaji, I have incorrect translated Issue by this Article. Then your code works correctly. I misunderstood the task.
Reply
09/17/2012 at 12:17 AM

---
**内容**: Balaji said in reply to Andrey...
Hi Andrey,
Please dont apologise. I am glad you got it working.
Reply
09/17/2012 at 03:48 AM

---
**内容**: Oleg said...
Hi, Balaji,
good point from you again, thanks so much
I'm using often similar on that,
cmdStr = "(command \"_pline\")(while(>(getvar \"cmdactive\")0)(command pause))(command \"_pedit\" \"_L\" \"_Cl\" \"\")(command \"test2\") ";
Regards,
Oleg
Reply
09/18/2012 at 01:17 AM

---
**内容**: Tony Tanzillo said...
If it works or not, sending LISP programs to the command line is not a robust way to solve the problem.
The problem is easily solved by using acedCmd() or the internal managed wrapper for it (the Editor's RunCommand method, which can be invoked via reflection).
acedCmd() is called by the LISP (command) function, so why on Earth would you use that when you can use acedCmd() more directly (either via P/Invoke, or using the Editor's RunCommand method).
Reply
09/22/2012 at 01:18 AM

---
