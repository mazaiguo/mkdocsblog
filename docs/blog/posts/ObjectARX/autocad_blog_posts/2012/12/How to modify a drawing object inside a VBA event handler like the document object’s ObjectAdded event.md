---
title: "How to modify a drawing object inside a VBA event handler like the document object’s ObjectAdded event"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - COM
  - ObjectARX
  - VBA
description: "Consider this: Using WithEvents in VB(A), you are trying to modify an object passed to the document's ObjectAdded, ObjectModified events, or drawin..."
author: Autodesk
---
# How to modify a drawing object inside a VBA event handler like the document object’s ObjectAdded event

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-modify-a-drawing-object-inside-a-vba-event-handler-like-the-document-objects-objectadded-event.html

## 文章内容

By Gopinath Taget
Consider this: Using WithEvents in VB(A), you are trying to modify an object passed to the document's ObjectAdded, ObjectModified events, or drawing object's Modified event. However, this results in Error that look similar to this: "Object was opened for read" or similar. How can you work around this?
Firstly, modifying objects in events such as these is generally not recommended and not worth the trouble you might face later; especially if you are trying to modify objects that are already in the process of being modified. That is rarely a good idea.
However, if you absolutely need to modify objects in event handlers, there are some ways to achieve it.
ActiveX events are modeled on ObjectARX Event handling mechanism (reactors). There are many notifications when object is in an open state (for Read, Write or Notify) so in general, you cannot change it from within the event, evidenced by the fact for instance that the object is passed ByVal to the ObjectAdded event. You can however access any object for write in the CommandEnded event. So, you can set some global flags, trigger them in CommandStart, store ObjectIds during ObjectAdded and use the Ids in CommandEnded to change the relevant objects. For example, the code below will alter any line added to the document. This is the solution specific to VBA. For VB you have additional complexity of attaching events to docs (but that is a topic for another blog post).
Option Explicit
Dim cIDs As New Collection ' collection for line IDs to be modified
Dim bFlag As Boolean   ' flag to indicate when modification needed
Private Sub AcadDocument_BeginCommand(ByVal CommandName As String)   
  ' Here we can set the flag ONLY for particular command. 
  ' For simplicity, set always in this sample 
  bFlag = True 
  Call ClearCollection(cIDs)'Just in case
                            '(done already in EndCommand)
End Sub
Private Sub AcadDocument_ObjectAdded(ByVal Object As Object)   
  If bFlag Then ' If flag on and line - add the ID to the collection
      Dim obj As AcadObject   
      Set obj = Object   
      If obj.ObjectName = "AcDbLine" Then     
          cIDs.Add obj.ObjectID   
      End If
  End If
End Sub
Private Sub AcadDocument_EndCommand(ByVal CommandName As String)   
  ' Set all line start points to origin and color to magenta 
  If bFlag Then
    Dim pntO(0 To 2) As Double   
    pntO(0) = 0#: pntO(1) = 0#: pntO(2) = 0#       
    Dim id As Variant   
    For Each id In cIDs     
      Dim line As AcadLine     
      Set line = ThisDrawing.ObjectIdToObject(id)     
      line.StartPoint = pntO     
      line.Color = acMagenta   
    Next id       
    ' Reset flag and collection   
    bFlag = False   
    Call ClearCollection(cIDs) 
  End If
End Sub
Private Sub ClearCollection(cCol As Collection) 
  Dim iCnt As Long 
  For iCnt = 1 To cCol.Count   
    cCol.Remove 1 ' Since collections are reindexed
                  'automatically, remove the first member 
  Next iCntEnd
End Sub

