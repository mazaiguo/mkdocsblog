---
title: "Getting osnapped object's ID"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Consider this: You need to find out after calling acedGetPoint() whether the point returned was osnapped to some geometry, and if it was osnapped, ..."
author: Autodesk
---
# Getting osnapped object's ID

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/getting-osnapped-objects-id.html

## 文章内容

By Gopinath Taget
Consider this: You need to find out after calling acedGetPoint() whether the point returned was osnapped to some geometry, and if it was osnapped, to get ID of the entity it was osnapped to. How can I achieve this?
To do this, you are going to have to use the AcEdInputPointMonitor reactor class. Use the ObjectARX Wizard to create an implementation of this reactor class. Here's some pseudo code for your implementation of the monitorInputPoint() reactor method:
///////////////////////////////////////////////////////////////////
Acad::ErrorStatus asdkInputClosestPoint::monitorInputPoint(......)
{
 // if osnap mode is on
 if (history & Acad::PointHistory::ePickMask)
{
  // get any entities that have been used to calculate an osnap
  int keyPointLength = keyPointEntities.length ();
  // if entities have been used to calculate an osnap point
  if (keyPointLength)
  {
   // now we have the entities used for the osnap calc
   // the computedPoint gives us the snap point
     // you can iterate keyPointEntities array to get the
   // object Id's of snapped entities
  }
}
   return Acad::eOk;
}

## 评论

**内容**: Selevkos said...
Please provide us c# equivalent if it is possible?
Reply
08/08/2013 at 01:55 PM

---
