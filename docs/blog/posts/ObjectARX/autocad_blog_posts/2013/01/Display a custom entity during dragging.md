---
title: "Display a custom entity during dragging"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Polyline
description: "For a custom entity derived from AcDbEntity, when try to use the polyline() and polygon() primitives of AcGiWorldGeometry inside the worldDraw() fu..."
author: Autodesk
---
# Display a custom entity during dragging

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/display-a-custom-entity-during-dragging.html

## 文章内容

By Augusto Goncalves
For a custom entity derived from AcDbEntity, when try to use the polyline() and polygon() primitives of AcGiWorldGeometry inside the worldDraw() function, in some cases the functions may return a bad error status when used while dragging or modifying grip points.
This error does not produce a crash, but when stop dragging the entity while editing grip points, it’s no possible to see the new transformed/modified entity, only the points. This may cause a lot of inconvenience while scaling or rotating entities using grip points.
These functions return an error to indicate that the operation has been aborted. AutoCAD aborts the draw operation if the user continues to drag your entity, based on the ACAD variables DRAGP1 and DRAGP2. To see your entity more detailed during dragging, it’s possible to increase these two variables (you should try to set DRAGP1 to 100 and DRAGP2 to 250).
Note: When you can't see your entity when you stop dragging, then several parts of your entity might overlap. Since we use XOR to draw an entity during draggen, two vectors on top of each other are not visible (the first XOR operation displays the vector, and the second XOR operation makes it invisible again).

