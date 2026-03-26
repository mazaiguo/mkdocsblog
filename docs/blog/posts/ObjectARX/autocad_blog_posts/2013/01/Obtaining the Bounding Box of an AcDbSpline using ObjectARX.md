---
title: "Obtaining the Bounding Box of an AcDbSpline using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Dimension
  - ObjectARX
description: "I want to get the bounding box of spline, but the getGeomExtents() functions does not return the expected results. How do I get a tighter bounding ..."
author: Autodesk
---
# Obtaining the Bounding Box of an AcDbSpline using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/obtaining-the-bounding-box-of-an-acdbspline-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
I want to get the bounding box of spline, but the getGeomExtents() functions does not return the expected results. How do I get a tighter bounding box for a spline?
Solution
The AcDbSpline does not return a "tight" bounding box when getGeomExtents() is used.
To get a tighter bounding box you need to calculate the bounding box yourself. You can make use of the function getPointAtParam() to traverse along the spline and check for the maximum/minimum x and y coordinates. The accuracy of the bounding box depends upon how finely the curve is divided and sampled. The division value of 1e6 gives a good accuracy and takes acceptable time to calculate. The functions pasted below shows how this can be done. The attached VC++ project has the complete code (with minimal error checking). Type command "SplineBB" and select a spline object. It will draw two bounding boxes. The red rectangle is the extents returned by the getGeomExtents() while the yellow rectangle is the calculated one.
Something like this:
///////////////////////////////////////////////////////////////////////////////////////////////
//Description: fKeepExtremes
//1) Function to check for the minimum/maximum X and Y. 
//2) mPtMin and mPtMax will have minimum/maximum X and Y
///////////////////////////////////////////////////////////////////////////////////////////////
void fKeepExtremes(AcGePoint3d& mPtSample,AcGePoint3d& mPtMin,AcGePoint3d& mPtMax)
{
 //test for max
 if(mPtSample.x > mPtMax.x) mPtMax.x = mPtSample.x;
 if(mPtSample.y > mPtMax.y) mPtMax.y = mPtSample.y;
 if(mPtSample.z > mPtMax.z) mPtMax.z = mPtSample.z;
 
 //test for min
 if(mPtSample.x < mPtMin.x) mPtMin.x = mPtSample.x;
 if(mPtSample.y < mPtMin.y) mPtMin.y = mPtSample.y; 
 if(mPtSample.z > mPtMax.z) mPtMax.z = mPtSample.z;
}
///////////////////////////////////////////////////////////////////////////////////////////////
//Description: fGetBoundingBoxBySampling
//1) Function to divide the AcDbSpline 1e6 times and check for points at each division
///////////////////////////////////////////////////////////////////////////////////////////////
void fGetBoundingBoxBySampling(AcDbSpline *pSpline,AcGePoint3d& mPtMin, AcGePoint3d& mPtMax)
{
 double mParam;
 double mIncr;
 double mStartParam;
 double mEndParam;
 AcGePoint3d mPtTemp;
 pSpline->getStartPoint(mPtTemp);
 pSpline->getParamAtPoint(mPtTemp,mStartParam);
 pSpline->getEndPoint(mPtTemp);
 pSpline->getParamAtPoint(mPtTemp,mEndParam);
 
 //calculate the division
 mIncr = (mEndParam - mStartParam)/1e6; //1e6 is the sampling tolerance 
 
 //set the seed point for max and min. It is set to the start point
 mPtMax = mPtTemp;
 mPtMin = mPtTemp;
 for(mParam = mStartParam;mParam <= mEndParam;mParam +=mIncr)
 {
  if(Acad::eOk == pSpline->getPointAtParam(mParam,mPtTemp))
  {
   fKeepExtremes(mPtTemp,mPtMin,mPtMax);
  }
 }
}
///////////////////////////////////////////////////////////////////////////////////////////////
//Description: fDrawRect
//1) Draws a LwPolyline rectangle given lower left and upper right corners
///////////////////////////////////////////////////////////////////////////////////////////////
void fDrawRect(AcGePoint3d& mPtMin,AcGePoint3d& mPtMax,int mColor)
{
 AcDbPolyline *pPline = new AcDbPolyline(4);
 pPline->addVertexAt(0, AcGePoint2d(mPtMin.x,mPtMin.y));
 pPline->addVertexAt(1,AcGePoint2d(mPtMax.x,mPtMin.y));
 pPline->addVertexAt(2,AcGePoint2d(mPtMax.x,mPtMax.y));
 pPline->addVertexAt(3,AcGePoint2d(mPtMin.x,mPtMax.y));
 pPline->setClosed(Adesk::kTrue);
 
 fAddEntToDwg(acdbHostApplicationServices()->workingDatabase(),pPline);
 pPline->setColorIndex(mColor);
 pPline->close(); 
}
///////////////////////////////////////////////////////////////////////////////////////////////
//Description: SplineBB
//1) command 'SplineBB' 
///////////////////////////////////////////////////////////////////////////////////////////////
void SplineBB()
{
 AcDbEntity *pEnt = NULL;
 AcDbObjectId mId;
 ads_point mPt;
 ads_name mEname;
 
 //select the entity
 if ( RTNORM == acedEntSel(L"Select a Spline", mEname, mPt))
 {
  if ( Acad::eOk == acdbGetObjectId(mId, mEname ))
  {
   acdbOpenAcDbEntity(pEnt, mId, AcDb::kForRead);
  }
 }
 else
 {
  return;
 }
 //see if it is a spline
 AcDbSpline *pSpline = NULL;
 if (NULL != pEnt)
 {
  pSpline = AcDbSpline::cast(pEnt);
  if(NULL != pSpline)
  {
   AcGePoint3d mPtMin,mPtMax;
   //draw the bounding box returned by spline's getGeomExtents
   AcDbExtents mExts;
   pSpline->getGeomExtents(mExts);
   //draw bounding box returned by the spline in red
   fDrawRect(mExts.minPoint(),mExts.maxPoint(),1);
   
   //calculate the time taken
   struct _timeb t1,t2;
   _ftime(&t1);
   //calculate the bounding box
   fGetBoundingBoxBySampling(pSpline,mPtMin,mPtMax);
   
   _ftime(&t2);
   acutPrintf(L"\nMethod Time %6.2f seconds.\n", (t2.time + (double)(t2.millitm)/1000) - (t1.time + (double)(t1.millitm)/1000) );
   
   //draw calculated bounding box in yellow
   fDrawRect(mPtMin,mPtMax,2);
   pSpline->close();
  }
  else
  {
   acutPrintf(L"\nEntity is not an Spline");
   pEnt->close();
  }
 }
 return;
}

