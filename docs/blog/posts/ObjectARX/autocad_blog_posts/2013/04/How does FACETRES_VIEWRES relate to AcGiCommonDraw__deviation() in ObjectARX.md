---
title: "How does FACETRES/VIEWRES relate to AcGiCommonDraw::deviation() in ObjectARX"
date: 2013-04-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Can you please explain in detail how the FACETRES and VIEWRES relate to the deviation() in the AcGiCommonDraw class?"
author: Autodesk
---
# How does FACETRES/VIEWRES relate to AcGiCommonDraw::deviation() in ObjectARX

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/how-does-facetresviewres-relate-to-acgicommondrawdeviation-in-objectarx.html

## 文章内容

by Fenton Webb
Issue
Can you please explain in detail how the FACETRES and VIEWRES relate to the deviation() in the AcGiCommonDraw class?
Solution
Deviation – (2D and 3D) This is the value that controls the fineness of the tessellation. As the value goes towards zero, the tessellation goes up.  The deviation represents the error distance between the tessellated line/surface and the actual curve/curved surface.
VIEWRES - (2D and 3D) Controls the appearance of circles, arcs, ellipses, and splines using short vectors. When you raise and lower the value of VIEWRES, objects controlled by both VIEWRES and FACETRES are affected. When you raise and lower the value of FACETRES, only solid objects are affected.  Valid values are from 1 to 20000.  Note the first prompt in VIEWRES is obsolete and unused by AutoCAD - it is only there for script compatibility.
FACETRES - (2D and 3D) Adjusts the smoothness of shaded and rendered objects and objects with hidden lines removed. Valid values are from 0.01 to 10.0. FACETRES controls the smoothness of shaded and rendered curved solids. It is linked to the value set by VIEWRES: when FACETRES is set to 1, there is a one-to-one correspondence between the viewing resolution of circles, arcs, and ellipses and the tessellation of solid objects. For example, when FACETRES is set to 2, the tessellation will be twice the tessellation set by VIEWRES. The default value of FACETRES is 0.5. The range of possible values is 0.01 to 10.
Regarding the deviation calculation, this depends on the AcGiDeviationType.  For kAcGiMaxDevForFacet the formula is:
deviation =1.0 / FACETRES * 0.5 * pixel width.  
Pixel width is calculated as the inverse of the length in pixels of the camera horizontal (x) vector at the camera target.  Also note that in 3D visual styles only the deviation is further affected by the 3DCONFIG surface and curve tessellation sliders.
And, taken from the ObjectARX Reference regarding AcGiCommonDraw::deviation()
The deviation suggests the maximum tessellation deviation. For example, given a curve that is to be represented by line segments, the maximum distance from one of the line segments to its matching part of the curve is to be no less than some amount. The same value is applied to a curved surface that is approximated by a mesh of triangles or quadrangles.
This value helps decide how fine you are allowed to represent a curve with linear or planar elements, that is, to tessellate. In some cases the curve will be so small compared with the deviation amount that the curve may be represented by just one line segment (or triangle or quadrangle) or not at all. Lots of highly resolved tessellation geometry can fill a graphics system quickly, so this value was created to allow the user of the application some control on this effect. This value is only a suggestion.
See AcGiDeviationType for possible values.
Deviation types use the VIEWRES command's zoom percent value (as does AutoCAD's internal tessellation mechanism). The kAcGiMaxDevForFacet uses the FACETRES system variable value as well (as does AutoCAD when faceting surfaces).

