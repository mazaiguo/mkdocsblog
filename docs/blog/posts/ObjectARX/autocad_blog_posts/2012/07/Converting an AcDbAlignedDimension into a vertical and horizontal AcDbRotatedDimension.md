---
title: "Converting an AcDbAlignedDimension into a vertical and horizontal AcDbRotatedDimension"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Dimension
description: "How can I convert an existing AcDbAlignedDimension into two AcDbRotatedDimensions, so one is vertical and the second horizontal?"
author: Autodesk
---
# Converting an AcDbAlignedDimension into a vertical and horizontal AcDbRotatedDimension

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/converting-an-acdbaligneddimension-into-a-vertical-and-horizontal-acdbrotateddimension.html

## 文章内容

By Philippe Leefsma
Q:
How can I convert an existing AcDbAlignedDimension into two AcDbRotatedDimensions, so one is vertical and the second horizontal?
A:
Following arx code addresses this question: to test it just run the "ConvertAlignedDim" method in a command and select an aligned dimension.
Acad::ErrorStatus postToDatabase (AcDbEntity *pEnt)
{
 AcDbObjectId idObj;
 Acad::ErrorStatus es;
 AcDbBlockTable *pBlockTable;
 AcDbBlockTableRecord *pSpaceRecord;
   if ( (es = acdbHostApplicationServices()->workingDatabase()->getBlockTable (pBlockTable, AcDb::kForRead)) == Acad::eOk )
 {
  if ( (es = pBlockTable->getAt (ACDB_MODEL_SPACE, pSpaceRecord, AcDb::kForWrite)) == Acad::eOk )
  {
   es = pSpaceRecord->appendAcDbEntity (idObj, pEnt);
   pSpaceRecord->close ();
  }
  pBlockTable->close ();
 }
   return es;
}
  void CreateLinDim(const AcGePoint3d& pnt1, const AcGePoint3d& pnt2)
{
 //Create Horizontal dimension
 AcDbRotatedDimension *dimH = new AcDbRotatedDimension(0.0, pnt1, pnt2, pnt1 - AcGeVector3d  (0, 10, 0));
 postToDatabase (dimH);
 dimH->close();
   //Create Vertical dimension
 AcDbRotatedDimension *dimV = new AcDbRotatedDimension((4*atan(1.0))/2.0, pnt1, pnt2, pnt1 - AcGeVector3d (10, 0, 0));
 postToDatabase (dimV);
 dimV->close();
}
  void ConvertAlignedDim(void)
{
 ads_name ename; 
 ads_point pickpt;
   int rc = acedEntSel(L"\nSelect aligned dimension: ", ename, pickpt);
   if(rc != RTNORM)
 {
  if (rc != RTCAN) acutPrintf(L"\nError selecting entity ");
  return;
 }
   AcDbObjectId dimId;
 acdbGetObjectId(dimId, ename);
   AcDbObject *pObj;
 acdbOpenObject(pObj, dimId, AcDb::kForWrite);
 AcDbAlignedDimension* pAlignDim = AcDbAlignedDimension::cast(pObj);
   if(!pAlignDim)
 {
  acutPrintf(L"\nEntity selected is not an aligned dimension...");
  pObj->close();
  return;
 }
   CreateLinDim(pAlignDim->xLine1Point(), pAlignDim->xLine2Point());
   //Get rid of original aligned dimension
 pAlignDim->erase();
 pAlignDim->close();
   return;
}

