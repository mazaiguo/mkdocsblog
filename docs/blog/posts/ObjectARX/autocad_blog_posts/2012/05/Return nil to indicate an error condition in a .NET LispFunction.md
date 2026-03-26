---
title: "Return nil to indicate an error condition in a .NET LispFunction"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - AutoLISP
description: "I am implementing functionality in .NET that I am using from AutoLISP. How can I return an error condition from the .NET function?"
author: Autodesk
---
# Return nil to indicate an error condition in a .NET LispFunction

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/return-nil-to-indicate-an-error-condition-in-a-net-lispfunction.html

## 文章内容

By Wayne Brill
Issue
I am implementing functionality in .NET that I am using from AutoLISP. How can I return an error condition from the .NET function?
Solution
One suggestion is to return nil from the .NET function using the LispDataType. If the function does return nil you could then handle that appropriately. (Or you could return an integer and respond to that value in the LISP function)
Here is an excerpt from the AutoCAD .NET Managed Class Reference guide for the LispDataType:
Public Enum LispDataType
  Angle = &H138c
  DottedPair = &H139a
  Double = &H1389
  Int16 = &H138b
  Int32 = &H1392
  ListBegin = &H1398
  ListEnd = &H1399
  Nil = &H139b
  None = &H1388
  ObjectId = &H138e
  Orientation = &H1390
  Point2d = &H138a
  Point3d = &H1391
  SelectionSet = &H138f
  T_atom = &H139d
  Text = &H138d
  Void = &H1396
End Enum
Here is a VB example. Notice that if the entity is not selected ok, the routine returns nil.
<LispFunction("getId")>
Public Function test _
  (ByVal myLispArgs As ResultBuffer) As ResultBuffer
    ' This example asks the user to select
    ' an(entity) The object id of the entity is
    ' returned to the calling lisp function
    Dim rbfResult As ResultBuffer
    Dim ed As Autodesk.AutoCAD.EditorInput.Editor
    ed = Autodesk.AutoCAD.ApplicationServices. _
                  Application.DocumentManager. _
                        MdiActiveDocument.Editor
      Dim prmptEntOpts As New PromptEntityOptions _
                                  ("Select Entity")
    Dim prmptEntRes As PromptEntityResult
      ' Get the entity from the users selection
    prmptEntRes = ed.GetEntity(prmptEntOpts)
      ' Make sure the entity was selected ok
    If prmptEntRes.Status <> PromptStatus.OK Then
        rbfResult = New ResultBuffer _
              (New TypedValue(LispDataType.Nil))
        Return rbfResult
    End If
      ' Return the ObjectId to the Lisp function
    Dim objId As ObjectId
    objId = prmptEntRes.ObjectId
    rbfResult = New ResultBuffer _
      (New TypedValue(LispDataType.ObjectId, objId))
      Return rbfResult
  End Function
Here is a LISP function that uses the .NET function:
    (defun c:testID ( / objId nilTest ent)
    (setq objId (getId))
    (setq nilTest (nth 0 objId))
    (if (= nilTest nil)
        (princ "Entity not selected")
      )
 
     (if (/= nilTest nil)
     (progn
          (vl-load-com);ensure COM API is available
        (setq ent (vlax-ename->vla-object (nth 0 objId)));the 0 element is an ename
      (vla-highlight ent :vlax-true); highlight the entity using COM call
     );progn
    );if
    (princ)
    )

## 评论

**内容**: Thomas said...
When using VB.net to create lisp functions do not specify the return value As ResultBuffer then the type casting will be a result of your return type
You can then return any of the LispDataType Enum's or a Boolean for T or NIL. Using Return False will result in a nil being returned to the calling lisp function
If you specify the return type As ResultBuffer for the VB.net function the calling lisp function will get a list every time.
Reply
12/17/2014 at 07:38 AM

---
