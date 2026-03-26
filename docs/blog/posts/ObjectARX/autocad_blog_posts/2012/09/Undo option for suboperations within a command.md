---
title: "Undo option for suboperations within a command"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "I would like to provide the undo option for the suboperations in my custom command similar to the Line command in AutoCAD. Can you provide an examp..."
author: Autodesk
---
# Undo option for suboperations within a command

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/undo-option-for-suboperations-within-a-command.html

## 文章内容

By Balaji Ramamoorthy
Issue
I would like to provide the undo option for the suboperations in my custom command similar to the Line command in AutoCAD. Can you provide an example ?
Solution
Undo of a command is recorded by AutoCAD and all actions performed in it is recorded as a single undoable item in its undo stack.
To be able to undo suboperations, the command should handle it on its own by providing the "undo" option while prompting for input and acting accordingly when user opts for it.
Here is a command that replaces text entities in a drawing and each of the suboperations can be undone.
The logic to undo a previous suboperation is handled by the command.
The undo of the entire command is handled by AutoCAD. To try this command, use the attached drawing and invoke the command.
Each operation can be undone separately just like the "Line" command in AutoCAD.
Imports System.Collections.Specialized
  <CommandMethod("Test")> _
Public Sub commandMethodTest()
    Dim _oids As New ObjectIdCollection()
    Dim _previousTextColl As New StringCollection()
      Dim activeDoc As Document = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument
    Dim db As Database = activeDoc.Database
    Dim ed As Editor = Application.DocumentManager.MdiActiveDocument.Editor
      Dim cnt As Integer = 1
    While True
        Dim replaceText As [String] = [String].Format("String{0}", cnt)
        Dim peo As New PromptEntityOptions([String].Format("Pick text for {0} ", replaceText))
        If cnt > 1 Then
            peo.Keywords.Add("Undo")
            peo.AppendKeywordsToMessage = True
        End If
          peo.SetRejectMessage("Selected entity type is not valid. Please select a text entity")
        peo.AddAllowedClass(GetType(DBText), True)
        Dim per As PromptEntityResult = ed.GetEntity(peo)
          If per.Status = PromptStatus.Keyword Then
            ' Undo the previous text change
            If _oids.Count > 0 AndAlso _previousTextColl.Count > 0 Then
                Using Tx As Transaction = db.TransactionManager.StartTransaction()
                    Dim dbText As DBText = TryCast(Tx.GetObject(_oids(_oids.Count - 1), OpenMode.ForWrite), DBText)
                    dbText.TextString = _previousTextColl(_previousTextColl.Count - 1)
                    Tx.Commit()
                      _oids.RemoveAt(_oids.Count - 1)
                    _previousTextColl.RemoveAt(_previousTextColl.Count - 1)
                End Using
                cnt -= 1
            End If
        ElseIf per.Status = PromptStatus.OK Then
            ' Replacement
            Using Tx As Transaction = db.TransactionManager.StartTransaction()
                Dim dbText As DBText = TryCast(Tx.GetObject(per.ObjectId, OpenMode.ForWrite), DBText)
                  'To be able to undo if required.
                _oids.Add(per.ObjectId)
                _previousTextColl.Add(dbText.TextString)
                  dbText.TextString = replaceText
                Tx.Commit()
            End Using
            cnt += 1
        Else
            ' Cancelled
            ed.WriteMessage(vbLf & "Cancelled.")
            Exit While
        End If
    End While
End Sub

## 评论

**内容**: Gilles Chanteau said...
Hi,
What about using a Stack(Of String) instead of a StringCollection ?
Regards,
Gilles
Reply
09/02/2012 at 12:33 AM

---
**内容**: Balaji said in reply to Gilles Chanteau...
Hi Gilles,
Thank you, Yes indeed a stack would be a more appropriate data structure to use in this case.
Push / Pop instead of the Add and RemoveAt is definitely more intuitive.
Thank you.
Reply
09/03/2012 at 03:57 AM

---
