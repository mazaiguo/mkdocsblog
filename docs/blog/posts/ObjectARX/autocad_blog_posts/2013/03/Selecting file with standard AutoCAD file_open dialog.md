---
title: "Selecting file with standard AutoCAD file/open dialog"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - DWG
  - VBA
description: "Can I gain access to the "Open File Dialog" (with preview) found only in AutoCAD with VBA?"
author: Autodesk
---
# Selecting file with standard AutoCAD file/open dialog

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/selecting-file-with-standard-autocad-fileopen-dialog.html

## 文章内容

By Xiaodong Liang
Issue
Can I gain access to the "Open File Dialog" (with preview) found only in AutoCAD with VBA?
Solution
You can do this through the communication interface with AutoLISP and AutoCAD. The AutoLISP function, getfiled, behaves as the AutoCAD "Open File Dialog" and allows .DWG files to be previewed.
VBA:
Public Sub OpenDialog()
   Dim fileName As String
   'Using the SendCommand method, send getfiled AutoLISP expressions to the AutoCAD command line.
   'Set the return value to a user-defined system variable USERS1.
   ThisDrawing.SendCommand "(setvar " & """users1""" & "(getfiled " & """Select a DWG File""" & """c:/program files/acad2012/""" & """dwg""" & "8)) "
   'Use the GetVariable method to retrieve this system variable to store the selected file name
   fileName = ThisDrawing.GetVariable("users1")
   MsgBox "You have selected " & fileName & "!!!", , "File Message"
End Sub
VB.NET
      Public Sub OpenDialog(AcadApp As AcadApplication)
        Dim ThisDrawing As AcadDocument
        ThisDrawing = AcadApp.ActiveDocument
          Dim fileName As String
        'Using the SendCommand method, send getfiled
       ‘AutoLISP expressions to the AutoCAD command
       ‘line.Set the return value to a user-defined 
       ‘system variable USERS1.
        ThisDrawing.SendCommand("(setvar " &  
                                 """users1""" &
                                  "(getfiled " &
                          """Select a DWG File""" &
                    """c:/program files/acad2012/""" &
                   """dwg""" & "8)) ")
        'Use the GetVariable method to retrieve this 
        ‘system variable to store selected file name
        fileName = ThisDrawing.GetVariable("users1")
        MsgBox("You have selected " &
                fileName & "!!!", ,
                 "File Message")
    End Sub

## 评论

**内容**: Tony Tanzillo said...
It's truly shameful that VBA programmers must resort to this sort of kludgery to solve a simple problem like this.
But, if they have to, then VL.Application would be a better way to go about it.
Reply
03/30/2013 at 11:06 AM

---
**内容**: rob said...
but what if I want the user to select multiple files (as per the old commondialog.
I have tried to use the API but fails on the call to GetOpenFileName. returns 0 without showing dialog.
Reply
05/24/2013 at 01:01 AM

---
**内容**: BlackBox said...
Wow... Where's this beauty in the Developer Documentation?
Reply
05/24/2013 at 10:41 AM

---
