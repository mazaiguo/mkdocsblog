---
title: "Finding Transformation matrix for aligning two entities"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
description: "In AutoCAD API, entities are transformed (Moved / Rotated / Scaled) using transformation matrices."
author: Autodesk
---
# Finding Transformation matrix for aligning two entities

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/finding-transformation-matrix-for-aligning-two-entities.html

## 文章内容

By Balaji Ramamoorthy
In AutoCAD API, entities are transformed (Moved / Rotated / Scaled) using transformation matrices.
Here is a sample code snippet that demonstrates aligning two entities (say two lines oriented in space) by finding the required transformation matrix.
Document activeDoc
= Application.DocumentManager.MdiActiveDocument;
  Database db = activeDoc.Database;
Editor ed = activeDoc.Editor;
  PromptEntityResult per
= ed.GetEntity
(
new PromptEntityOptions("Select an entity : ")
);
  if (per.Status != PromptStatus.OK)
return;
ObjectId oid = per.ObjectId;
  PromptPointResult ppr1
= ed.GetPoint
(
new PromptPointOptions("Select src point 1")
);
  if (ppr1.Status != PromptStatus.OK)
return;
Point3d sp1 = ppr1.Value;
  PromptPointResult ppr2
= ed.GetPoint
(
new PromptPointOptions("Select src point 2")
);
  if (ppr2.Status != PromptStatus.OK)
return;
Point3d ep1 = ppr2.Value;
  PromptPointResult ppr3
= ed.GetPoint
(
new PromptPointOptions("Select dest point 1")
);
  if (ppr3.Status != PromptStatus.OK)
return;
Point3d sp2 = ppr3.Value;
  PromptPointResult ppr4
= ed.GetPoint
(
new PromptPointOptions("Select dest point 2")
);
  if (ppr4.Status != PromptStatus.OK)
return;
Point3d ep2 = ppr4.Value;
  Matrix3d resMat = Matrix3d.Identity;
  Matrix3d trans1 = Matrix3d.Displacement(sp2-sp1);
sp1 = sp1.TransformBy(trans1);
ep1 = ep1.TransformBy(trans1);
resMat = resMat.PreMultiplyBy(trans1);
  // Rotation about Z axis
Vector3d dir1 = ep1 - sp1;
Vector3d dir2 = ep2 - sp2;
Plane xy = new Plane(Point3d.Origin, Vector3d.ZAxis);
Matrix3d trans2
= Matrix3d.Rotation
(
dir2.AngleOnPlane(xy)-dir1.AngleOnPlane(xy),
Vector3d.ZAxis,
sp1
);
sp1 = sp1.TransformBy(trans2);
ep1 = ep1.TransformBy(trans2);
resMat = resMat.PreMultiplyBy(trans2);
  // Rotation about X axis
dir1 = ep1 - sp1;
dir2 = ep2 - sp2;
Plane yz = new Plane(Point3d.Origin, Vector3d.XAxis);
Matrix3d trans3
= Matrix3d.Rotation
(
dir2.AngleOnPlane(yz)-dir1.AngleOnPlane(yz),
Vector3d.XAxis,
sp1
);
sp1 = sp1.TransformBy(trans3);
ep1 = ep1.TransformBy(trans3);
resMat = resMat.PreMultiplyBy(trans3);
  // Rotation about Y axis
dir1 = ep1 - sp1;
dir2 = ep2 - sp2;
Plane xz = new Plane(Point3d.Origin, Vector3d.YAxis);
Matrix3d trans4
= Matrix3d.Rotation
(
dir2.AngleOnPlane(yz)-dir1.AngleOnPlane(xz),
Vector3d.YAxis,
sp1
);
sp1 = sp1.TransformBy(trans4);
ep1 = ep1.TransformBy(trans4);
resMat = resMat.PreMultiplyBy(trans4);
  // Scaling
dir1 = ep1 - sp1;
dir2 = ep2 - sp2;
Matrix3d trans5
= Matrix3d.Scaling
(
dir2.Length / dir1.Length,
sp1
);
sp1 = sp1.TransformBy(trans5);
ep1 = ep1.TransformBy(trans5);
resMat = resMat.PreMultiplyBy(trans5);
  using (Transaction tr
= db.TransactionManager.StartTransaction())
{
Entity ent = (Entity)tr.GetObject(oid, OpenMode.ForWrite);
ent.TransformBy(resMat);
tr.Commit();
}

## 评论

**内容**: Christopher said...
There is an error on this line:
Matrix3d trans4 = Matrix3d.Rotation(dir2.AngleOnPlane(yz)-dir1.AngleOnPlane(xz), Vector3d.YAxis,sp1);
It should be:
Matrix3d trans4 = Matrix3d.Rotation(dir2.AngleOnPlane(xz)-dir1.AngleOnPlane(xz), Vector3d.YAxis,sp1);
Reply
03/23/2020 at 07:29 PM

---
**内容**: Christopher said...
This code doesn't work on correctly in 3d.
https://autode.sk/2y4D51k
To recreate the drawing, here is the 3D Polyline, copy the line to the command line.
3DPoly 652492.7740,367502.1323,2867.9053 652534.3375,367499.4847,2862.0912
Here are the two point locations, copy the points to the command line:
point 652492.7740,367502.1323,2867.9053
point 652534.7389,367499.4590,2867.5313
I'm trying to get help here: https://forums.autodesk.com/t5/net/align-entity-3d/td-p/9395411
Reply
03/23/2020 at 11:35 PM

---
