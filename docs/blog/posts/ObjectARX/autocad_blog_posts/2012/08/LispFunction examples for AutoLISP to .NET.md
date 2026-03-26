---
title: "LispFunction examples for AutoLISP to .NET"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
  - Selection
description: "It is possible to pass standard data types to and from .NET using a result buffer and the <LispFunction> directive. Below are two .NET methods that..."
author: Autodesk
---
# LispFunction examples for AutoLISP to .NET

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/lispfunction-examples-for-autolisp-to-net.html

## 文章内容

By Augusto Goncalves
It is possible to pass standard data types to and from .NET using a result buffer and the <LispFunction> directive. Below are two .NET methods that make selections, and return (1) one entity ID or (2) a set of entities IDs.
<LispFunction("MyLispFunction1")> _
Public Function SelectOneEntity( _
                ByVal myLispArgs As ResultBuffer) _
              As ResultBuffer
    Dim rbfResult As ResultBuffer
  Dim ed As Editor = Application.DocumentManager. _
    MdiActiveDocument.Editor
    ' select one entity
  Dim prmptEntOpts As New PromptEntityOptions( _
    "Select Entity")
  Dim prmptEntRes As PromptEntityResult
    prmptEntRes = ed.GetEntity(prmptEntOpts)
  If prmptEntRes.Status <> PromptStatus.OK Then
    rbfResult = New ResultBuffer( _
      New TypedValue(5019))
    Return rbfResult
  End If
    ' return the objectId selected
  Dim objId As ObjectId
  objId = prmptEntRes.ObjectId
  rbfResult = New ResultBuffer( _
    New TypedValue(5006, objId))
    Return rbfResult
End Function
  <LispFunction("MyLispFunction2")> _
Public Function SelectSetOfEntities( _
                ByVal myLispArgs As ResultBuffer) _
              As ResultBuffer
    Dim rbfResult As ResultBuffer
  Dim ed As Editor = Application.DocumentManager. _
    MdiActiveDocument.Editor
    ' make a selection
  Dim prmptSelOpts As New PromptSelectionOptions()
  Dim prmptSelRes As PromptSelectionResult
    prmptSelRes = ed.GetSelection(prmptSelOpts)
    If prmptSelRes.Status <> PromptStatus.OK Then
    rbfResult = New ResultBuffer(New TypedValue(5019))
    Return rbfResult
    End If
    ' return the selection set
  Dim selSet As SelectionSet
  selSet = prmptSelRes.Value
  rbfResult = New ResultBuffer( _
              New TypedValue(CInt(5007), selSet))
  Return rbfResult
End Function
And now the LISP to call those methods, no change here.
(defun c:test1 ()
    (setq MyList (MyLispFunction1))
  )
 
(defun c:test2 ()
  (setq MyList (MyLispFunction2))
)

## 评论

**内容**: Gilles Chanteau said...
Hi Augusto,
Rather than returning ResultBuffers which are converted into LISP lists, I'd return the expected LISP type expected: an ename (or nil) and a PickSet (or nil).
MyLispFunction1 would return a TypedValue: New TypedValue(LispDatatype.ObjectId, objId) or New TypedValue(LispDataType.Nil) if the PromptEntityResult.Status is not Ok, and MyLispFunction2 would return directly a SelectionSet (Nothing if PromptSelectionResult.Status is not Ok).
Reply
08/22/2012 at 02:02 PM

---
