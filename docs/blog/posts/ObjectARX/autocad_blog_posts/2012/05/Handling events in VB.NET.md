---
title: "Handling events in VB.NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
description: "I found a C# sample project called EventsWatcher, but I'm not sure how to do similar event handling in VB.NET"
author: Autodesk
---
# Handling events in VB.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/handling-events-in-vbnet.html

## 文章内容

By Adam Nagy
I found a C# sample project called EventsWatcher, but I'm not sure how to do similar event handling in VB.NET
Solution
In VB.NET you can handle events in two ways:
1) The VB6 way:
declare a variable with WithEvents keyword
set it to the object which provides the events
select the variable in the combo box on the left side (A) above the coding area, then select the event you want to handle in the combo box on the right side (B)

2) The .NET way / handling a specific event
define a function you want to handle the event with, e.g. OnDocumentDestroyed
create a delegate for the function, e.g. New DocumentDestroyedEventHandler(AddressOf OnDocumentDestroyed)
use AddHandler to add the delegate as one of the handlers of the specific event
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.ApplicationServices
  Public Class MyClass1 
    ' VB style 
  Private Shared WithEvents docEvents As DocumentCollection 
    Private Shared Sub docEvents_DocumentCreated(
    ByVal sender As Object, ByVal e As DocumentCollectionEventArgs) _
    Handles docEvents.DocumentCreated   
      MsgBox(e.Document.Name & " opened") 
  End Sub 
    ' .NET style 
  Private Shared docDestroyedEvent As DocumentDestroyedEventHandler 
    Public Shared Sub OnDocumentDestroyed(
    ByVal sender As Object, ByVal e As DocumentDestroyedEventArgs)
      MsgBox(e.FileName & " closed") 
  End Sub 
    <CommandMethod("StartEventHandling")> _ 
  Public Sub Asdkcmd1()   
    ' Start VB Style handling – all docEvents related event
    ' handling is started    
    docEvents = Application.DocumentManager   
      ' Start .NET style handling – only this specific event
    ' handling is started   
    Dim docs As DocumentCollection = Application.DocumentManager  
    If docDestroyedEvent Is Nothing Then     
      docDestroyedEvent =
        New DocumentDestroyedEventHandler(
          AddressOf OnDocumentDestroyed)     
      AddHandler docs.DocumentDestroyed, docDestroyedEvent   
    End If 
  End Sub 
    <CommandMethod("StopEventHandling")> _ 
  Public Sub Asdkcmd2()   
    ' Stop VB style handling – all docEvents related event handling
    ' is stopped   
    docEvents = Nothing  
      ' Stop .NET style handling – only this specific event handling
    ' is stopped   
    Dim docs As DocumentCollection = Application.DocumentManager   
    If Not docDestroyedEvent is Nothing Then      
      RemoveHandler docs.DocumentDestroyed, docDestroyedEvent     
      docDestroyedEvent = Nothing   
    End If   
  End Sub
End Class
In VB.NET “Shared” is the C#/C++ equivalent of “static”, which means that the same instance of the variable will be available for all instances of the container class.
You find this being used in the EventsWatcher sample as well. It’s needed, because otherwise a new instance of MyClass1 would be created for each document.
So without this “Shared” keyword, each document in which you called “StartEventHandling” would start running its own event handler.

## 评论

**内容**: Matus Brlit said...
is it necessary to create an explicit delagate?
I would use just this:
Dim docs As DocumentCollection = Application.DocumentManager
AddHandler docs.DocumentDestroyed, AddressOf docDestroyedEvent
Reply
06/01/2012 at 04:52 AM

---
**内容**: Adam Nagy said in reply to Matus Brlit...
Thanks for the comment, Matus.
No, as far as I know it's not necessary.
In this case I just used it to track if we subscribed to the event already (If docDestroyedEvent Is Nothing Then)
Reply
06/01/2012 at 07:00 AM

---
