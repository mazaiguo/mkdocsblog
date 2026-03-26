---
title: "Catch WM_ACTIVATEAPP messages of AutoCAD"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I would like to be notified when AutoCAD gets activated/deactivated so I could measure how much time the user spends on it. I tried using System.Wi..."
author: Autodesk
---
# Catch WM_ACTIVATEAPP messages of AutoCAD

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/catch-wm_activateapp-messages-of-autocad.html

## 文章内容

By Adam Nagy
I would like to be notified when AutoCAD gets activated/deactivated so I could measure how much time the user spends on it. I tried using System.Windows.Forms.IMessageFilter, but that only seemed to work while debugging AutoCAD and in case of using acedRegFilterWinMsg()/acedRegisterWatchWinMsg() the WM_ACTIVATEAPP message was not sent. Is there a way to achieve what I need?
Solution
You could subclass the AutoCAD window, in which case you can catch all the windows events it gets.
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.EditorInput
  Public Class Class1
  <CommandMethod("GetAppEvents")> _
  Public Shared Sub GetAppEvents()
      SubClassWindow(Application.MainWindow.Handle)
  End Sub
    Delegate Function WindowProcDelegate( _
    ByVal hwnd As IntPtr, ByVal msg As Integer, _
    ByVal wParam As Integer, ByVal lParam As Integer) As Integer
    Declare Function SetWindowLong32 Lib "USER32.DLL" _
      Alias "SetWindowLongA" _
      (ByVal hwnd As IntPtr, ByVal attr As Integer, _
       ByVal lVal As WindowProcDelegate) As IntPtr
    Declare Function SetWindowLong64 Lib "USER32.DLL" _
      Alias "SetWindowLongPtrA" _
      (ByVal hwnd As IntPtr, ByVal attr As Integer, _
       ByVal lVal As WindowProcDelegate) As IntPtr
    Public Shared Function SetWindowLong( _
      ByVal hWnd As IntPtr, ByVal nIndex As Integer, _
      ByVal dwNewLong As WindowProcDelegate) As IntPtr
      If IntPtr.Size = 8 Then
      Return SetWindowLong64(hWnd, nIndex, dwNewLong)
    Else
      Return SetWindowLong32(hWnd, nIndex, dwNewLong)
    End If
  End Function
    Declare Function CallWindowProc Lib "USER32.DLL" _
      Alias "CallWindowProcA" _
      (ByVal lpPrevWndFunc As IntPtr, ByVal hWnd As IntPtr, _
      ByVal Msg As Integer, ByVal wParam As IntPtr, _
      ByVal lParam As IntPtr) As Integer
    Public Shared myWindowProcDelegate As WindowProcDelegate = _
    New WindowProcDelegate(AddressOf SubClassProc)
    Public Shared prevProcPtr As IntPtr = IntPtr.Zero
    Public Shared Function SubClassProc( _
    ByVal hwnd As IntPtr, ByVal msg As Integer, _
    ByVal wParam As IntPtr, ByVal lParam As IntPtr) As Integer
      'WM_ACTIVATEAPP = &H1C
    If msg = &H1C Then
      Dim doc As Document =
        Application.DocumentManager.MdiActiveDocument
        If Not doc Is Nothing Then
        'if wParam is 0, then the application got deactivated
        If wParam = 0 Then
          doc.Editor.WriteMessage( _
              "AutoCAD got deactivated..." + vbCrLf)
        Else
          doc.Editor.WriteMessage( _
              "AutoCAD got activated..." + vbCrLf)
        End If
      End If
    End If
      Return CallWindowProc(prevProcPtr, hwnd, msg, wParam, lParam)
  End Function
    Public Shared Sub SubClassWindow(ByVal hwnd As IntPtr)
      If prevProcPtr = IntPtr.Zero Then
      'GWL_WNDPROC = (-4)
      prevProcPtr = SetWindowLong(hwnd, -4, myWindowProcDelegate)
    End If
  End Sub
End Class

## 评论

**内容**: Owen Wengerd said...
It should be noted that this code only works in 32-bit AutoCAD.
Reply
05/28/2012 at 08:36 AM

---
**内容**: Adam Nagy said...
Thanks for the comment, Owen.
I've updated the code to work on 64 bit OS as well.
Reply
05/29/2012 at 05:57 AM

---
