---
title: "Ordinate Dimension Text is incorrect in rotated UCS"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - DXF
  - Dimension
  - UCS
  - Unicode
description: "I have a function which creates ordinate dimensions. When the UCS is rotated around the Z Axis the value for the text is incorrect and appears to b..."
author: Autodesk
---
# Ordinate Dimension Text is incorrect in rotated UCS

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/ordinate-dimension-text-is-incorrect-in-rotated-ucs.html

## 文章内容

By Philippe Leefsma
Q:
I have a function which creates ordinate dimensions. When the UCS is rotated around the Z Axis the value for the text is incorrect and appears to be the value of the X or Y value this point would have in WCS.
A:
The solution to this behavior is to invoke AcDbDimension::setHorizontalRotation() . The value of  DXF group code 51 is queried via AcDbDimension::horizontalRotation(), and is what is established by the angle of the UCS X axis at the time of acquisition.  The X/Y ordinate flag on AcDbOrdinateDimension is set to indicate whether the text is aligned with, or perpendicular to, the horizontal rotation (the UCS X axis in effect) or the vertical direction (the UCS Y axis in effect).
When you rotate around the WCS Z axis to get your UCS, the underlying OCS is exactly the WCS. The value stored is the negative of the horizontal rotation angle in the OCS.  Invoking AcDbEntity::transformBy on a dimension intentionally does not alter this setting, although it moves all the dimensioned points, extension line and text position points. 
So, to reorient the text, get the angle between your UCS x axis and the OCS X axis (which is 1,0,0 when the UCS Z axis is parallel to the WCS Z axis; or else you use the arbitrary axis algorithm to arrive at your OCS X axis, given the UCS Z axis or object normal vector), and pass the negative of this angle to setHorizontalRotation() and your text will be oriented in the direction of that UCS X or Y axis, depending on the setting of the X/Y ordinate flag.
Here is an example that creates an ordinate dimension correctly regardless of the UCS rotation:
void CreateOrdinateDimension()
{
    ads_point pt1;
      if(RTNORM != acedGetPoint(
        NULL, L"\n Select point for ordinate dimension", pt1))
          return;
      AcGePoint3d ptx1(pt1[X],pt1[Y],pt1[Z]);
    AcGePoint3d pT2;
    AcGeMatrix3d mx;
      AcDbDatabase *pDb = acdbHostApplicationServices()->workingDatabase();
      if (!acdbUcsMatrix(mx, pDb))
       return;
      // pT2 is the point for the leader
    pT2[0] = ptx1[0];
    pT2[1] = ptx1[1] - 3.0;
    pT2[2] = ptx1[2];
              AcDbOrdinateDimension *pDim =
        new AcDbOrdinateDimension(Adesk::kTrue,ptx1,pT2,NULL,NULL);
      AcGeVector3d mXPrev = AcGeVector3d::kXAxis;
      // get the old HorizontalRotation
    double mOldHorzRot = pDim->horizontalRotation();
      // matrix to build the ECS
    AcGeMatrix3d mMat;
      // get the old Xaxis and transform it to current plane
    mMat.setToPlaneToWorld(pDim->normal()); //ECS
    mXPrev.transformBy(mMat); //get the ECS xaxis in the world coordinates
    mXPrev.transformBy(mx); //transform current xaxis to plane defined by mx
      // transform the dimension entity by the given transformation matrix
    pDim->transformBy(mx);
      // get the xAxis after transformation of the dimension entity
    mMat.setToWorldToPlane(pDim->normal());
      // transform the old axis to the current ECS.
    mXPrev.transformBy(mMat);
      // get the angle of the old xaxis with respect to the current xaxis
    double mNewHorzRot = - atan2(mXPrev.y, mXPrev.x);
    pDim->setHorizontalRotation(mOldHorzRot + mNewHorzRot);
      AcDbBlockTable *pBlockTable;
    acdbHostApplicationServices()->workingDatabase()
       ->getSymbolTable(pBlockTable, AcDb::kForRead);
      AcDbBlockTableRecord *pBlockTableRecord;
    pBlockTable->getAt(ACDB_MODEL_SPACE, pBlockTableRecord, AcDb::kForWrite);
    pBlockTable->close();
      AcDbObjectId dimIdD;
    pBlockTableRecord->appendAcDbEntity(dimIdD, pDim);
      pBlockTableRecord->close();
    pDim->close();
}

