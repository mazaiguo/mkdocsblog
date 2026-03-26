---
title: "AcDbSymbolUtilities"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
  - Layer
description: "The class AcDbSymbolUtilities::Services (typedef AcDbSymUtilServices) provides utility functions that are accessed by calling acdbSymUtil(). This u..."
author: Autodesk
---
# AcDbSymbolUtilities

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/acdbsymbolutilities.html

## 文章内容

By Virupaksha Aithal
The class AcDbSymbolUtilities::Services (typedef AcDbSymUtilServices) provides utility functions that are accessed by calling acdbSymUtil(). This utility has functions related to various symbol table operation like getting the model space id, paper space id, layer zero id etc.
Below code shows the procedure to get the model space id directly.
Refer blog http://adndevblog.typepad.com/autocad/2012/04/did-you-know-about-this-utility-class.html for .NET Equivalent
void getModelspaceId()
{
    AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      //get model psace id
    AcDbObjectId modelId;
    modelId = acdbSymUtil()->blockModelSpaceId(pDb);
      //get layer zero id.
    AcDbObjectId LayerId;
    LayerId = acdbSymUtil()->layerZeroId(pDb);
      //other functions...
}

