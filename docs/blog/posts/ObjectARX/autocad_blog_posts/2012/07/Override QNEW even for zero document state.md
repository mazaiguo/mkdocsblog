---
title: "Override QNEW even for zero document state"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - COM Interop
description: "I have the following code to override the QNEW command that is usually started by clicking the "New" button on the Quick Access Toolbar:"
author: Autodesk
---
# Override QNEW even for zero document state

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/override-qnew-even-for-zero-document-state.html

## 文章内容

By Adam Nagy
I have the following code to override the QNEW command that is usually started by clicking the "New" button on the Quick Access Toolbar:
using System;
using System.Windows.Forms;
using Autodesk.AutoCAD.Runtime;
using System.Runtime.InteropServices;
  [assembly: ExtensionApplication(typeof(CommandOverride.Commands))]
[assembly: CommandClass(typeof(CommandOverride.Commands))]
  namespace CommandOverride
{
  public class Commands : IExtensionApplication
  {
    [CommandMethod("QNEW")]
    public void MyQnew()
    {
      MessageBox.Show("MyQnew");
    }
      [DllImport("acad.exe", // "accore.dll" in AutoCAD 2013
      CharSet=CharSet.Unicode,
      CallingConvention = CallingConvention.Cdecl,
      EntryPoint = "ads_queueexpr")]
    private static extern int ads_queueexpr(string filename);
      public void Initialize()
    {
      ads_queueexpr("(command \"_UNDEFINE\" \"QNEW\") ");
    }
      public void Terminate()
    {
    }
  }
}
Unfortunately, it does not work in zero document state. How could I make it work there as well?
Solution
As you've found, in zero document state it's not enough to undefine QNEW command, you actually have to catch its Windows message. You can watch out for WM_COMMAND message using acedRegisterFilterWinMsg(), click the button you are interested in (in our case it's QNEW) then check the WPARAM value of the message. For QNEW it is 0x12, so this is what we need to intercept. If you return 1 from your event filter, then the message will not be passed on to AutoCAD and so you can override the message.
using System;
using System.Windows.Forms;
using Autodesk.AutoCAD.Runtime;
using System.Runtime.InteropServices;
  [assembly: ExtensionApplication(typeof(CommandOverride.Commands))]
[assembly: CommandClass(typeof(CommandOverride.Commands))]
  namespace CommandOverride
{
  public class Commands : IExtensionApplication
  {
    public void Initialize()
    {
      // we assign it to a variable to keep it alive
      windowsHookProc = new WindowsHookProc(this.WindowsHook);
      acedRegisterFilterWinMsg(windowsHookProc);
    }
      public void Terminate()
    {
    }
      [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    public delegate int WindowsHookProc(
      ref System.Windows.Forms.Message msg);
    private static WindowsHookProc windowsHookProc = null;
      [DllImport("acad.exe", // "accore.dll" in AutoCAD 2013
      CharSet = CharSet.Unicode,
      CallingConvention = CallingConvention.Cdecl,
      // You need to check the exact entry point string
      // with e.g. depends.exe
      EntryPoint =
        "?acedRegisterFilterWinMsg@@YAHQ6AHPAUtagMSG@@@Z@Z")]
    private static extern int acedRegisterFilterWinMsg(
      WindowsHookProc callBackFunc);
      private const int WM_COMMAND = 0x0111;
    private const int ID_FILE_QNEW = 0x0012;
    private int WindowsHook(ref System.Windows.Forms.Message msg)
    {
      if (msg.Msg == WM_COMMAND)
      {
        if (msg.WParam == (IntPtr)ID_FILE_QNEW)
        {
          MessageBox.Show("MyQnewHook");
            // 1 = Do not pass it on to AutoCAD
          return 1;
        }
      }
        return 0;
    }
  }
}
If the user types the QNEW command in the command line instead of clicking the "New" button, even then it will be translated into a WM_COMMAND before it gets executed and so you can catch it there as well and prevent it from reaching AutoCAD.

## 评论

**内容**: bidanshi said...
Hey... this is a brilliant bit of code. Thank you for sharing.
I have a couple questions. I'm trying to hi-jack the open command, but there are two instances where the event is escaping me.
1. When the drawing is opened from Windows Explorer.
2. When CAD starts in a zero document state (once a drawing opens we're fine, before that has trouble though).
Any thoughts on intercepting these?
Reply
10/28/2013 at 03:45 PM

---
