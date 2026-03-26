---
title: "How to combine a .Net Jig and MessageFilter to catch user input such as Right Click?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - DWG
  - Database
description: "Here is a common question developers were asking to ADN support:"
author: Autodesk
---
# How to combine a .Net Jig and MessageFilter to catch user input such as Right Click?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-combine-a-net-jig-and-messagefilter-to-catch-user-input-such-as-right-click.html

## 文章内容

By Philippe Leefsma
Here is a common question developers were asking to ADN support:
I use a EntityJig derived class to let the user place a block reference in the dwg, it works fine but I would like to let the user get a null angle just giving a right click when prompted for the angle. Using "UserInputControls.NullResponseAccepted" doesn't seem to work as expected.
Do you have a solution to handle that request?
Solution
Here is a complete VB.Net sample that illustrates ho to handle a MessageFilter within a Jig. The sample could be extended to monitor more user actions if needed.
  Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.EditorInput
Imports Autodesk.AutoCAD.Geometry
Imports Autodesk.AutoCAD.Runtime
Imports System.Runtime.InteropServices
  '////////////////////////////////////////////////////////////////////
'// Use: Jig a newly created block reference
'// Author: Philippe Leefsma, September 2011
'////////////////////////////////////////////////////////////////////
Public Class JigMsgFilter
    Inherits EntityJig
      Private _position As Point3d
    Private _filter As JigFilter
      Public Sub New(ByVal btrId As ObjectId)
        MyBase.New(New BlockReference(Point3d.Origin, btrId))
          _position = Point3d.Origin
        _filter = New JigFilter
          System.Windows.Forms.Application.AddMessageFilter(_filter)
      End Sub
      Public Overloads ReadOnly Property Entity() As BlockReference
        Get
            Return MyBase.Entity
        End Get
    End Property
      Protected Overloads Overrides Function Update() As Boolean
        Entity.Position = _position
        Return True
    End Function
      Protected Overloads Overrides Function Sampler( _
        ByVal prompts As JigPrompts) _
            As SamplerStatus
          Dim jigOpts As JigPromptPointOptions = _
          New JigPromptPointOptions(vbCrLf + "Specify position: "))
        jigOpts.UserInputControls = _
            UserInputControls.NullResponseAccepted
          Dim res As PromptPointResult = prompts.AcquirePoint(
            jigOpts)
          If (res.Status <> PromptStatus.OK) Then
            Return SamplerStatus.Cancel
        End If
          If (_position = res.Value) Then
            Return SamplerStatus.NoChange
        End If
          _position = res.Value
          Return SamplerStatus.OK
      End Function
      Public Function Run() As PromptStatus
        Dim promptResult As PromptResult = _
        Application.DocumentManager.MdiActiveDocument.Editor.Drag(Me)
        Return promptResult.Status
    End Function
      '////////////////////////////////////////////////////////////
    '// Use: Start Jig command
    '//
    '////////////////////////////////////////////////////////////
    Public Shared Sub JigMsgFilter()
          Dim doc As Document = _
            Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Dim res As PromptResult = _
            ed.GetString(vbCrLf + "Enter block name to insert: ")
          If res.Status <> PromptStatus.OK Then
            Exit Sub
        End If
          Using Tx As Transaction = _
            db.TransactionManager.StartTransaction()
              Dim bT As BlockTable = Tx.GetObject( _
                db.BlockTableId, _
                OpenMode.ForRead)
              If (Not bT.Has(res.StringResult)) Then
                ed.WriteMessage(vbCrLf + "Block do not exist :(")
                Exit Sub
            End If
              Dim btrId As ObjectId = bT(res.StringResult)
              Dim jig As New JigMsgFilter(btrId)
              If (jig.Run() <> PromptStatus.OK) Then
                jig.Entity.Dispose()
                Exit Sub
            End If
              Dim model As BlockTableRecord = Tx.GetObject( _
                bT(BlockTableRecord.ModelSpace), _
                OpenMode.ForWrite)
              model.AppendEntity(jig.Entity)
              Tx.AddNewlyCreatedDBObject(jig.Entity, True)
            Tx.Commit()
          End Using
      End Sub
      '////////////////////////////////////////////////////////////
    '// Use: Implementation of message filter
    '//
    '////////////////////////////////////////////////////////////
    Private Class JigFilter
        Implements System.Windows.Forms.IMessageFilter
          Private WM_RIGHTCLICK As Integer = &H204
          Public Function PreFilterMessage( _
            ByRef m As System.Windows.Forms.Message) _
                As Boolean _
            Implements _
                System.Windows.Forms.IMessageFilter.PreFilterMessage
              If m.Msg = WM_RIGHTCLICK Then
                  Dim doc As Document = _
                    Application.DocumentManager.MdiActiveDocument
                Dim ed As Editor = doc.Editor()
                  ed.WriteMessage(vbCrLf + "Right Button pressed!!")
                  'Block message for AutoCAD
                Return True
              End If
              Return False
          End Function
      End Class
  End Class

## 评论

**内容**: David said...
Hello Philippe,
Thanks for the Post,
I am trying to reuse it and I am not able to.
Code prompts for block name and then it shows a
Colon at command prompt. Nothing appear on cross hair.
left click exit program and right click the same.
even right clisk doesn't show the message.
I am using 2012 , 64 bit.
Reply
07/04/2012 at 04:48 PM

---
**内容**: Philippe said in reply to David...
Hi David,
The colon was caused by the "prompts.AcquirePoint" without text argument. I updated that with the string "Specify position:".
However the code works fine on my side. I am running Win7 x64 - AutoCAD 2012. Do you have a different configuration?
Reply
07/05/2012 at 02:26 AM

---
**内容**: David said in reply to Philippe...
No Philippe. Could you please tell me what should I expect to see when this program runs. I am really trying to understand this Imessagefilter with try and error. Thanks,
Reply
07/05/2012 at 05:12 AM

---
**内容**: David said...
still I am struggle and on right click I don't get that message and I don't get any error neither.
It is strange.
Reply
07/05/2012 at 08:16 PM

---
**内容**: Philippe said...
You should see a moving block reference following the mouse pointer, by left-clicking it will place the block, right-click will print a message to the editor.
The "System.Windows.Forms.IMessageFilter" is a .Net functionality, you should be able to easily find doc about it from msdn.
Reply
07/10/2012 at 12:17 AM

---
**内容**: David said...
I got it Philippe . Thanks.
Reply
07/10/2012 at 05:59 PM

---
**内容**: Maria said...
Thank you for your example and the inside on jig. I'm trying to use this code to solve a problem of mine to no avail.
Specifically, I've created a dynamic block by adding two Grip points.
When I run the insert command I select my block and check "Specify On-Screen" in the Insertion point group. The prompt on the screen is "Specify insertion point or [Basepoint/Scale/Rotate]:" and at this point I can click the CTRL button and the block will cycle through my grip points.
I can use your example code to prompt the user to place the block and can capture the CTRL button. What I'm struggling is to make AUTOCAD redraw the block after each time I press the CTRL button at the next snapping point (meaning the mouse cross hair becomes the next snapping point of my block).
Any inside on how to accomplish this?
Reply
02/08/2018 at 01:46 PM

---
