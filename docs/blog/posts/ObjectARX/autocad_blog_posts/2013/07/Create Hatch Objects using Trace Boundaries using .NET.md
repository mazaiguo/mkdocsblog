---
title: "Create Hatch Objects using Trace Boundaries using .NET"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Hatch
  - Polyline
description: "After sweating over some Hatch creation code, I thought I better share with you guys how I solved it."
author: Autodesk
---
# Create Hatch Objects using Trace Boundaries using .NET

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/create-hatch-objects-using-trace-boundaries-using-net.html

## 文章内容

by Fenton Webb
After sweating over some Hatch creation code, I thought I better share with you guys how I solved it.
Here’s what I wanted Hatched:
The way I made it work was, to first get all of the boundary geometry as Polylines using the Editor.TraceBoundary function.
This gave me an array of 3 Polylines, shown in red e.g.
Next, I add the polylines to the Database (temporarily) so that the Hatch object can process them (outside of any Transaction) – sorry VB
dim loopObjectIds = new ObjectIdCollection()
Dim db As Database = Application.DocumentManager.MdiActiveDocument.Database
' add the loop objects to the dwg
For Each polyline As Polyline In loopObjects
  Using curSpace As BlockTableRecord = db.CurrentSpaceId.Open(OpenMode.ForWrite)
    loopObjectIds.Add(curSpace.AppendEntity(polyline))
    ' make sure to close the polyline
    polyline.Close()
  End Using
Next 
Now append each polyline obtained by the trace as a separate loop e.g.
For Each objectId In loopObjectIds
  Dim ids = New ObjectIdCollection()
  ids.Add(objectId)
  acHatch.AppendLoop(HatchLoopTypes.Outermost, ids)
Next
acHatch.EvaluateHatch(True)
That’s it!!
Also, here are the different results obtained by setting the Hatch.HatchStyle to:
HatchStyle.Ignore results in this:
HatchStyle.Outer results in this:
HatchStyle.Normal
results in this:
For the record, I could have used the appendLoop function which takes a Curve2dCollection, however I didn’t on this occasion because I didn’t know that we have equivalent .NET functions to these C++ versions…
acdbConvertAcDbCurveToGelibCurve
acdbConvertGelibCurveToAcDbCurve
acdbAssignGelibCurveToAcDbCurve
in .NET
CreateFromGeCurve
SetFromGeCurve

## 评论

**内容**: Zakir said...
very useful post. Thanks for sharing
Reply
11/12/2013 at 08:41 AM

---
**内容**: JoSko said...
Hi,
I 've been trying to implement your code in c# to get the result you have with HatchStyle.Outer and i can't get it to work. Can you please tell me when do you write the line acHatch.HatchStyle = HatchStyle.Outer ?

Reply
07/21/2019 at 10:23 AM

---
**内容**: Imad Almuzain said...
where is Editor.TraceBoundary in code?
Reply
03/22/2021 at 12:28 AM

---
**内容**: Lima said...
Well, that's very interesting. Thanks for sharing, bro
Reply
04/23/2021 at 05:22 AM

---
