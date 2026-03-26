---
title: "Creating associative dimension in paperspace associated to a modelspace entity"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "Most of the code in this blog post is from a code snippet that my colleague Philippe Leefsma implemented. While his original code created an aligne..."
author: Autodesk
---
# Creating associative dimension in paperspace associated to a modelspace entity

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/creating-associative-dimension-in-paperspace-associated-to-a-modelspace-entity.html

## 文章内容

By Balaji Ramamoorthy
Most of the code in this blog post is from a code snippet that my colleague Philippe Leefsma implemented. While his original code created an aligned dimension in paperspace, i have modified it slightly to create an ordinate dimension to cater to a recent developer request.
Here are the code snippets to create aligned and ordinate dimensions in paperspace while retaining their associativity with a reference point on an entity that is in modelspace.
 //For AcDbDimAssoc 
 #include  "dbdimassoc.h"  
   //For AcDbOsnapPointRef 
 #include  "dbdimptref.h" 
   static  void  paperRotatedDimAssoc(void )
 {
  AcDbDatabase* pDb 
   = acdbHostApplicationServices()->workingDatabase();
    AcDbBlockTableRecordPointer ms(
   ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
    AcDbBlockTableRecordPointer ps(
   ACDB_PAPER_SPACE, pDb, AcDb::kForWrite);
    AcDbObjectId lineId, vpId, dimId;
    AcGePoint3d pt1(AcGePoint3d::kOrigin);
  AcGePoint3d pt2(5,0,0);
    {//creates a line 
   AcDbObjectPointer<AcDbLine> line;
   line.create();
   line->setStartPoint(pt1);
   line->setEndPoint(pt2);
   ms->appendAcDbEntity(lineId, line);
  }
    {//creates a viewport 
   AcDbObjectPointer<AcDbViewport> vp;
   vp.create();
   ps->appendAcDbEntity(vpId, vp);
   vp->setWidth(10);
   vp->setHeight(10);
   vp->setCenterPoint(AcGePoint3d(5,5,0));
     vp->setViewDirection(AcDb::kTopView);
   vp->setViewTarget(AcGePoint3d(2.5,0,0));
   vp->setViewCenter(AcGePoint2d(2.5,0));
   vp->setUnlocked();
   vp->setOn();
     AcGeMatrix3d ms2ps(
    AcDbPointRef::mswcsToPswcs(vp));
   pt1 = pt1.transformBy(ms2ps);
   pt2 = pt2.transformBy(ms2ps);
  }
    {//creates the dimension object 
   AcDbObjectPointer<AcDbRotatedDimension> dim;
   dim.create();
   dim->setXLine1Point(pt1);
   dim->setXLine2Point(pt2);
   dim->setDimLinePoint(AcGePoint3d(2,2,0));
   ps->appendAcDbEntity(dimId, dim);
  }
    AcDbObjectPointer<AcDbDimAssoc> assoc;
  assoc.create();
    AcDbObjectIdArray arr(2);
  arr.append(vpId);
  arr.append(lineId);
    AcDbFullSubentPath path1(
   arr, 
   AcDbSubentId(AcDb::kVertexSubentType, 0));
    AcDbFullSubentPath path2(
   arr, 
   AcDbSubentId(AcDb::kVertexSubentType, 1));
    AcGePoint3d refPt1(pt1);
  AcDbOsnapPointRef *ref1 = new  AcDbOsnapPointRef(
   AcDbPointRef::kOsnapNear, &path1, &path1, &refPt1);
    AcGePoint3d refPt2(pt2);
  AcDbOsnapPointRef *ref2 = new  AcDbOsnapPointRef(
   AcDbPointRef::kOsnapNear, &path2, &path2, &refPt2);
    assoc->setDimObjId(dimId);
  assoc->setTransSpatial(true );
  assoc->setPointRef(AcDbDimAssoc::kXline1Point, ref1);
  assoc->setPointRef(AcDbDimAssoc::kXline2Point, ref2);
  assoc->setAssocFlag(static_cast <int >(
   AcDbDimAssoc::kFirstPointRef
   |AcDbDimAssoc::kSecondPointRef));
    assoc->updateDimension();
    AcDbObjectId dimAssocId;
  Acad::ErrorStatus es = acdbPostDimAssoc(
   dimId, assoc, dimAssocId);
    acutPrintf(_T("\\npost dim: %s\\n" ), 
   acadErrorStatusText(es));
    if  (assoc.open(dimAssocId, AcDb::kForWrite)
   ==Acad::eOk)
  {
   assoc->startCmdWatcher();
   assoc->addToPointRefReactor();
   assoc->addToDimensionReactor();
  }
 }
   static  void  paperOrdinateDimAssoc(void )
 {
  AcDbDatabase* pDb 
   = acdbHostApplicationServices()->workingDatabase();
    AcDbBlockTableRecordPointer ms(
   ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
     AcDbBlockTableRecordPointer ps(
   ACDB_PAPER_SPACE, pDb, AcDb::kForWrite);
    AcDbObjectId lineId, vpId, dimId;
    AcGePoint3d pt1(AcGePoint3d::kOrigin);
  AcGePoint3d pt2(5,0,0);
    {//creates a line 
   AcDbObjectPointer<AcDbLine> line;
   line.create();
   line->setStartPoint(pt1);
   line->setEndPoint(pt2);
   ms->appendAcDbEntity(lineId, line);
  }
    {//creates a viewport 
   AcDbObjectPointer<AcDbViewport> vp;
   vp.create();
   ps->appendAcDbEntity(vpId, vp);
   vp->setWidth(10);
   vp->setHeight(10);
   vp->setCenterPoint(AcGePoint3d(5,5,0));
     vp->setViewDirection(AcDb::kTopView);
   vp->setViewTarget(AcGePoint3d(2.5,0,0));
   vp->setViewCenter(AcGePoint2d(2.5,0));
   vp->setUnlocked();
   vp->setOn();
     AcGeMatrix3d ms2ps(
    AcDbPointRef::mswcsToPswcs(vp));
   pt1 = pt1.transformBy(ms2ps);
   pt2 = pt2.transformBy(ms2ps);
  }
    {//creates the dimension object 
   AcDbObjectPointer<AcDbOrdinateDimension> dim;
   dim.create();
   dim->setUsingXAxis(true );
   dim->setOrigin(pt1);
   dim->setDefiningPoint(pt2);
   dim->setLeaderEndPoint(pt2 
    + AcGeVector3d(1.0, 0.0, 0.0));
   ps->appendAcDbEntity(dimId, dim);
  }
    AcDbObjectPointer<AcDbDimAssoc> assoc;
  assoc.create();
    AcDbObjectIdArray arr(2);
  arr.append(vpId);
  arr.append(lineId);
    AcDbFullSubentPath path1(
   arr, 
   AcDbSubentId(AcDb::kVertexSubentType, 0));
    AcDbFullSubentPath path2(
   arr,
   AcDbSubentId(AcDb::kVertexSubentType, 1));
    AcGePoint3d refPt1(pt1);
  AcDbOsnapPointRef *ref1 = new  AcDbOsnapPointRef(
   AcDbPointRef::kOsnapNear, &path1, &path1, &refPt1);
    AcGePoint3d refPt2(pt2);
  AcDbOsnapPointRef *ref2 = new  AcDbOsnapPointRef(
   AcDbPointRef::kOsnapNear, &path2, &path2, &refPt2);
    assoc->setDimObjId(dimId);
  assoc->setTransSpatial(true );
  assoc->setPointRef(AcDbDimAssoc::kOriginPoint, ref1);
  assoc->setPointRef(AcDbDimAssoc::kDefiningPoint, ref2);
  assoc->setAssocFlag(static_cast <int >(
   AcDbDimAssoc::kFirstPointRef|
   AcDbDimAssoc::kSecondPointRef));
    assoc->updateDimension();
    AcDbObjectId dimAssocId;
  Acad::ErrorStatus es = 
   acdbPostDimAssoc
   (dimId, assoc, dimAssocId);
    acutPrintf(_T("\\npost dim: %s\\n" ), 
   acadErrorStatusText(es));
    if  (assoc.open(dimAssocId, AcDb::kForWrite)==Acad::eOk)
  {
   assoc->startCmdWatcher();
   assoc->addToPointRefReactor();
   assoc->addToDimensionReactor();
  }
 }

## 评论

**内容**: Loic said...
Hi Balaji,
What about the new assoc dimensions based on AcDbAssocPersSubentId (http://adndevblog.typepad.com/autocad/2015/02/making-a-custom-entity-associative-dimension-enabled.html) ?
I have some issues to make my custom compound entities compatible with this new behavior and I think having a sample similar to yours but using the new behaviour would help me to understand how it works.
Thanks!
Loic
Reply
03/27/2015 at 12:35 AM

---
**内容**: Balaji said in reply to Loic...
Hi Loic,
Sorry for the delay in replying to you. I had taken a day off last Friday.
I will look into the sample that you shared and see how we can get it to work with the AcdbAssocPersSubentId.
I will get back to you on this.
Regards,
Balaji
Reply
03/29/2015 at 10:53 PM

---
**内容**: Loic said in reply to Balaji...
Thanks a lot!
(No worry for the delay, there's no rush here, I hope you enjoyed your Friday!)
Reply
03/30/2015 at 01:15 AM

---
**内容**: Abhay Joshi said...
do we need to delete AcDbOsnapPointRef instance?
Reply
01/25/2016 at 05:33 AM

---
**内容**: Abhay Joshi said...
Hello Balaji,
I am trying to create the associative dimension in paper space same as example. As per your sample code, it works well for top viewport with scale 1:1. But creates issues for dimensions in isometric views with scale other than 1:1. Before creating AcDbDimAssoc object. I override DIMLFAC for dimension by using setDimlfac(). Which include scale (1.22 * 10). It dimension showed correct value after creating it. But after I changed view scale manually, the value is no longer correct.
After checking difference between manual and programmatic dimension in ArxDbg, I found XDATA for ACAD_DIMASSOC_CALC_DIMLFAC, ACAD_DIMASSOC_DIMLFAC and ACAD_DIMASSOC_OVERRIDDEN_DIMLFAC in manual dimensions.
After googling I found link https://forums.autodesk.com/t5/autocad-2000-2000i-2002-archive/paperspace-dimensions-giving-incorrect-values/m-p/141420 for DIMLFAC XDATA. I mentioned to set XDATA for these applications.
In code after creating AcDbDimAssoc I set XDATA to dimension for ACAD_DIMASSOC_OVERRIDDEN_DIMLFAC with lfac*viewscale and ACAD_DIMASSOC_CALC_DIMLFAC with viewscale.
Then dimension worked fine for all manual operations (changing viewscale, modification in line).
Is it safe to set XDATA for DIMLFAC?
Reply
09/23/2016 at 06:24 AM

---
**内容**: Ari Bejarano said...
Hi Balaji,
This piece of code does not work for me and I do not know what I'm doing wrong, just draw the line and the text appears:
\npost dim: eOk\n
I am using autocad 2018 and ObjectARX 2018, my goal is to do it from .net but I see that it is not yet possible. Could you pass me the complete code, please?
Reply
08/18/2017 at 06:23 PM

---
