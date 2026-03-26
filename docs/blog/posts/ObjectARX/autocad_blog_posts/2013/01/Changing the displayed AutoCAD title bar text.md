---
title: "Changing the displayed AutoCAD title bar text"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Unicode
description: "Is it possible to change the text displayed in the AutoCAD title bar?"
author: Autodesk
---
# Changing the displayed AutoCAD title bar text

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/changing-the-displayed-autocad-title-bar-text.html

## 文章内容

By Xiaodong Liang
Issue
Is it possible to change the text displayed in the AutoCAD title bar?
Solution
With ObjectARX you can do the following:
static void test()
{
    acedGetAcadFrame()->SetWindowText (
                       _T("My AutoCAD"));
}
There is no AutoLISP or AutoCAD ActiveX API that will set this because the AutoCAD ActiveX Application Object's Caption Property is read-only. However, you can use the Win32 API functions, GetActiveWindow and SetWindowText.  Following is a code demo of VB.NET.
  ' declare the global functions of Windows
     Public Declare Function _
        GetActiveWindow Lib "user32" () As Long
      Public Declare Function _
        GetWindowText Lib "user32" Alias _   
            "GetWindowTextA" ( _
            ByVal hwnd As Long, _
            ByVal lpString As String, _
            ByVal cch As Long) As Long
       Public Declare Function _
        SetWindowText Lib "user32" Alias _
            "SetWindowTextA" ( _
            ByVal hwnd As Long,  _
            ByVal lpString As String) As Long
      Public Declare Function _
        FindWindow Lib "user32" Alias  _ 
                 "FindWindowA" ( _
                    ByVallpClassName As String,  _
               ByVal lpWindowName As String) As Long
     Sub test() 
        Const progID As String =  
                  "AutoCAD.Application.18"
          Dim acType As Type = _
            Type.GetTypeFromProgID(progID)
        Dim AcadApp As AcadApplication = Nothing
          AcadApp =
         CType(Activator.CreateInstance(acType, True),
                AcadApplication)
          System.Threading.Thread.Sleep(2000)
          AcadApp.Visible = True
          Dim acadhnd As Long
        Dim titletxt As String
        Dim curtxt As String
          titletxt = "This is my version of AutoCAD"
        curtxt = Space(256)
          'Obtains the handle of AutoCAD window.
        'acadhnd = GetActiveWindow
        ' use the AutoCAD caption to get the handle
        acadhnd = FindWindow(vbNullString,
                               AcadApp.Caption)
          'Obtain the current text in the titlebar.
        GetWindowText(acadhnd, curtxt, 125)
        MsgBox(curtxt)
          'Set the desired text for the titlebar.
        SetWindowText(acadhnd, titletxt)
 End Sub

## 评论

**内容**: ian.robinson@aecom.com said...
Is it possible for you to supply files containing the coding?
Kind regards, Robbo.
Reply
02/18/2014 at 01:49 AM

---
**内容**: ian.robinson@aecom.com said...
A VB.Net beginner.
How can I get this to work with VS 2012 Express using 2014 wizard?
Any help appreciated.
Many thanks in advance.
Reply
02/23/2014 at 10:26 AM

---
**内容**: Anwar said...
Dear Friends,
I can't seethe quick access toolbar of my AutoCAD 2012 with windows 10, when it is on top of ribbon but when it is bellow the ribbon i can see it?
how can is change the white color of this bar in order i can see it.
Reply
08/05/2019 at 12:27 AM

---
