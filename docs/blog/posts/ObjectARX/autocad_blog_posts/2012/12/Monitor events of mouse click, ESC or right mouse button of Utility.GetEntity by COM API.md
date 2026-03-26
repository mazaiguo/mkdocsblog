---
title: "Monitor events of mouse click, ESC or right mouse button of Utility.GetEntity by COM API"
date: 2012-12-01
categories:
  - AutoCAD COM
tags:
  - API
  - COM
description: "Is it possible to know what a user has clicked after the follow command :"
author: Autodesk
---
# Monitor events of mouse click, ESC or right mouse button of Utility.GetEntity by COM API

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/monitor-events-of-mouse-click-esc-or-right-mouse-button-of-utilitygetentity-by-com-api.html

## 文章内容

By Xiaodong Liang
Issue
Is it possible to know what a user has clicked after the follow command :
AppAcad.ActiveDocument.Utility.GetEntity ObjPall, pnt, "Select Entity".
I want to know the user has selected a point in the draft, and not an entity, or has canceled the command by "ESC" or right mouse button.
Solution
COM API  has event AcadDocument.BeginRightClick to watch right mouse event. But no method to monitor ESC. The workaround is to have the error status and do what you want in the exception. The sample below demonstrates this.
Sub Example()

   Dim returnObj As AcadObject
   Dim basePnt As Variant

     On Error GoTo ERRHAND
     ThisDrawing.Utility.GetEntity returnObj, basePnt, "Select Entity"

    'If returnObj.ObjectID <> 0 Then  ' on 32bits OS
    If returnObj.ObjectID32 <> 0 Then ' on 64bits OS
        MsgBox "You selected an object!"
End If
Exit Sub

 
ERRHAND:
   
     'do what you want
     Call ThisDrawing.Utility.Prompt(Err.Description & vbCr)
     Resume ' back to GetEntity
End Sub


Private Sub AcadDocument_BeginRightClick(ByVal PickPoint As Variant)
    Call ThisDrawing.Utility.Prompt("AcadDocument_BeginRightClick" & vbCr)
End Sub

Private Sub AcadDocument_BeginSave(ByVal FileName As String)

End Sub

## 评论

**内容**: ko0ls said...
can you change it to vb.net
Reply
12/14/2013 at 12:33 AM

---
