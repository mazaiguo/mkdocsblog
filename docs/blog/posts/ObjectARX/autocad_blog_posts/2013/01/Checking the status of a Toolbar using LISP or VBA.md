---
title: "Checking the status of a Toolbar using LISP or VBA"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - VBA
description: "How to check, at any time, whether a toolbar is shown or not, using either Visual LISP or VBA?"
author: Autodesk
---
# Checking the status of a Toolbar using LISP or VBA

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/checking-the-status-of-a-toolbar-using-lisp-or-vba.html

## 文章内容

By Fenton Webb
Issue
How to check, at any time, whether a toolbar is shown or not, using either Visual LISP or VBA?
Solution
The following LISP and VBA code will tell you the current status of a specific toolbar.  To modify it, substitute the appropriate menugroup, toolbar name, and properties. 
LISP:
;;; For demonstration purposes only
;;; No error checking provided
(defun C:TBar_Chk()
   (vl-load-com)
   (setq oAcad (vlax-get-acad-object)
           oDoc (vla-get-activedocument oAcad)
           oMenuGrp (vla-item (vla-get-menugroups oAcad) "ACAD")
           oTBar (vla-item (vla-get-toolbars oMenuGrp) "Viewports")
           sTBarName (vlax-get-property oTBar 'name)
   )  
   (if (= (vlax-get-property oTBar 'visible) :vlax-true)
      (alert (strcat "Toolbar: " sTBarName "\nStatus: Visible"))
      (alert (strcat "Toolbar: " sTBarName "\nStatus: Hidden"))
   )
)
VBA:
';;; For demonstration purposes only
';;; No error checking provided
Sub TBar_Chk()
    Dim oMenuGrp As AcadMenuGroup
    Dim oTBar As AcadToolbar
    Dim sTBarName As String
    Set oMenuGrp = ThisDrawing.Application.MenuGroups.Item("ACAD")
    Set oTBar = oMenuGrp.Toolbars.Item("Viewports")
    sTBarName = oTBar.Name
    If oTBar.Visible = True Then
        MsgBox "Toolbar: " + sTBarName + vbCr + "Status: Visible"
    Else
        MsgBox "Toolbar: " + sTBarName + vbCr + "Status: Hidden"
    End If
End Sub

