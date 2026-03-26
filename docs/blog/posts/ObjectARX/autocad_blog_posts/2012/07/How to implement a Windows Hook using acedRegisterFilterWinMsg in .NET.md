---
title: "How to implement a Windows Hook using acedRegisterFilterWinMsg in .NET"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Unicode
description: "It is possible setup a hook for Windows Messages, which is a low level event to capture when the system is performing almost any task, such as mous..."
author: Autodesk
---
# How to implement a Windows Hook using acedRegisterFilterWinMsg in .NET

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-implement-a-windows-hook-using-acedregisterfilterwinmsg-in-net.html

## 文章内容

By Augusto Goncalves
It is possible setup a hook for Windows Messages, which is a low level event to capture when the system is performing almost any task, such as mouse movement or opening a dialog.
Inside AutoCAD there is a special method to do so, which do not interfere with its built-in behavior, but have the same features: acedRegisterFilterWinMsg
This method still implemented only on C++, so we need to use the DllImport attribute, which you might be familiar. For this specific case, it is also required the decorated name of this aced method, which can be obtained using the Dependency Walker tool.
// For AutoCAD 2013 64 bit
// On previous versions, import from acad.exe (instead accore.dll)
[DllImport("accore.dll",
  CharSet = CharSet.Unicode,
  CallingConvention = CallingConvention.Cdecl,
  EntryPoint = "?acedRegisterFilterWinMsg@@YAHQ6AHPEAUtagMSG@@@Z@Z")]
private static extern int acedRegisterFilterWinMsg(
  WindowHookProc callBackFunc);
  // hook message filter callback function
[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
public delegate int WindowHookProc(
  ref System.Windows.Forms.Message msg);
  private static int WindowsHook(
  ref System.Windows.Forms.Message msg)
{
  // check the msg struct for whatever we want,
  // like keys, paint messages etc
  if (msg.Msg == ???)
  {
    // do something
  }
  return 0;
}
  private static WindowHookProc callBackFunc = null;
  [CommandMethod("registerHook")]
public static void CmdRegisterHook()
{
  callBackFunc = new WindowHookProc(WindowsHook);
  acedRegisterFilterWinMsg(callBackFunc);
}

## 评论

**内容**: Kerry Brown said...

The link to Windows Messages is broken.
Reply
07/09/2012 at 01:51 AM

---
**内容**: Madhukar Moogala said in reply to Kerry Brown...
Not any more :-).
Reply
07/09/2012 at 04:05 PM

---
**内容**: Justin Ralston said...
Augusto
As you know in Civil3d alot of the functions are not exposed in the API. I am currently looking for a way to create a catchment object programmically following on from my forum request here
http://forums.autodesk.com/t5/AutoCAD-Civil-3D-Customization/Can-you-create-Catchment-Objects-from-the-API/td-p/3619810

I was thinking that I could use the sendcommand to launch the CreateCatchmentObject which is fine and pass it an object but then the create catchment object grabs the focus and I can not use sendkeys to tab thru the dialog
Would it be possible to hook this window in Civil3d and return focus to my code and step thru the dialog box with sendkey commands. or are some of the functions exposed but not managed if so can you rap them and use them?
Justin Ralston
Reply
09/15/2012 at 02:18 AM

---
**内容**: BJHuffine said...
curious... if WindowsHook is set to return 0 at the end, what happens if 1 or -1 is returned?
Reply
02/04/2014 at 10:02 AM

---
**内容**: Augusto Goncalves said in reply to BJHuffine...
Hi,
Actually this can return the next hook, like suggested at http://support.microsoft.com/kb/318804
Also, there is some more information at http://msdn.microsoft.com/en-us/library/windows/desktop/ms644990%28v=vs.85%29.aspx
Regards,
Augusto Goncalves
Reply
02/07/2014 at 12:07 PM

---
**内容**: Zu600 said...
Can't Find acedRegisterFilterWinMsg Function When In AutoCAD2021？
Reply
04/25/2023 at 06:15 AM

---
