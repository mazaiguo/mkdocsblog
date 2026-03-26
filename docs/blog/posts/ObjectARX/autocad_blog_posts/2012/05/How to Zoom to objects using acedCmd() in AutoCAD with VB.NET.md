---
title: "How to Zoom to objects using acedCmd() in AutoCAD with VB.NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "For a change, I thought I’d post some VB.NET code which utilizes acedCmd(). You know, I grew up on acedCommand() back when the original C ADS API w..."
author: Autodesk
---
# How to Zoom to objects using acedCmd() in AutoCAD with VB.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-zoom-to-objects-using-acedcmd-in-autocad-with-vbnet.html

## 文章内容

by Fenton Webb
For a change, I thought I’d post some VB.NET code which utilizes acedCmd(). You know, I grew up on acedCommand() back when the original C ADS API was released back in R11 and I have to say, I still love its power and simplicity…
    ' zoom to selected entities using acedCmd
    ' by Fenton Webb, DevTech, Autodesk 09/May/2012
    ' (using full namespaces in VB.NET)
    <CommandMethod("ZoomToEnts")>
    Public Sub ZoomToEnts()
      ' get the autocad editor instance
      Dim ed As Autodesk.AutoCAD.EditorInput.Editor = _
      Autodesk.AutoCAD.ApplicationServices. _
      Application.DocumentManager.MdiActiveDocument.Editor
      ' get a select set of entities in the dwg window
      Dim selection As PromptSelectionResult = ed.GetSelection()
      ' if the selection was successful
      If selection.Status = PromptStatus.OK Then
        ' create a new .NET resbuf struct
        Dim rbCommand As New Autodesk.AutoCAD.DatabaseServices.ResultBuffer
        ' create the buildlist
        rbCommand.Add( _
        New Autodesk.AutoCAD.DatabaseServices.TypedValue(5005, "_ZOOM")) ' RTSTR
        rbCommand.Add( _
        New Autodesk.AutoCAD.DatabaseServices.TypedValue(5005, "_o")) ' RTSTR
        ' in old ADS you could send an RTPICKS 5007 which was an ename selection
        ' set but I found iterating the objectIds much easier than trying to work
        ' out an old style ename ss from a .NET SelectionSet
        Dim id As ObjectId
        For Each id In selection.Value.GetObjectIds()
          rbCommand.Add( _
          New Autodesk.AutoCAD.DatabaseServices.TypedValue(5006, id)) ' RTENAME
        Next
        ' exit out of entity selection
        rbCommand.Add( _
        New Autodesk.AutoCAD.DatabaseServices.TypedValue(5005, "")) ' RTSTR
        ' now call the zoom to objects command
        acedCmd(rbCommand.UnmanagedObject)
      End If
    End Sub
  Updated May 10th 2012 to add additional line breaks (to prevent code being truncated on blog).

## 评论

**内容**: Kerry Brown said...

Fenton,
You may need to show the DllImport definition for acedCmd for 2013 and prior to 2013
... If my memory is correct.
Regards
Reply
05/09/2012 at 03:14 AM

---
**内容**: Account Deleted said...
Kerry! Fenton declare acedCmd in http://adndevblog.typepad.com/autocad/2012/04/synchronously-send-and-wait-for-commands-in-autocad-using-c-net.html
Reply
05/09/2012 at 03:20 AM

---
**内容**: Fenton Webb said...
Here's the VB.NET declaration for acedCmd() (with namespaces) - sorry everyone :-)
_
Public Function acedCmd(vlist As System.IntPtr) As Integer
End Function
Reply
05/09/2012 at 03:22 AM

---
**内容**: Fenton Webb said...
"lessThanSymbol" System.Runtime.InteropServices.DllImport("acad.exe", CallingConvention:=System.Runtime.InteropServices.CallingConvention.Cdecl, EntryPoint:="acedCmd")"greaterThanSymbol" _
Public Function acedCmd(vlist As System.IntPtr) As Integer
End Function
Reply
05/09/2012 at 03:24 AM

---
**内容**: Fenton Webb said...
oh how annoying, you can't use the lessThan/GreaterThan symbols... :-S
Reply
05/09/2012 at 03:24 AM

---
**内容**: Kerry Brown said...

@Alexander,
I was thinking more of the servicing casual reader who may not realize that the definition is needed ...
Regards
Reply
05/09/2012 at 03:28 AM

---
**内容**: Account Deleted said...
Fenton!
>>oh how annoying, you can't use the lessThan/GreaterThan symbols...
This is not the only bug engine of this blog. Check the ends of long lines of code "eaten". This is horrible!
Reply
05/09/2012 at 03:42 AM

---
**内容**: Gaston Nunez said...
Hi,
Just to honor the history, ADS API was first released with R10 for OS/2.
Gaston Nunez
Reply
05/09/2012 at 04:12 PM

---
**内容**: Account Deleted said...
>>ADS API was first released with R10 for OS/2.
And functions has prefix ads_ (i.e. ads_command, ads_cmd, etc...)
Reply
05/09/2012 at 10:09 PM

---
**内容**: SummerNight said...
Hi Fenton,
I am trying to do a similar thing using JavaScript. I have a webpage with a dwf map embedded on it. I get some variables using a GET method from another form/page and I parse that info variables. These variables work as the Object id's for the object I want to select inside the map. Right now, the selection works but I can't zoom into the selected object. Since its a huge map I need some kind of flag to notify where the object resides. Here's a link to the code I have so far: http://pastebin.com/zy8NW1ey
Reply
07/15/2013 at 09:04 AM

---
