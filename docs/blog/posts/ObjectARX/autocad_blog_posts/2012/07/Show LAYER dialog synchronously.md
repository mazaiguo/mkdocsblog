---
title: "Show LAYER dialog synchronously"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Layer
description: "I would like to run the LAYER command from my own command. Unfortunately, it seems that the LAYER dialog only shows once my command is finised. Wou..."
author: Autodesk
---
# Show LAYER dialog synchronously

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/show-layer-dialog-synchronously.html

## 文章内容

By Adam Nagy
I would like to run the LAYER command from my own command. Unfortunately, it seems that the LAYER dialog only shows once my command is finised. Would it be possible to show this dialog during my command and then continue with my command once the dialog is closed?
Solution
First of all, for a few releases now the layer dialog has been modeless. However, it has a setting that enables the old behaviour: LAYERDLGMODE
Also, to start another command synchronously, you would need to P/Invoke acedCmd() from your .NET project.
Since you try to run the LAYER command from inside your command, it starts in command line mode. If you want to force it to show the dialog, then you also need to P/Invoke acedInitDialog(). This has mangled name, which also means that it may be different depending on the OS type (32 bit vs. 64 bit) and the version of AutoCAD, so make sure that you are using the correct mangled name of the function.
You can use dumpbin.exe or depends.exe to get this information from acad.exe. You can find further information about these utilities on the internet.
Here is the .NET project that does what you need in case of AutoCAD 2011 on 32 bit OS:
using System;
using System.Runtime.InteropServices;
  using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.DatabaseServices;
  namespace StartCommand
{
  public class Command
  {
    [DllImport(
      "acad.exe",
      CallingConvention = CallingConvention.Cdecl,
      CharSet = CharSet.Unicode,
      EntryPoint = "acedCmd")]
    public static extern int acedCmd(System.IntPtr resBuf);
      // Mangled entry point may be different in case of
    // different OS (32 bit vs 64 bit) and different AutoCAD versions
      [DllImport(
      "acad.exe",
      CallingConvention = CallingConvention.Cdecl,
      CharSet = CharSet.Unicode,
      EntryPoint = "?acedInitDialog@@YAHH@Z")]
    public static extern bool acedInitDialog(bool useDialog);
      [CommandMethod("StartCommand1")]
    public void StartCommand1()
    {
      // Do something
      // ...
        acApp.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
        "\nCommand Started ...\n"
      );
        // Now show the LAYER dialog
      // First make sure that we use the modal version
        short dlgMode = (short)acApp.GetSystemVariable("LAYERDLGMODE");
      acApp.SetSystemVariable("LAYERDLGMODE", 0);
        // Execute the LAYER command
        using (ResultBuffer rb = new ResultBuffer())
      {
        rb.Add(new TypedValue((int)LispDataType.Text, "_LAYER"));
          // Make sure that not the command line version gets started
          acedInitDialog(true);
          acedCmd(rb.UnmanagedObject);
      }
        // Restore the value
        acApp.SetSystemVariable("LAYERDLGMODE", dlgMode);
        // Continue with our command
        acApp.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
        "\nCommand Continued ...\n"
      );
    }
  }
}

