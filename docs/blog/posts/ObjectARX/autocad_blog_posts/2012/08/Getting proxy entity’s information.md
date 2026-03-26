---
title: "Getting proxy entity’s information"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - DXF
description: "You can make use of class “AcDbProxyEntity” to get the original name, original dxf name and the number of references of that particular entity’s pr..."
author: Autodesk
---
# Getting proxy entity’s information

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/getting-proxy-entitys-information.html

## 文章内容

By Virupaksha Aithal
You can make use of class “AcDbProxyEntity” to get the original name, original dxf name and the number of references of that particular entity’s proxy in the drawing file.
Below code shows the procedure to get the “originalClassName” and “originalDxfName” of the proxy entity.
int nReturn ;
ads_name name;
ads_point pt;
  nReturn = acedEntSel(_T("Select proxy entity\n"), name, pt);
  if(nReturn != RTNORM)
return;
  //get the object Id of the entity
AcDbObjectId Id;
if(acdbGetObjectId(Id, name) != Acad::eOk)
return;
  //open the selected entity
AcDbObject *pObject = NULL;
if(acdbOpenAcDbObject(pObject, Id, AcDb::kForRead)
                                                != Acad::eOk)
{
    return;
}
    AcDbProxyEntity *pProxy = AcDbProxyEntity::cast(pObject);
  if(pProxy != NULL)
{
    acutPrintf(_T("Original class name : %s\n"),
                                pProxy->originalClassName());
      acutPrintf(_T("DXF name : %s\n"),
                                pProxy->originalDxfName());
      acutPrintf(_T("Description : %s\n"),
                            pProxy->applicationDescription());
}
  pObject->close();

