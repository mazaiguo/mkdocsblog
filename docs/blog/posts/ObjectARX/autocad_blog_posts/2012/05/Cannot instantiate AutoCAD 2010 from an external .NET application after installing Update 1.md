---
title: "Cannot instantiate AutoCAD 2010 from an external .NET application after installing Update 1"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
description: "I'm creating an AutoCAD instance from my external .NET application. It worked fine until I installed Update 1 for AutoCAD 2010. Since then I starte..."
author: Autodesk
---
# Cannot instantiate AutoCAD 2010 from an external .NET application after installing Update 1

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/cannot-instantiate-autocad-2010-from-an-external-net-application-after-installing-update-1.html

## 文章内容

By Adam Nagy
I'm creating an AutoCAD instance from my external .NET application. It worked fine until I installed Update 1 for AutoCAD 2010. Since then I started to get the following error saying "Creating an instance of the COM component with CLSID {6D7AE628-FF41-4CD3-91DD-34825BB1A251} from the IClassFactory failed due to the following error: 80010001"

What could be the problem?
Solution
There was a fix in AutoCAD for a problem which was caused by WPF not letting through some calls under certain scenarios, which now makes it necessary for you to implement IMessageFilter in your external .NET application. In VB6 it is supposed to be done in the background, but .NET does not do it for you. Here is your modified code:
Imports Autodesk.AutoCAD.Interop
Imports Autodesk.AutoCAD.Interop.Common
Imports System.Runtime.InteropServices
  ' SEE http://msdn.microsoft.com/en-us/library/ms693740(VS.85).aspx
' for details
<ComImport(), _
InterfaceType(ComInterfaceType.InterfaceIsIUnknown), _
Guid("00000016-0000-0000-C000-000000000046")> _
Public Interface IMessageFilter
  <PreserveSig()> _
  Function HandleInComingCall( _
    ByVal dwCallType As Integer, _
    ByVal hTaskCaller As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal lpInterfaceInfo As IntPtr) As Integer
  <PreserveSig()> _
  Function RetryRejectedCall( _
    ByVal hTaskCallee As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal dwRejectType As Integer) As Integer
  <PreserveSig()> _
  Function MessagePending( _
    ByVal hTaskCallee As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal dwPendingType As Integer) As Integer
End Interface
  Public Class Form1
  Implements IMessageFilter
    <DllImport("ole32.dll")> _
  Shared Function CoRegisterMessageFilter( _
    ByVal lpMessageFilter As IMessageFilter, _
    ByRef lplpMessageFilter As IMessageFilter) As Integer
  End Function
    Public Sub New()
      ' This call is required by the Windows Form Designer.
    InitializeComponent()
      ' Add any initialization after the InitializeComponent() call.
    Dim oldFilter As IMessageFilter = Nothing
    Dim ret As Integer = CoRegisterMessageFilter(Me, oldFilter)
    End Sub
  #Region "IMessageFilter Members"
    Function HandleInComingCall( _
    ByVal dwCallType As Integer, _
    ByVal hTaskCaller As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal lpInterfaceInfo As IntPtr) As Integer _
  Implements IMessageFilter.HandleInComingCall
      Return 0
  End Function
    Function RetryRejectedCall( _
    ByVal hTaskCallee As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal dwRejectType As Integer) As Integer _
  Implements IMessageFilter.RetryRejectedCall
      ' retry in a second.
    Return 1000
  End Function
    Function MessagePending( _
    ByVal hTaskCallee As IntPtr, _
    ByVal dwTickCount As Integer, _
    ByVal dwPendingType As Integer) As Integer _
  Implements IMessageFilter.MessagePending
      Return 1
  End Function
  #End Region
    Private Sub Form1_FormClosed( _
    ByVal sender As Object, _
    ByVal e As System.Windows.Forms.FormClosedEventArgs) _
      Handles Me.FormClosed
    'objAcad.Quit()
  End Sub
    Private Sub Form1_Load( _
    ByVal sender As System.Object, _
    ByVal e As System.EventArgs) Handles MyBase.Load
    End Sub
    Private Sub Button1_Click( _
    ByVal sender As System.Object, _
    ByVal e As System.EventArgs) Handles Button1.Click
    Dim acType As Type = _
      Type.GetTypeFromProgID("AutoCAD.Application.18")
    Dim objAcad As AcadApplication = _
      System.Activator.CreateInstance(acType)
    objAcad.Visible = True
    objAcad.WindowState = AcWindowState.acMin
    Dim bQuiet As Boolean
    bQuiet = objAcad.GetAcadState.IsQuiescent
    If bQuiet = True Then
      objAcad.Visible = True
      MsgBox("Autocad is quiet")
    Else
      MsgBox("Autocad is not quiet")
    End If
    With objAcad
      MsgBox("Setting single document mode to false")
      .Preferences.System.SingleDocumentMode = False
      MsgBox("Adding a new blank doc")
      .Documents.Add()
      MsgBox("Adding another new blank doc")
      .Documents.Add()
      MsgBox("Beginning loop that closed docs")
      Do While .Documents.Count <> 1
        MsgBox("Closing a document")
        .Documents.Item(1).Close(False)
      Loop
      MsgBox("Finished closing docs")
      End With
  End Sub
    Protected Overrides Sub Finalize()
    MyBase.Finalize()
  End Sub
    Private Sub Button2_Click( _
    ByVal sender As System.Object, _
    ByVal e As System.EventArgs) Handles Button2.Click
    Me.Close()
  End Sub
  End Class

