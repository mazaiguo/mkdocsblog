---
title: "Quick tip: Setting start values for drawing object handles"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Database
description: "If you would like entity handle values of entities to start from a specific value, you can use the AcDbDatabase::setHandseed() method. The followin..."
author: Autodesk
---
# Quick tip: Setting start values for drawing object handles

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/quick-tip-setting-start-values-for-drawing-object-handles.html

## 文章内容

By Gopinath Taget
If you would like entity handle values of entities to start from a specific value, you can use the AcDbDatabase::setHandseed() method. The following code forces handle values to start at 1000.
Note that setting Handseed to a value less than the largest handle in the drawing will prevent entities being added to that drawing and serious problems could occur. To get the current available handle, you can use the AcDbDatabase::handseed method.
AcDbDatabase * pDb = acdbHostApplicationServices()->workingDatabase();
AcDbHandle hand(1000);
Acad::ErrorStatus es = pDb->setHandseed(hand);

## 评论

**内容**: Montalto Glaze said...
Thanks for this blog I have gotten some points here. Recently I'm doing my research related to this.
Reply
03/27/2013 at 02:42 AM

---
