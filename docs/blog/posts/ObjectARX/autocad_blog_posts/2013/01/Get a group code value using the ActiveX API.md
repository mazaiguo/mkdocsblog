---
title: "Get a group code value using the ActiveX API"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - API
  - AutoLISP
  - Block
  - COM
  - XREF
description: "There is no straight-forward method to get the group code value in activex. You can use a lisp string along with a user variable to get the value. ..."
author: Autodesk
---
# Get a group code value using the ActiveX API

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/get-a-group-code-value-using-the-activex-api.html

## 文章内容

By Gopinath Taget
There is no straight-forward method to get the group code value in activex. You can use a lisp string along with a user variable to get the value. For instance if you want to find out if an XRef is attached or an Overlay, you can use Group Code 70 to determine this.
Here is the VB snippet for this:
Sub GetXRefType()
'note there is no error handling included
Dim ps_str As String
Dim po_blk As AcadBlock
Dim po_blkref As AcadEntity
Dim pi_dxf70 As Integer
Dim pv_1 As Variant
ThisDrawing.Utility.GetEntity po_blkref, pv_1, "Select an xref..."
Set po_blk = ThisDrawing.Blocks(po_blkref.Name) ps_str = "(SETVAR ""USERR1"" (cdr (assoc 70 (tblsearch ""BLOCK"" """ & po_blkref.Name & """)))) "
ThisDrawing.SendCommand ps_str
pi_dxf70 = ThisDrawing.GetVariable("USERR1")
If pi_dxf70 = 44 Then MsgBox "XREF " & po_blk.Name & " is Overlaid."
If pi_dxf70 = 36 Then MsgBox "XREF " & po_blk.Name & " is Attached."
End Sub

