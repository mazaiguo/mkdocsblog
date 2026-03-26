---
title: "Create a Linear Dimension with ARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Database
  - Dimension
  - ObjectARX
description: "Below code shows the procedure to create linear dimension with ObjectARX"
author: Autodesk
---
# Create a Linear Dimension with ARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/create-a-linear-dimension-with-arx.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to create linear dimension with ObjectARX
Acad::ErrorStatus postToDatabase (AcDbEntity *pEnt)
{
  AcDbObjectId idObj;
  Acad::ErrorStatus es;
  AcDbBlockTable *pBlockTable;
  AcDbBlockTableRecord *pSpaceRecord;
    AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
    es = pDb->getBlockTable(pBlockTable,
                    AcDb::kForRead);
    if (es == Acad::eOk )
  {
    es = pBlockTable->getAt(ACDB_MODEL_SPACE,
                    pSpaceRecord, AcDb::kForWrite);
      if ( es == Acad::eOk )
    {
      es = pSpaceRecord->appendAcDbEntity (idObj, pEnt);
      pSpaceRecord->close ();
    }
    pBlockTable->close ();
  }
    return es;
}
  void CreateLinDim()
{
  AcGePoint3d pnt1, pnt2;
    // pick start point
  acedGetPoint(NULL,
      L"\nPick bottom left point ",
      asDblArray(pnt1));
  acedGetPoint(asDblArray(pnt1),
      L"\nPick top right point ",
      asDblArray(pnt2));
    // now create our dimensions
  AcDbRotatedDimension *dimH =
      new AcDbRotatedDimension(0.0,
      pnt1, pnt2,
      pnt1 - AcGeVector3d  (0, 10, 0));
    AcDbRotatedDimension *dimV =
      new AcDbRotatedDimension((4*atan(1.0))/2.0,
      pnt1, pnt2,
      pnt1 - AcGeVector3d (10, 0, 0));
    // add to model space
  postToDatabase (dimH);
  postToDatabase (dimV);
    // close after use
  dimH->close();
  dimV->close();
}

## 评论

**内容**: nam said...
could y show me the code in vb.net? I really need, please
Reply
12/10/2012 at 10:11 AM

---
