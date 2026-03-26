---
title: "Refreshing External References palette using Microsoft UI Automation"
date: 2015-09-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Palette
  - Plugin
  - XREF
description: "In this blog post we will look at refreshing the external references palette in AutoCAD. Before we get into the details, here is some background in..."
author: Autodesk
---
# Refreshing External References palette using Microsoft UI Automation

发布日期: 2015-09-01

原始链接: https://adndevblog.typepad.com/autocad/2015/09/refreshing-external-references-palette-using-microsoft-ui-automation.html

## 文章内容

By Balaji Ramamoorthy
In this blog post we will look at refreshing the external references palette in AutoCAD. Before we get into the details, here is some background information on why it might be required to refresh that palette.
The external references palette in AutoCAD turns into an Enhanced Standard Window (ESW) when the Vault plugin for AutoCAD is installed. Since the check-in/ check-out status of the files are displayed in the external references palette, it is necessary for a way to refresh the palette to display the current status in case the file status got modified externally using Vault client.
Because there is no public API to do this, we will look at using Microsoft's UI Automation to simulate a click on the Refresh button. Please note that the approach suggested here is unsupported by Autodesk as it relies on Win32 and UI Automation API. If you need to use this approach, please test it more completely with your application.
To get the click on Refresh button to work, the Microsoft UI Automation has all the necessary API. Unfortunately, the nature of the Refresh button in the external references palette in AutoCAD posed a problem. By looking at the layout of the External References palette using Spy++, it becomes evident that the Refresh button is part of a Toolbar inside the palette. Also, the Refresh button is a drop-down with Reload and Refresh options. By using the UI Automation's Invoke pattern, it was not possible to simulate a mouse click on the Refresh button.
To work around this, we can resort to Win32 API's SendInput method to simulate a mouse click and gather the inputs required by that method using Microsoft UI Automation API. Here is a sample code that works ok in AutoCAD 2016. For other AutoCAD versions, you may need to identify the control-id of the Refresh button using Spy++ and update the code accordingly.
 // Add reference to UIAutomationClient.dll  
 // and UIAutomationTypes.dll 
 using  System.Windows.Automation;
 using  System.Diagnostics;
 using  System.Runtime.InteropServices;
   using  Autodesk.AutoCAD.Runtime;
 using  Autodesk.AutoCAD.EditorInput;
 using  Autodesk.AutoCAD.DatabaseServices;
 using  Autodesk.AutoCAD.ApplicationServices;
     // Based on http://www.pinvoke.net 
 // /default.aspx/user32/SendInput.html 
 // /default.aspx/Structures/MOUSEINPUT.html 
 // /default.aspx/user32/mouse_event.html 
   [DllImport("user32.dll" , SetLastError = true )]
 static  extern  uint SendInput(uint nInputs, 
  INPUT[] pInputs, int  cbSize);
   [StructLayout(LayoutKind.Sequential)]
 internal  struct  MOUSEINPUT
 {
     public  int  dx;
     public  int  dy;
     public  uint mouseData;
     public  uint dwFlags;
     public  uint time;
     public  IntPtr dwExtraInfo;
 }
   [StructLayout(LayoutKind.Sequential)]
 internal  struct  INPUT
 {
     public  int  type;
     public  MOUSEINPUT mi;
     public  INPUT(uint flag)
     {
         type = 0; // Mouse input 
         mi.dx = 0;
         mi.dy = 0;
         mi.mouseData = 0;
         mi.time = 0;
         mi.dwExtraInfo = IntPtr.Zero;
         mi.dwFlags = flag;
     }
 }
           private  const  int  MOUSEEVENTF_LEFTDOWN = 0x0002;
 private  const  int  MOUSEEVENTF_LEFTUP = 0x0004;
   [CommandMethod("XRefPalRefresh" )]
 public  void  XRefPalRefresh()
 {
     Editor ed = 
   Application.DocumentManager.MdiActiveDocument.Editor;
     try 
     {
         System.Diagnostics.Process p 
    = Process.GetCurrentProcess();
         AutomationElement acadAutoElem = 
    AutomationElement.RootElement.FindFirst(
    TreeScope.Children, 
             new  PropertyCondition(
    AutomationElement.ProcessIdProperty, p.Id));
           // Control Id retreived for the Refresh button  
   // in AutoCAD 2016 using Spy++ 
         string btnRefreshhexID = "000075FB" ;
         string btnRefreshdecimalID = 
    System.Convert.ToInt32(btnRefreshhexID, 16)
    .ToString();
         AutomationElement refreshBtnAutoElem 
    = acadAutoElem.FindFirst(
             TreeScope.Descendants, 
             new  PropertyCondition(
    AutomationElement.AutomationIdProperty, 
    btnRefreshdecimalID));
           if  (refreshBtnAutoElem == null)
         {
             ed.WriteMessage("Refresh button in  
     External References
     palette was not identified !"); 
             return ;
         }
                           // Using UI's Invoke pattern 
         // Does work for simple buttons but not for  
   // the Refresh button in  
         //'s external references palette. 
         //InvokePattern ipClickRefreshBtn =  
   // (InvokePattern)refreshBtnAutoElem.GetCurrentPattern 
   // (InvokePattern.Pattern); 
         //ipClickRefreshBtn.Invoke(); 
           //'s resort to clicking by location. 
         System.Windows.Point point 
    = refreshBtnAutoElem.GetClickablePoint();
         System.Windows.Forms.Cursor.Position 
             = new  System.Drawing.Point(
    (int )point.X, (int )point.Y);
           INPUT input1 = new  INPUT(MOUSEEVENTF_LEFTDOWN);
         INPUT input2 = new  INPUT(MOUSEEVENTF_LEFTUP);
         SendInput(2, new [] { input1, input2 }, 
    Marshal.SizeOf(typeof(INPUT)));
     }
     catch  (System.Exception ex)
     {
         ed.WriteMessage(ex.Message);
     }
 }
  Before we end this blog post, a known limitation of this approach is that the external palette must be open and the Refresh button in it must not be masked by any other window.

