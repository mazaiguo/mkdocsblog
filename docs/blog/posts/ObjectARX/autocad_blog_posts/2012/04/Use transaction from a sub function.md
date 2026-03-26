---
title: "Use transaction from a sub function"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - Block
description: "If you start a transaction inside your main function, then you do not need to create another one (a sub transaction) inside your sub function, you ..."
author: Autodesk
---
# Use transaction from a sub function

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/use-transaction-from-a-sub-function.html

## 文章内容

By Adam Nagy
If you start a transaction inside your main function, then you do not need to create another one (a sub transaction) inside your sub function, you do not even need to pass the transaction to the sub function, you can simply use ObjectId.GetObject() instead, which will automatically use the outer transaction you started.
Public Sub MoveBlock( _
  ByRef blockRefId As ObjectId, _
    ByVal newLocation As Point3d)
    Dim blockRef As BlockReference = _
    blockRefId.GetObject(OpenMode.ForWrite)
    blockRef.Position = newLocation
  End Sub
  <CommandMethod("MoveBlockCommand")> _
Public Sub MoveBlockCommand()
  Dim ed As Editor = _
    Application.DocumentManager.MdiActiveDocument.Editor
    Dim perEntity As PromptEntityResult = _
    ed.GetEntity("Select block to move: " + vbCrLf)
  If perEntity.Status <> PromptStatus.OK Then Return
    Dim pprPoint As PromptPointResult = _
    ed.GetPoint("Pick the new position for the block: " + vbCrLf)
  If pprPoint.Status <> PromptStatus.OK Then Return
    Dim db As Database = HostApplicationServices.WorkingDatabase
    Using tr As Transaction = db.TransactionManager.StartTransaction
    MoveBlock(perEntity.ObjectId, pprPoint.Value)
      tr.Commit()
  End Using
End Sub

## 评论

**内容**: Eyal Cohen said...
Adam thanks.
I hope this message finds you well (long time since your post).
Following your insight
(i.e. no necessity of both outer+inner trans objects):
Suppose we have "outer" main procedures (e.g. commands subs),
which call a variety of "inner" helper methods.
Do you think there is a preferred practice:
a. Start an "outer" transaction inside the main procedure? or
b. create "inner" transactions inside each of the helper methods?
Thanks in advance, Eyal.
Reply
11/13/2020 at 11:48 PM

---
