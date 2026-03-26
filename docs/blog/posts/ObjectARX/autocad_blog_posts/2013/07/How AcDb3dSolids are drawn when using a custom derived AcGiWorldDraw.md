---
title: "How AcDb3dSolids are drawn when using a custom derived AcGiWorldDraw"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
  - Solid
description: "It is possible to create your own custom WorldDraw and ViewportDraw classes (in ObjectARX they are called AcGiWorldDraw and AcgiViewprtDraw). By do..."
author: Autodesk
---
# How AcDb3dSolids are drawn when using a custom derived AcGiWorldDraw

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/how-acdb3dsolids-are-drawn-when-using-a-custom-derived-acgiworlddraw.html

## 文章内容

by Fenton Webb
It is possible to create your own custom WorldDraw and ViewportDraw classes (in ObjectARX they are called AcGiWorldDraw and AcgiViewprtDraw). By doing this, you can essentially override the low level draw routines that AutoCAD uses and replace them with your own functions which can be used to work out the primitive geometrical object data that is being drawn.

A good example of how this works can be found in the ObjectARX sample called acgisamp.
If you are wondering how AcDb3dSolids (Solid3d in .NET) draw themselves, and which primitive draw functions inside of your custom AcGiWorldDraw are called and when, here’s the answer:
AcDb3dSolid::WorldDraw() is called, the solid geometry history worldDraw is called (internal AcDbShHistory::worldDraw()).
From the internal AcDbShHistory::worldDraw() each node in the solid 3d history is obtained and the primative objects are called one by one via their worldDraw() (internal AcDbShPrimitive::WorldDraw())
From the internal AcDbShPrimitive::WorldDraw() the body of the primitive is drawn by drawing each graphics representation in turn... The order is:

For a regen type of kAcGiHideOrShadeCommand or kAcGiShadedDisplay

1) Draws the face edges depending on the edge type, Line or Tessellated yields a geometry.polyline(), Circle or Arc yields a geometry.circle() or geometry.circularArc()
2) Draws the wire edges depending on the edge type as in (1)
3) Draws the body points using geometry.polypoint()

For a regen type of kAcGiStandardDisplay, kAcGiSaveWorldDrawForR12 or kAcGiSaveWorldDrawForProxy

1) Draws the face edges depending on the edge type, Line or Tessellated yields a geometry.polyline(), Circle or Arc yields a geometry.circle() or geometry.circularArc()
2) Draws the wire edges depending on the edge type as in (1)
3) If SPLFRAME=1 then the spline and spline-fit polylines are drawn using geometry.polyline()
4) Draw the iso line edges, if necessary , depending on the edge type as in (1)
5) Draws the body points using geometry.polypoint()

## 评论

**内容**: Audun Opdal said...
Thank you for posting this.
I can't find the acgisamp project in the ObjectARX 2014 download. Where do I find it?
Reply
08/05/2013 at 03:22 AM

---
**内容**: Subir Dutta said...
I see the shell example in ObjectARX SDK. We have to create the list of vertices and faces and send it to the shell api.
As in block we can add comple solid using boolean operations, isn't there any easy way to create complex 3D custom entity using boolean operation where we simple add 3D solid primitives and do boolean on them ?
Is there any sample on similar path ?
Reply
11/10/2015 at 06:27 AM

---
