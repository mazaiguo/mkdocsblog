---
title: "How to create a new layout and paper space viewport?"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - API
  - AutoCAD
  - VBA
description: "How do I use the AutoCAD VBA API to create a new layout and a new paper space viewport?"
author: Autodesk
---
# How to create a new layout and paper space viewport?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-create-a-new-layout-and-paper-space-viewport.html

## 文章内容

By Daniel Du
Issue
How do I use the AutoCAD VBA API to create a new layout and a new paper space viewport?
Solution
To create a new layout, use the add method of the layouts property of the drawing:
Set lyt = ThisDrawing.Layouts.Add("Test1")
To create a new paper space viewport, use the AddPViewport of the drawing's paper space property:
Set PSVport = ThisDrawing.PaperSpace.AddPViewport(pnt, 5, 4) 
where pnt is the center of the viewport.
One item of which to be aware is that the paper space property of the drawing references the ActiveLayout. The following procedure creates a new layout and paper space viewport on the new layout.
Public Sub NewLayoutAndNewPVport()
    Dim PSVport As AcadPViewport
    Dim lyt As AcadLayout
    Dim pnt(0 To 2) As Double
 
    ' Create a point to be used for the new paperspace viewport
    pnt(0) = 5
    pnt(1) = 5
    pnt(2) = 0
 
    ' Create a new layout
    lyt = ThisDrawing.Layouts.Add("Test1")
 
    ' If a layout named "Test1" already exists comment out
    ' the line above and uncomment this line.
    ' Set lyt = ThisDrawing.Layouts("Test1")
 
    ' Make lyt created above the active layout
    ThisDrawing.ActiveLayout = lyt
 
    ' Create a new paper space viewport notice that you use
    ' the Paperspace property of this drawing. The Paperspace
    ' property references the active layout
    PSVport = ThisDrawing.PaperSpace.AddPViewport(pnt, 5, 4)
 
    ' Make sure the Viewport is displayed and on
    PSVport.Display(True)
    PSVport.ViewportOn = True
 
    ' Before making a pViewport active the mspace property needs
    ' to be True for a floating viewport
    ThisDrawing.MSpace = True
    ThisDrawing.ActivePViewport = PSVport
    ThisDrawing.Regen(acActiveViewport)
 
End Sub

## 评论

**内容**: Tim said...
excelent. thanks
Reply
01/22/2015 at 12:54 PM

---
**内容**: Zouhair said...
How can we set up the paper space. Like the paper size, let say A4 and print format let say Pdf.
Reply
06/13/2020 at 05:44 PM

---
**内容**: Parizer Parizovici said...
Hi,
This vba give me a error 424 on the object lyt(lyt= nothing)
can you explain this type of error?
THX
Reply
01/31/2021 at 01:52 AM

---
