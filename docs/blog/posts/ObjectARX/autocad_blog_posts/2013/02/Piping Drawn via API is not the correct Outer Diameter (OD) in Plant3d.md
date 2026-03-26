---
title: "Piping Drawn via API is not the correct Outer Diameter (OD) in Plant3d"
date: 2013-02-01
categories:
  - Plant 3D
tags:
  - API
  - C++
  - Plant 3D
description: "Use the sample project CreatePipeline from the Plant 3D 2013 SDK to draw piping in a model. It draws a 6" CS300 line. Next, put in a piece of pipe ..."
author: Autodesk
---
# Piping Drawn via API is not the correct Outer Diameter (OD) in Plant3d

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/piping-drawn-via-api-is-not-the-correct-outer-diameter-od-in-plant3d.html

## 文章内容

by Fenton Webb
Issue
Use the sample project CreatePipeline from the Plant 3D 2013 SDK to draw piping in a model. It draws a 6" CS300 line. Next, put in a piece of pipe using the buttons on ribbon.
The pipe drawn through Plant 3D routing is the correct OD. However, the same Pipe drawn using the SDK is the nominal diameter. What is the problem here?
Solution
The managed Pipe entity has a property OuterDiameter that calls into the unmanaged C++ AcPpDb3dPipe::GetOuterDiameter() / AcPpDb3dPipe::SetOuterDiameter(). You have to set this value using the Pipe’s SpecPart and MatchingPipeOD property.
For example:
pipeEntity.OuterDiameter = pipeSpecPart.PropValue(“MatchingPipeOD”);

## 评论

**内容**: qxzhu said...
The pipe drawn through Plant 3D routing can auto add bend.how to auto add bend by using SDK.
Reply
03/04/2013 at 07:41 PM

---
