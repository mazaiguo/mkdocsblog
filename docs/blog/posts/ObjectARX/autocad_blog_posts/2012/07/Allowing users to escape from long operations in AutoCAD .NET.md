---
title: "Allowing users to escape from long operations in AutoCAD .NET"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "In a long operation, you may want to give your user the option to hit escape to cancel the operation and regain control. Here is some code from a D..."
author: Autodesk
---
# Allowing users to escape from long operations in AutoCAD .NET

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/allowing-users-to-escape-from-long-operations-in-autocad-net.html

## 文章内容

By Stephen Preston
In a long operation, you may want to give your user the option to hit escape to cancel the operation and regain control. Here is some code from a DevNote originally written for AutoCAD 2007-2009, which still works today.
[CommandMethod("loop")]
static public void Loop()
{
  DocumentCollection dm =
    Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager;
  Editor ed = dm.MdiActiveDocument.Editor;
  // Create and add our message filter
  MyMessageFilter filter = new MyMessageFilter();
  System.Windows.Forms.Application.AddMessageFilter(filter);
  // Start the loop
  while (true)
  {
    // Check for user input events
    System.Windows.Forms.Application.DoEvents();
    // Check whether the filter has set the flag
    if (filter.bCanceled == true)
    {
      ed.WriteMessage("\nLoop cancelled.");
      break;
    }
    ed.WriteMessage("\nInside while loop...");
  }
  // We're done - remove the message filter
  System.Windows.Forms.Application.RemoveMessageFilter(filter);
}
  // Our message filter class
public class MyMessageFilter : IMessageFilter
{
  public const int WM_KEYDOWN = 0x0100;
  public bool bCanceled = false;
  public bool PreFilterMessage(ref Message m)
  {
    if (m.Msg == WM_KEYDOWN)
    {
      // Check for the Escape keypress
      Keys kc = (Keys)(int)m.WParam & Keys.KeyCode;
      if (m.Msg == WM_KEYDOWN && kc == Keys.Escape)
      {
        bCanceled = true;
      }
      // Return true to filter all keypresses
      return true;
    }
    // Return false to let other messages through
    return false;
  }
}
  Update 7/30/12:
And here is the VB.NET translation (mostly through automatic translation using DeveloperFusion):
      <CommandMethod("LOOP")>
    Public Shared Sub qqq()
      Dim dm As DocumentCollection =
        Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager
      Dim ed As Editor = dm.MdiActiveDocument.Editor
      ' Create and add our message filter
      Dim filter As New MyMessageFilter()
      System.Windows.Forms.Application.AddMessageFilter(filter)
      ' Start the loop
      While True
        ' Check for user input events
        System.Windows.Forms.Application.DoEvents()
        ' Check whether the filter has set the flag
        If filter.bCanceled = True Then
          ed.WriteMessage(vbLf & "Loop cancelled.")
          Exit While
        End If
        ed.WriteMessage(vbLf & "Inside while loop...")
      End While
      ' We're done - remove the message filter
      System.Windows.Forms.Application.RemoveMessageFilter(filter)
    End Sub
    ' Our message filter class
    Public Class MyMessageFilter
      Implements IMessageFilter
      Public Const WM_KEYDOWN As Integer = &H100
      Public bCanceled As Boolean = False
        Public Function PreFilterMessage1(
      ByRef m As System.Windows.Forms.Message) As Boolean _
      Implements System.Windows.Forms.IMessageFilter.PreFilterMessage
        If m.Msg = WM_KEYDOWN Then
          ' Check for the Escape keypress
          Dim kc As Keys = DirectCast(CInt(m.WParam), Keys) And Keys.KeyCode
          If m.Msg = WM_KEYDOWN AndAlso kc = Keys.Escape Then
            bCanceled = True
          End If
          ' Return true to filter all keypresses
          Return True
        End If
        ' Return false to let other messages through
        Return False
      End Function
    End Class

## 评论

**内容**: David said...
Hello Stephen
I don't think the code works in 2012/ 64 bit.
I had to change it to vb of course. Could you please take a look what is wrong ? Thanks
Public Class LoopCommands
_
Public Shared Sub [Loop]()
Dim dm As DocumentCollection = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager
Dim ed As Editor = dm.MdiActiveDocument.Editor
' Create and add our message filter
Dim filter As New MyMessageFilter()
System.Windows.Forms.Application.AddMessageFilter(CType(filter, System.Windows.Forms.IMessageFilter))
' Start the loop
While True
' Check for user input events
System.Windows.Forms.Application.DoEvents()
' Check whether the filter has set the flag
If filter.bCanceled = True Then
ed.WriteMessage(vbLf & "Loop cancelled.")
Exit While
End If
ed.WriteMessage(vbLf & "Inside while loop...")
End While
' We're done - remove the message filter
System.Windows.Forms.Application.RemoveMessageFilter(CType(filter, System.Windows.Forms.IMessageFilter))
End Sub

' Our message filter class
Public Class MyMessageFilter
Implements IMessageFilter
Public Const WM_KEYDOWN As Integer = &H100
Public bCanceled As Boolean = False
Public Function PreFilterMessage(ByRef m As Message) As Boolean
If m.Msg = WM_KEYDOWN Then
' Check for the Escape keypress
Dim kc As Keys = DirectCast(CInt(m.WParam), Keys) And Keys.KeyCode
If m.Msg = WM_KEYDOWN AndAlso kc = Keys.Escape Then
bCanceled = True
End If
' Return true to filter all keypresses
Return True
End If
' Return false to let other messages through
Return False
End Function
Public Function PreFilterMessage1(ByRef m As System.Windows.Forms.Message) As Boolean Implements System.Windows.Forms.IMessageFilter.PreFilterMessage
End Function
End Class
End Class
Reply
07/27/2012 at 01:01 PM

---
**内容**: Madhukar Moogala said...
I've updated the post with a VB.NET translation. VB.NET and C# versions work fine for me on AutoCAD 2012 64-bit.
Reply
07/30/2012 at 06:14 PM

---
**内容**: Lucano Deskovic said...
hello, I've been using the same principle in trying to block number input in ACAD, but for unknown reason, messagefilter keeps letting first 2 keys "leak through" to the application.
I'm suspecting it could have something to do with paletteset/acad focus(since I'm using a button to enable/disable the feature), but I've exhausted all other options but to ask you for a tip. (been at autodesk forum and stackoverflow).
http://forums.autodesk.com/t5/net/paletteset-keepfocus-and-keyboard-override/m-p/6069569#M47738
http://stackoverflow.com/questions/35977925/c-sharp-message-filter-keeps-leaks-first-2-keys-pressed
Reply
03/13/2016 at 06:20 PM

---
