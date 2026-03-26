---
title: "Check If SOLID3D Has Valid Shape Manger Object"
date: 2017-10-01
categories:
  - AutoCAD
tags:
  - API
  - Solid
description: "Having Solid’s with invalid shape manager object is always prone to fatal crash it is suggested to check the sanity of underlying shape manager obj..."
author: Autodesk
---
# Check If SOLID3D Has Valid Shape Manger Object

发布日期: 2017-10-01

原始链接: https://adndevblog.typepad.com/autocad/2017/10/check-if-solid3d-has-valid-shape-manger-object.html

## 文章内容

By Madhukar Moogala
Having Solid’s with invalid shape manager object is always prone to fatal crash it is suggested to check the sanity of underlying shape manager object for a given AcDb3dSolid.
You can check using SOLIDEDIT command.
  ;51 is Handle of the solid entity
(command "._solidedit" "B" "C" "51" "X" "X")
With API
Acad::ErrorStatus selectEntity(AcDbObjectId& eId)
{
    ads_name en;
    ads_point pt; 
    ads_entsel(_T("\nSelect an entity: "), en, pt);
 return acdbGetObjectId(eId, en);
}

void solidCheckForValidASM()
{
 AcDbObjectId solId = AcDbObjectId::kNull;
 if (!eOkVerify(selectEntity(solId))) return;

 AcDbSmartObjectPointer pSolid(solId, AcDb::kForRead);
 if (!eOkVerify(pSolid.openStatus())) return; 

 //Get access underlying raw pointer
 if (nullptr == pSolid.object()) return;
 std::unique_ptr pEnt(new AcBrBrep());

 //pass raw pointer to BREP API
 if(pEnt->set(*pSolid.object())!= AcBr::eOk) return;
 
 bool isGoodAsmBody = pEnt->checkEntity();
 if (!isGoodAsmBody)
 {
  acedAlert(_T("Null or Invalid Shape Manager"));
 }

 return;
}

