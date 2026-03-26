---
title: "Issues regarding runtime type identification and casting in C++"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "While creating ARX applications, you might wonder what the usage and performance differences are between c-style cast, staticcast, dynamiccast and ..."
author: Autodesk
---
# Issues regarding runtime type identification and casting in C++

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/issues-regarding-runtime-type-identification-and-casting-in-c.html

## 文章内容

By Gopinath Taget
While creating ARX applications, you might wonder what the usage and performance differences are between c-style cast, static_cast, dynamic_cast and AcRxObject::cast() in ObjectARX?
static_cast and c-style cast are the fastest but potentially unsafe, and they will probably generate identical code. ARX includes its own support for safe runtime casting within inheritance hierarchies, AcRxObject::cast(), and this will be substantially slower (some tests indicate a factor of 5) but safe, as it has to do the work at runtime. This is much closer to what the C++ dynamic_cast operator does.
In principal, if you definitely know the type of the object you want to
downcast, then static_cast or c-style cast should be used for performance reasons. If you are not sure, use the ARX cast mechanism but don't make the common mistake of performing it twice as in:
if (pObj->isKindOf(AcDbEntity::desc()))
{  
AcDbEntity *pEnt = AcDbEntity::cast(pObj);
}
In the code above, both 'AcDbEntity::desc()' AND 'AcDbEntity::cast()' use our ARX runtime casting. It's sufficient to do it only once, as in:
if (pObj->isKindOf(AcDbEntity::desc()))
{  
AcDbEntity *pEnt = (AcDbEntity*)pObj;
}
Or:
AcDbEntity *pEnt = AcDbEntity::cast(pObj);
if (NULL != pEnt)
{  
// if pObj is a kind of AcDbEntity, do to pEnt whatever you want here
}

## 评论

**内容**: Alfredo said...
Thanks for that tip!
Reply
12/16/2012 at 09:21 AM

---
**内容**: Sudarshan deshpande said...
Hello ,Can i get AcDbObjectId Of entity which was taken from AcRxObject with AcDbPolyline
Plz help me i stuck really bad in my project.

if(pEntity->isKindOf(AcDbPolyline::desc()))
es = ((AcDbPolyline*)pEntity)->getOffsetCurves(offsetDist, offsetCurves);
else if(pEntity->isKindOf(AcDbCurve::desc()))
es = ((AcDbCurve*)pEntity)->getOffsetCurves(offsetDist, offsetCurves);
if(pEntity->isKindOf(AcDbPolyline::desc()))
pOffsetEntity = (AcDbEntity*)offsetCurves[1];
else if(pEntity->isKindOf(AcDbCurve::desc()))
pOffsetEntity = AcDbCurve::cast((AcDbObject*)offsetCurves[1]);

here i am not gettin ObjectId of pOffsetEntity which i need to mmake regions with another one ...
Reply
10/13/2016 at 05:40 AM

---
