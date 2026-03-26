---
title: "Dismissing popup dialogs in AutoCAD"
date: 2015-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
description: "Most AutoCAD dialogs that get displayed can be suppressed if needed using certain system variables or when the command is preceded with a "-" to in..."
author: Autodesk
---
# Dismissing popup dialogs in AutoCAD

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/dismissing-popup-dialogs-in-autocad.html

## 文章内容

By Balaji Ramamoorthy
Most AutoCAD dialogs that get displayed can be suppressed if needed using certain system variables or when the command is preceded with a "-" to invoke the commandline version of it. You can read about such usage in this post :
Switch Between Dialog Boxes and the Command Line
Also, for batch processing of drawings AccoreConsole or AutoCAD.IO is much more suited and does not have the limitation of dialogs popping up during processing. To know about these options, please refer to the following blog posts :
Getting started with AccoreConsole
Getting started with AutoCAD.IO
If you still find yourself needing a way to dismiss the dialog inside AutoCAD, you can try using Windows hooks to dismiss the dialog. Please note that this method is not recommended, but since it is a commonly asked query I have posted a sample code here. This sample code uses CBT hooks in C# and is based on this MSDN article:
How to set a Windows hook in Visual C# .NET
To use it, you will need to call the “SetupHook” and “RemoveHook” around the code which might result in the dialog and ensure that the hook closes the right dialog.
 //For example :      
 //    SetupHook(); 
 //    ...Some processing that might result in a dialog  
 //    ...that you want to close. 
 //    RemoveHook(); 
   public  delegate  int  HookProc(
    int  nCode, 
    IntPtr wParam, 
    IntPtr lParam);
   //Declare the hook handle as an int. 
 static  int  hHook = 0;
   //Declare the mouse hook constant. 
 //For other hook types, you can obtain these values 
 // from Winuser.h in the Microsoft SDK. 
 public  const  int  WH_CBT = 5;
   public  const  uint WM_CLOSE = 0x0010;
   private  static  long  HCBT_ACTIVATE = 5;
 private  static  long  HCBT_CREATEWND = 3;
   //Declare MouseHookProcedure as a HookProc type. 
 HookProc CBTHookProcedure_;
   // This is the Import for the SetWindowsHookEx function. 
 // Use this function to install a thread-specific hook. 
 [DllImport("user32.dll" , CharSet = CharSet.Auto, 
  CallingConvention = CallingConvention.StdCall)]
 public  static  extern  int  SetWindowsHookEx(int  idHook, 
  HookProc lpfn, IntPtr hInstance, int  threadId);
   // This is the Import for the UnhookWindowsHookEx function. 
 // Call this function to uninstall the hook. 
 [DllImport("user32.dll" , CharSet = CharSet.Auto, 
  CallingConvention = CallingConvention.StdCall)]
 public  static  extern  bool  UnhookWindowsHookEx(int  idHook);
   // This is the Import for the CallNextHookEx function. 
 // Use this function to pass the hook information  
 // to the next hook procedure in chain. 
 [DllImport("user32.dll" , CharSet = CharSet.Auto, 
  CallingConvention = CallingConvention.StdCall)]
 public  static  extern  int  CallNextHookEx(int  idHook, 
  int  nCode, IntPtr wParam, IntPtr lParam);
   [DllImport("user32.dll" , CharSet = CharSet.Auto, 
  SetLastError = true )]
 static  extern  int  GetWindowText(IntPtr hWnd, 
  System.Text.StringBuilder lpString, int  nMaxCount);
   [DllImport("user32.dll" )]
 static  extern  IntPtr GetActiveWindow();
   [DllImport("user32.dll" , CharSet = CharSet.Auto)]
 static  extern  IntPtr SendMessage(IntPtr hWnd,
  UInt32 Msg, IntPtr wParam, IntPtr lParam);
   public  static  int  CBTHookProcedure(int  nCode, 
  IntPtr wParam, IntPtr lParam)
 {
     if  (nCode < 0)
     {
   return  CallNextHookEx(
    hHook, nCode, wParam, lParam);
     }
     else 
     {
         System.Text.StringBuilder wndName 
    = new  System.Text.StringBuilder(300);
         GetWindowText(GetActiveWindow(), wndName, 300);
         if  (! wndName.ToString().Contains(
    "AutoCAD Civil 3D" ))
         {
             SendMessage(GetActiveWindow(), 
     WM_CLOSE, IntPtr.Zero, IntPtr.Zero);
         }
     }
     return  CallNextHookEx(hHook, nCode, wParam, lParam);
 }
   void  SetupHook()
 {
  if  (hHook == 0)
  {
   // Create an instance of HookProc. 
   CBTHookProcedure_ = new  HookProc(CBTHookProcedure);
     hHook = SetWindowsHookEx(
   WH_CBT,
   CBTHookProcedure_,
   (IntPtr)0,
   AppDomain.GetCurrentThreadId());
     //If the SetWindowsHookEx function fails. 
   if  (hHook == 0)
   {
    System.Windows.Forms.MessageBox.Show(
     "SetWindowsHookEx Failed" );
    return ;
   }
  }
 }
   void  RemoveHook()
 {
     if  (hHook != 0)
     {
   bool  ret = UnhookWindowsHookEx(hHook);
   //If the UnhookWindowsHookEx function fails. 
   if  (ret)
   {
    hHook = 0;
   }
     }
 }

