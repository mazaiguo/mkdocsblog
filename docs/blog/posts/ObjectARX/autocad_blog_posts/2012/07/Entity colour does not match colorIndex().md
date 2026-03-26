---
title: "Entity colour does not match colorIndex()"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Layer
description: "I have a drawing where the colorIndex() of the layer that the entity is on is 7, which means that entities on it with Color set to By Layer should ..."
author: Autodesk
---
# Entity colour does not match colorIndex()

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/entity-colour-does-not-match-colorindex.html

## 文章内容

By Adam Nagy
I have a drawing where the colorIndex() of the layer that the entity is on is 7, which means that entities on it with Color set to By Layer should be either black or white. However, the entity on the layer is drawn in grey for some reason. I also checked the layer's color index using ArxDbg and could confirm that it was indeed 7.
Solution
If the color of the entity was really white, then in the Layer Dialog next to the color box it would read "white" instead of "242, 242, 242"
When you check the AcDbEntity::colorIndex() or AcDbEntity::color().colorIndex() then you get back the index which is the closest to the actual color of the entity.
However from the AcDbEntity::color().colorMethod() you can tell if the entity’s color is really based on the specific color index, or it has just been mapped to it.
Same with layers.
I added the following to the ArxDbg sample’s ArxDbgUiTdcDbObjectBase::display() function
addToDataList(_T("ColorMethod"),
  ArxDbgUtils::intToStr(layer->color().colorMethod(), str));
Now when I check the layer with ArxDbg, then I can see that the colorMethod() for that layer is ColorMethod::kByColor (=194). If in the user interface I set its color to White, then I will get back ColorMethod::kByACI (=195)
This is how you can tell programmatically if an object’s color is really based on an AutoCAD Color Index.

