---
title: "Replacing an entity while preserving its handle"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "You may need to replace entities with other entities while retaining the original handle value, since other parts of your program already depend on..."
author: Autodesk
---
# Replacing an entity while preserving its handle

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/replacing-an-entity-while-preserving-its-handle.html

## 文章内容

By Balaji Ramamoorthy
You may need to replace entities with other entities while retaining the original handle value, since other parts of your program already depend on the handle value.
You can replace an existing entity by a new one with ObjectARX and the handle can be retained using function AcDbObject::handOverTo(). The new entity will have the same handle and AcDbObjectId as the old one.
The example below prompts you to select a line. A new circle will be created that has the same handle as the old line. You can exchange the line by any other entity if required.
Here is the sample code :
ads_name ename;
AcGePoint3d pick = AcGePoint3d::kOrigin;
if(acedEntSel
            (
                ACRX_T("Select a line to replace :"),
                ename,
                (ads_real*)&pick
            ) != RTNORM)
    return;
  AcDbObjectId id = AcDbObjectId::kNull;
if(acdbGetObjectId(id, ename) != Acad::eOk)
    return;
  AcDbEntity* pEnt = NULL;
Acad::ErrorStatus es
            = acdbOpenAcDbEntity(pEnt, id, AcDb::kForWrite);
if(es != Acad::eOk)
    return;
  AcDbLine* pLine = AcDbLine::cast(pEnt);
if(! pLine)
{
    acutPrintf(_T("\nSelected entity is not a line"));
    pEnt->close();
    return;
}
  double endParam = 0.0;
pLine->getEndParam(endParam);
  double startParam = 0.0;
pLine->getStartParam(startParam);
  AcGePoint3d mp = AcGePoint3d::kOrigin;
pLine->getPointAtParam( (startParam + endParam) * 0.5, mp ); 
  AcDbCircle *pCircle
        = new AcDbCircle(
                            mp,
                            pLine->normal(),
                            (pLine->endPoint()-mp).length()
                        );
pLine->upgradeOpen();
  if(pLine->handOverTo(pCircle) == Acad::eObjectToBeDeleted)
{
    acutPrintf(_T("\nLine replaced by a circle."));   
    pCircle->close();
    delete pLine;
}
else
{
    acutPrintf(_T("\nCouldn't replace line"));   
    pLine->close();
    delete pCircle;
}
Posted at 02:07 AM in AutoCAD, Balaji Ramamoorthy, ObjectARX | Permalink

