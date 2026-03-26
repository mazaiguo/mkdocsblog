---
title: "What entities support a non-uniform scale matrix?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Dimension
  - Hatch
  - Polyline
description: "AutoCAD has a number of entity types and you might wonder which entities support non-uniform scaling."
author: Autodesk
---
# What entities support a non-uniform scale matrix?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/what-entities-support-a-non-uniform-scale-matrix.html

## 文章内容

By Gopinath Taget
AutoCAD has a number of entity types and you might wonder which entities support non-uniform scaling.
As a general rule, the AutoCAD built-in entity classes for entity types that existed before R13 (such as AcDbCircle, AcDbLine, AcDbArc, AcDb2dPolyline, etc.) require that the transformation matrix represent a uniformly scaling orthogonal transformation (if it is not, then Acad::eCannotScaleNonUniformly will be returned). Other AutoCAD built-in classes typically does not have this restrictions.
Also, here is more specific information on commonly used AutoCAD entities:
The following are entities that have a scaling restriction:
AcDb2dPolyine, AcDb3dPolyine, AcDbDimension and derived classes, AcDbArc, AcDbCircle, AcDbBlockReference, AcDbMInsert, AcDbFace, AcDbLine, AcDbPloyline, AcDbPoint, AcDbPoint, AcDbHatch, AcDbShape, AcDbText and derived classes, AcDbTrace, AcDbViewport, AcDbRegion, AcDb3dSolid, and AcDbBody.
The entities that support non-uniform scale matrix are:
AcDbLeader, AcDbMLine, AcDbMText, AcDbOle2Frame, AcDbPloyFaceMesh, AcDbPolygonMesh, AcDbRay, AcDbXline, AcDbFcf, AcDbSolid, AcDbEllipse, AcDbSpline, AcDbImage

## 评论

**内容**: Stephen Swift said...
Why can I scale a block non-uniformly using the Insert Dialog Box, but not through the API?
Reply
03/17/2014 at 02:04 PM

---
