---
title: "acreEntityToFaces normals on polygon mesh"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Solid
  - Surface
description: "The normal represents the normal of the surface, of which the facet is an approximation. When facetting AcDb3dSolids, the facets may lie on curved ..."
author: Autodesk
---
# acreEntityToFaces normals on polygon mesh

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/acreentitytofaces-normals-on-polygon-mesh.html

## 文章内容

By Augusto Goncalves
The normal represents the normal of the surface, of which the facet is an approximation. When facetting AcDb3dSolids, the facets may lie on curved surfaces. Certain algorithms require the exact normal at the facet vertex, so they can produce more realistic renderings.
The PolygonMesh object does not represent an exact solid. A normal cannot therefore be calculated at the facet vertex. ( There is no surface on which to calculate the normal ).
Assuming that the polygon mesh is used to represent some solid object, then it may be appropriate to use the average normal of all the facets around that vertex. If the normals are used to affect a rendered image, this would show sharp edges as rounded. It would therefore be useful to have a minimum angular turn that a facet edge could have. If the angle between adjacent facets were greater than this tolerance, then each facet would retain its own normal, so the edge looked sharp.

