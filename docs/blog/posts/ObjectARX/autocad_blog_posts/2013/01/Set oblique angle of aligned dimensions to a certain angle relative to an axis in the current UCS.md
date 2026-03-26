---
title: "Set oblique angle of aligned dimensions to a certain angle relative to an axis in the current UCS"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Dimension
  - UCS
description: "Consider this: You want to set the oblique angle of an aligned dimension to an arbitrary value (for example, 30 degrees from the X-axis of the curr..."
author: Autodesk
---
# Set oblique angle of aligned dimensions to a certain angle relative to an axis in the current UCS

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/set-oblique-angle-of-aligned-dimensions-to-a-certain-angle-relative-to-an-axis-in-the-current-ucs.html

## 文章内容

By Gopinath Taget
Consider this: You want to set the oblique angle of an aligned dimension to an arbitrary value (for example, 30 degrees from the X-axis of the current UCS to one of the extension line within which the dimension is constructed).
To do this, you need to realize that that the Oblique angles are calculated relative to the line containing the two start points of the two extension lines of the dimension. Let's call this the base line of aligned dimensions. With this in mind, if the angle from the baseline to X axis is angBaselineToX, and the oblique angle relative to X axis will be angRelOblique, then (- angBaselineToX + angRelOblique) should be sent to AcDbAlignedDimension::oblique() as the input parameter. The following code does this:
void setDimTxtOblique()
{
AcGePoint3d pt1, pt2;
 double baseAng, oblAng;
AcGePoint3d ptDim;
AcGeMatrix3d m;
Acad::ErrorStatus es;
 int ret;
  AcDbDatabase *pDb =
  acdbHostApplicationServices()->workingDatabase();
   // get start and end points
 if(acedGetPoint(NULL, L"\nFirst point: ",
  asDblArray(pt1))!= RTNORM)
  return;
   if( acedGetPoint(asDblArray(pt1), L"\nSecond point: ",
  asDblArray(pt2) ) != RTNORM)
  return;
   // get text position
AcGePoint3d ptMid( 0.5*(pt1.x + pt2.x), 0.5*(pt1.y + pt2.y),
  0.5*(pt1.z + pt2.z));
 if(acedGetPoint(asDblArray(ptMid), L"\nDim Line position:",
  asDblArray(ptDim) ) != RTNORM)
  return;
   // get the oblique angle from users
 // please note it's relative to the X axis of current UCS
ret = acedGetAngle(NULL, L"Oblique angle: <0.0>", &oblAng);
   if( ret == RTNONE ) oblAng = 0.0;
 else if ( ret != RTNORM ) return;
   // calculate the dimension baseline angle
baseAng = acutAngle(asDblArray(pt1), asDblArray(pt2));
   // create aligned dimension
AcDbAlignedDimension* pDim = new AcDbAlignedDimension;
es = pDim->setXLine1Point(pt1); assert(es==Acad::eOk);
es = pDim->setXLine2Point(pt2); assert(es==Acad::eOk);
   // get transform matrix
 if( !acdbUcsMatrix(m, pDb) ) return;
   // set line points and text position as default
es=pDim->setDimLinePoint(ptDim); assert(es==Acad::eOk);
es=pDim->useDefaultTextPosition(); assert(es==Acad::eOk);
es=pDim->setOblique(oblAng-baseAng); assert(es==Acad::eOk);
   // set default database and transform it to WCS
pDim->setDatabaseDefaults();
es = pDim->transformBy(m); assert(es==Acad::eOk);
   // append it to AutoCAD database
AcDbBlockTableRecord *pBlkRec;
AcDbObjectId objID;
es = acdbOpenObject(pBlkRec, pDb->currentSpaceId(),
  AcDb::kForWrite);
assert(es==Acad::eOk);
es =pBlkRec->appendAcDbEntity (objID, pDim) ;
assert(es==Acad::eOk);
 // close it
pDim->close();
pBlkRec->close();
   return;
}

## 评论

**内容**: giack said...
How can i do it with c#?
Reply
04/15/2013 at 07:59 AM

---
