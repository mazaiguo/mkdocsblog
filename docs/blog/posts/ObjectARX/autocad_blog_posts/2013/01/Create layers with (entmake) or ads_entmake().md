---
title: "Create layers with (entmake) or ads_entmake()"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Layer
description: "It is possible to create layers using adsentmake() or (entmake). However, you need to specify all the100 subclass data markers on calling entmake. ..."
author: Autodesk
---
# Create layers with (entmake) or ads_entmake()

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-layers-with-entmake-or-ads_entmake.html

## 文章内容

By Augusto Goncalves
It is possible to create layers using ads_entmake() or (entmake). However, you need to specify all the100 subclass data markers on calling entmake. A subclass data marker specifies the derived class names of an object. Specifying these subclass data markers is necessary for all new Entity/Object types. For R12 compatibility reasons, you can omit these subclass data markers for the old R12 entities.
It wasn't possible to entmake layers in R12; this is why you need to specify the subclass data markers for layers as well:
(entmake (list (cons 0 "LAYER")
           (cons 100 "AcDbSymbolTableRecord")
           (cons 100 "AcDbLayerTableRecord")
           (cons 2 "My Layer Name")
           (cons 70 0)
           (cons 62 7)
           (cons 6 "CONTINUOUS")
     )
)
I wanted to create a layer using ads_entmake(), but ads_entmake() returns the error code RTREJ (AutoCAD rejected request -- invalid). Because the routine has to be used in drawings where that layer already could exist, the solution with ads_command() is not so nice, because of the warning "Layer already exists". The entmake-solution raises no warning to the user if a layer already exists

