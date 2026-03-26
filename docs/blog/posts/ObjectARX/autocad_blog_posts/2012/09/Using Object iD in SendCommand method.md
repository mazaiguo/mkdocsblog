---
title: "Using Object iD in SendCommand method"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - Selection
description: "You can use Object id to send the "entity selection" while sending the command to AutoCAD using SendCommand API. You need to format the command str..."
author: Autodesk
---
# Using Object iD in SendCommand method

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/using-object-id-in-sendcommand-method.html

## 文章内容

By Virupaksha Aithal
You can use Object id to send the "entity selection" while sending the command to AutoCAD using SendCommand API. You need to format the command string such that it contains the objectid handles. Refer below code, which invokes the fillet command after getting 2 lines from the user. The fillet command is used to show the use of Object id during the command invocation and you can use this logic in any other command which requires object selection.
      <CommandMethod("TESTFILLET")> _
        Public Sub testFillet()
            Dim doc As Document = _
                        Application.DocumentManager.MdiActiveDocument
            Dim ed As Editor = doc.Editor
            Dim Db As Database = doc.Database
              Dim pEntRes1 As PromptEntityResult = ed.GetEntity( _
                                      "Select first line to Fillet")
            If pEntRes1.Status <> PromptStatus.OK Then
                Return
            End If
              Dim obj1 As String = pEntRes1.ObjectId.ObjectClass.Name
              If String.Compare(obj1, "AcDbLine", True) <> 0 Then
                ed.WriteMessage("Select line entity" + vbLf)
                Return
            End If
              Dim pEntRes2 As PromptEntityResult = ed.GetEntity( _
                                    "Select second line to Fillet")
            If pEntRes2.Status <> PromptStatus.OK Then
                Return
            End If
              obj1 = pEntRes2.ObjectId.ObjectClass.Name
              If String.Compare(obj1, "AcDbLine", True) <> 0 Then
                ed.WriteMessage("Select line entity" + vbLf)
                Return
            End If
              Dim strHandle1 As String = _
                        pEntRes1.ObjectId.Handle.ToString()
            Dim strEntName1 As String = _
                            "(handent """ & strHandle1 & """)"
              Dim strHandle2 As String = _
                            pEntRes2.ObjectId.Handle.ToString()
            Dim strEntName2 As String = _
                            "(handent """ & strHandle2 & """)"
              Dim strCommand As String = _
                        "_fillet" + vbCr + "r" + vbCr + "0.495" + _
                    vbCr + strEntName1 + vbCr + strEntName2 + vbCr
              doc.AcadDocument.SendCommand(strCommand)
          End Sub

## 评论

**内容**: JR said...
This was a very helpful insight. I used the concept to perform some other tasks. Thanks.
Reply
07/15/2016 at 06:03 AM

---
**内容**: everybody said...
how do this from vba?
Reply
02/19/2019 at 04:30 AM

---
**内容**: Vaibhav Shinde said in reply to everybody...
Dim strEntName1 As String
Dim rotobj As AcadEntity
strEntName1 = "(handent """ & rotobj.Handle & """)"

AcadDoc.SendCommand "ROTATE" & vbCr & strEntName1 & vbCr & " " & vbCr & 0 & "," & varpt(1) & "," & varpt(2) & vbCr
Reply
11/27/2019 at 11:00 PM

---
**内容**: Daboho said...
How if using promptselection
And ed.getselection() to any curve(multiple curve)
Multiple fillet using send command is posible
Reply
07/13/2020 at 04:13 PM

---
**内容**: Mike said...
Merci !
Reply
06/15/2021 at 02:25 AM

---
