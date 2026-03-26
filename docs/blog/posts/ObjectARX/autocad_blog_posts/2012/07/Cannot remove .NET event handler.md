---
title: "Cannot remove .NET event handler"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "When my AddIn is loaded it starts listening to the DocumentToBeDestroyed event and it works fine."
author: Autodesk
---
# Cannot remove .NET event handler

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/cannot-remove-net-event-handler.html

## 文章内容

By Adam Nagy
When my AddIn is loaded it starts listening to the DocumentToBeDestroyed event and it works fine.
However, when later on I try to stop listening to this event I do not succeed and so my handler keeps getting called.
Here is my code:
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
  Public Class Commands
  Implements IExtensionApplication
    Public Sub Initialize() Implements IExtensionApplication.Initialize
    AddHandler _
      Application.DocumentManager.DocumentToBeDestroyed, _
      AddressOf docBeginDocClose
  End Sub
    Public Sub Terminate() Implements IExtensionApplication.Terminate
  End Sub
    Public Sub docBeginDocClose( _
    ByVal senderObj As Object, _
    ByVal docColDocActEvtArgs As DocumentCollectionEventArgs)
      System.Diagnostics.Debug.Print("in docBeginDocClose")
  End Sub
    <CommandMethod("StopEvent")> _
  Public Sub StopEvents()
    Try
      RemoveHandler _
        Application.DocumentManager.DocumentToBeDestroyed, _
        AddressOf docBeginDocClose
    Catch ex As Exception
      MsgBox("Error: " & ex.Message)
    End Try
  End Sub
  End Class
Solution
AutoCAD creates an instance of the class that contains the Initialize() function. If the command function is an instance function (not static/shared), then AutoCAD also creates a new instance of the class that contains that function for each document. If the handler is an instance function as well, then you'll get the instance of it that belongs to the same class instance as the command handler.
So you attach one instance’s function to the event inside Initialize() or a command, then you try to remove another instance’s function later on – so you do not remove the function that you attached to the event in the first place.
That’s why your handler keeps being called even after you tried to remove it.
Based on the above, the solution is to simply make the function static (C#) / Shared (VB.NET):
Public Shared Sub docBeginDocClose( _
  ByVal senderObj As Object, _
  ByVal docColDocActEvtArgs As DocumentCollectionEventArgs)
    System.Diagnostics.Debug.Print("in docBeginDocClose")
End Sub

## 评论

**内容**: 王磊 said...
解决了我的问题，谢谢！
Reply
09/11/2015 at 01:22 AM

---
