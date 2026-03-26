---
title: "Removing all custom handlers of an event"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "In some scenarios, we may add more than one handler for a specific event. In this case, AutoCAD will throw it several times. Imagine a code like th..."
author: Autodesk
---
# Removing all custom handlers of an event

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/removing-all-custom-handlers-of-an-event.html

## 文章内容

By Augusto Goncalves
In some scenarios, we may add more than one handler for a specific event. In this case, AutoCAD will throw it several times. Imagine a code like the one below, where for the Document object we add 2 handlers duplicated, and another different.
<CommandMethod("addEvents")> _
Public Sub CmdCheckEvents()
  ' get the document collection
  ' and add a few handlers
  Dim doc As Document = Application. _
    DocumentManager.MdiActiveDocument
    ' add handler 1
  AddHandler doc.CommandEnded, _
    AddressOf CustomCommandEnded1
  ' duplicate handler 1
  AddHandler doc.CommandEnded, _
    AddressOf CustomCommandEnded1
    ' add handler 2
  AddHandler doc.CommandEnded, _
    AddressOf CustomCommandEnded2
End Sub
  ' handler 1
Private Sub CustomCommandEnded1(sender As Object, _
                                e As CommandEventArgs)
  Application.DocumentManager.MdiActiveDocument. _
    Editor.WriteMessage("CMDEND_1")
End Sub
  ' handler 2
Private Sub CustomCommandEnded2(sender As Object, _
                                e As CommandEventArgs)
  Application.DocumentManager.MdiActiveDocument _
    .Editor.WriteMessage("CMDEND_2")
End Sub
As a result, the event will trigger duplicated for the handler 1 and again for the handler 2.
With .NET we can get the list of events and manipulate it using Reflection. This is not very direct, but can be achieved with the following code. Note that we have to be carefully to not remove handlers from other plug-ins, so skip those not defined on the current assembly.
<CommandMethod("removeEvents")> _
Public Sub CmdRemoveEvents()
  Dim doc As Document = Application. _
    DocumentManager.MdiActiveDocument
  RemoveHandlers(doc, "CommandEnded")
End Sub
  Public Sub RemoveHandlers(obj As Object, eventName As String)
  ' type of the object
  Dim docType As Type = obj.GetType()
    ' get the event info
  Dim eventInfo As EventInfo = docType.GetEvent(eventName)
    ' get all fields
  Dim fields() As FieldInfo = docType.GetFields(
    BindingFlags.Instance Or _
    BindingFlags.Static Or _
    BindingFlags.NonPublic Or _
    BindingFlags.Public)
    ' find the field with the name we seek with LINQ.
  ' this assumes that the respective field has
  ' a name similar to the event
  ' e.g. CommandEnded field is m_pCommandEndedEvent
  Dim eventFields As Object = From f In fields _
                              Where f.Name.Contains(eventInfo.Name) _
                              Select f
  ' get the field from the selection (first)
  Dim eventField As FieldInfo = Nothing
  For Each f In eventFields
    eventField = f
  Next
  ' in case nothing was found...
  If (eventField Is Nothing) Then Exit Sub
    ' now the value of the field
  Dim eventDelegate As [Delegate] = eventField.GetValue(obj)
    ' finally all the handlers added to the event
  Dim handlers As [Delegate]() = eventDelegate.GetInvocationList()
    ' iterate through the collection of handlers
  For Each handler As [Delegate] In handlers
      ' get the type of the handler, so we can skip internal handlers
    Dim handlerType As Type = handler.Target.GetType()
    ' only handlers defined on this custom assembly
    If (handlerType.Assembly = _
        System.Reflection.Assembly. _
        GetExecutingAssembly()) Then
        ' finally remove the handler
      eventInfo.RemoveEventHandler(obj, handler)
    End If
  Next
End Sub

## 评论

**内容**: Tony Tanzillo said...
"' get the type of the handler, so we can skip internal handlers
Dim handlerType As Type = handler.Target.GetType()
' only handlers defined on this custom assembly
If (handlerType.Assembly.FullName = _
System.Reflection.Assembly. _
GetExecutingAssembly().FullName) Then
"
If the two assemblies are the same assembly, they can be directly compared with the equals operator.
Reply
04/16/2013 at 04:54 AM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Thanks Tony, that is better.
Hope this code was useful.
Regards,
Augusto Goncalves
Reply
04/16/2013 at 07:20 AM

---
**内容**: Fernando said...
Hello Augusto, this is Fernando from Mexico greeting you.
I have tried your interesting code in a home project where I would like
to cancel the events of another command that my drawing entities can read
(through lisp for example), I have loaded your code after another container
of events, I have ordered Remover and it is then when this fatal error arises:
Unhandled Access Violation. Reading 0x0000 Exception at a292c02h.
What am I doing wrong?
Any solution would be apretiated.
Thanks in advance.
Reply
01/15/2019 at 08:54 AM

---
**内容**: Augusto Goncalves said in reply to Fernando...
This sample code should track events on the .NET environment, that's probaly why you are getting those errors (due the LISP events)
Reply
01/18/2019 at 11:15 AM

---
**内容**: Fernando said...
Thanks Augusto for yur answer but, I tried with RemoveHandlers(doc, "CommandEnded") and I have failed. I notice that the events handlers coming from command methods are persistent regardless of whether they were loaded before or after your assembly.
I wish i had could make a list of RemoveHandlers(doc, "EventName1")
RemoveHandlers(doc, "EventName2"), etc
Thanks in advance.
Reply
01/22/2019 at 09:35 PM

---
