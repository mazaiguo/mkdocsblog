---
title: "How to transform a block reference and all its attributes using ObjectARX?"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
description: "How do I position, rotate or scale a block reference and all its attributes?"
author: Autodesk
---
# How to transform a block reference and all its attributes using ObjectARX?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-transform-a-block-reference-and-all-its-attributes-using-objectarx.html

## 文章内容

By Philippe Leefsma
Q:
How do I position, rotate or scale a block reference and all its attributes?
A:
The functions AcDbBlockReference::setPosition(), AcDbBlockReference::setRotation() and AcDbBlockReference::setScaleFactors() all
work on just the block reference. They do not transform the attributes attached to the block.
The easiest way to transform a block reference and all its attributes is to call AcDbEntity::transformBy() on the block reference. This operation transforms the block and all its attributes in exactly the same way as it does for any other entity. This function can be used to translate, rotate or scale the block reference.
Here is the code for four simple commands:
AcDbBlockReference * getBR();
  //TRANS - translates the selected block reference by (100,100,0).
void Asdktrans()
{
   AcDbBlockReference * pBR = getBR();
     if (pBR == NULL)
     return;
     AcGeMatrix3d mat;
   mat = mat.setToTranslation(AcGeVector3d(100,100,0));
   pBR->transformBy(mat);
     pBR->close();
}
  //ROT - rotates the selected block reference by 45 degrees.
void Asdkrot()
{
   AcDbBlockReference * pBR = getBR();
     if (pBR == NULL)
     return;
     AcGeMatrix3d mat;
   mat = mat.rotation(0.785398, pBR->normal(), pBR->position());
   pBR->transformBy(mat);
     pBR->close();
}
  //SCAL - scales the selected block reference by a factor of 2.
void Asdkscal()
{
   AcDbBlockReference * pBR = getBR();
   if (pBR == NULL)
     return;
     AcGeMatrix3d mat;
   mat = mat.scaling(2, AcGePoint3d(0,0,0));
   pBR->transformBy(mat);
     pBR->close();
}
  //ROTSCALTRANS - performs all three operations in a single call to transformBy().
void Asdkrotscaltrans()
{
   AcDbBlockReference * pBR = getBR();
     if (pBR == NULL)
     return;
     AcGeMatrix3d mat1;
   mat1 = mat1.rotation(0.785398, pBR->normal(), pBR->position());
   AcGeMatrix3d mat2;
   mat2 = mat2.scaling(2, AcGePoint3d(0,0,0));
   AcGeMatrix3d mat3;
   mat3 = mat3.setToTranslation(AcGeVector3d(100,100,0));
     AcGeMatrix3d mat;
   mat = mat1*mat2*mat3;
   pBR->transformBy(mat);
     pBR->close();
}
  // Opens block reference chosen by user
AcDbBlockReference * getBR()
{
  ads_name ename;
  ads_point pt;
  AcDbObjectId objId;
  Acad::ErrorStatus es;
    if (RTNORM != acedEntSel(_T("\nSelect Block : "), ename, pt))
    return NULL;
    es = acdbGetObjectId(objId, ename);
  if (es != Acad::eOk)
    return NULL;
    AcDbBlockReference * pBR;
  AcDbObject * pObj;
    acdbOpenObject(pObj, objId, AcDb::kForWrite);
    pBR = AcDbBlockReference::cast(pObj);
    if (pBR == NULL)
  {
    pObj->close();
    acutPrintf(_T("\nThis is not a block."));
    return NULL;
  }
    return pBR;
}

