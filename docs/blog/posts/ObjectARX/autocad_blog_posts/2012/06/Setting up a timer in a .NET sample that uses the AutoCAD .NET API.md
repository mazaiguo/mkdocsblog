---
title: "Setting up a timer in a .NET sample that uses the AutoCAD .NET API"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Plugin
description: "If you want your AutoCAD .NET plug-in to perform some tasks at regular intervals, then it is important to ensure that the timer runs in the AutoCAD..."
author: Autodesk
---
# Setting up a timer in a .NET sample that uses the AutoCAD .NET API

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-up-a-timer-in-a-net-sample-that-uses-the-autocad-net-api.html

## 文章内容

By Balaji Ramamoorthy
 If you want your AutoCAD .NET plug-in to perform some tasks at regular intervals, then it is important to ensure that the timer runs in the AutoCAD's main UI thread. Implementing the timer in a separate thread does not work because AutoCAD (atleast until 2013 release) does not support multithreaded applications.
To setup a timer to work properly, one possible way is to use a hidden modeless window that in-turn instantiates a timer (use the System.Windows.Forms.Timer). The System.Windows.Forms.Timer differs from the other timers provided by the .Net framework and is guranteed to run in the same UI thread which started it. For a comparison of the various timers available in the .Net framework, you may refer to this MSDN magazine article.
Here is the sample code that displays a tray bubble at a specified time interval :
First lets look at the commands class
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.EditorInput
Imports Autodesk.AutoCAD.Windows
  <Assembly: CommandClass(GetType(AdskMyTimerClass))>
  Public Class AdskMyTimerClass
    Implements IExtensionApplication
      'System.Threading.Timer is a simple, lightweight timer that
    'uses callback methods and is served by thread pool threads.
    'It is not recommended for use with Windows Forms, because
    'its callbacks do not occur on the user interface thread.
      'System.Windows.Forms.Timer is a better choice for use with
    'Windows Forms and its callbacks occur on the same UI thread.
    Private _timerForm As MyForm
      Public Sub Initialize() _
        Implements IExtensionApplication.Initialize
        _timerForm = Nothing
    End Sub
      Public Sub Terminate() _
        Implements IExtensionApplication.Terminate
        StopTimerMethod()
    End Sub
      <CommandMethod("StartTimer")> _
    Public Sub StartTimerMethod()
        If _timerForm Is Nothing Then
            _timerForm = New MyForm
            _timerForm.Show()
            _timerForm.Hide()
        End If
    End Sub
      <CommandMethod("StopTimer")> _
    Public Sub StopTimerMethod()
        If _timerForm IsNot Nothing Then
            _timerForm.Close()
            _timerForm.Dispose()
            _timerForm = Nothing
        End If
    End Sub
End Class
Now for the Form class that creates the timer :
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.EditorInput
Imports Autodesk.AutoCAD.Windows
  Public Class MyForm
      Private _myTimer As System.Windows.Forms.Timer
    Private _ti As TrayItem
    Private _icon As System.Drawing.Icon
    Private _cnt As Int32
      Private Sub MyForm_Load( _
            ByVal sender As System.Object, _
         ByVal e As System.EventArgs) _
         Handles MyBase.Load
        _myTimer = New System.Windows.Forms.Timer()
        _myTimer.Enabled = True
        _myTimer.Interval = 5000
        AddHandler _myTimer.Tick, AddressOf MyBubbleTimer_Tick
        _myTimer.Start()
    End Sub
      Private Sub MyBubbleTimer_Tick( _
            ByVal sender As System.Object, _
            ByVal e As System.EventArgs
                                    )
        _cnt = _cnt + 1
          Dim sb As StatusBar = Application.StatusBar
        Dim tis As TrayItemCollection = sb.TrayItems
          If _ti Is Nothing Then
            _cnt = 1
            _ti = New TrayItem()
            _ti.Visible = True
            _icon = New System.Drawing.Icon("C:\\Temp\\spintest.ico")
            _ti.Icon = Icon
            _ti.ToolTipText = "My Timer trigerred bubble !"
            tis.Add(_ti)
            sb.Update()
        End If
          _ti.CloseBubbleWindows()
          Dim bubble As New TrayItemBubbleWindow()
        bubble.Text = "Hello !"
        bubble.Title = String.Format("{0}", _cnt)
        bubble.HyperLink = "http://www.autodesk.com"
        bubble.HyperText = "Autodesk"
          _ti.ShowBubbleWindow(bubble)
    End Sub
      Private Sub MyForm_FormClosed( _
            ByVal sender As System.Object, _
            ByVal e As System.Windows.Forms.FormClosedEventArgs _
            ) Handles MyBase.FormClosed
        ' Stop the timer
        _myTimer.Stop()
        _myTimer.Dispose()
          ' Remove the tray item
        If _ti IsNot Nothing Then
            Dim sb As StatusBar = Application.StatusBar
            Dim tis As TrayItemCollection = sb.TrayItems
            tis.Remove(_ti)
            sb.Update()
        End If
    End Sub
End Class

## 评论

**内容**: Maxence said...
Why create an hidden form ? You can use a System.Windows.Form.Timer without a parent form?
Reply
10/16/2012 at 04:15 AM

---
**内容**: Balaji said...
Thanks for pointing that out.
Yes, I think that should also work correctly.
Reply
10/17/2012 at 05:46 AM

---
**内容**: yadwad said...
Hi Balaji
Can you list out the libraries for this code. It will be help full
Reply
11/06/2014 at 01:55 PM

---
