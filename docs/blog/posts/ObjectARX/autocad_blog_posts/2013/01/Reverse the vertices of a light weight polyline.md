---
title: "Reverse the vertices of a light weight polyline"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Plugin
  - Polyline
description: "In order to do this you will have to read the vertices in reverse order and store them in a temporary array. You should then reset the Polyline to ..."
author: Autodesk
---
# Reverse the vertices of a light weight polyline

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/reverse-the-vertices-of-a-light-weight-polyline.html

## 文章内容

By Gopinath Taget
In order to do this you will have to read the vertices in reverse order and store them in a temporary array. You should then reset the Polyline to clear it of all the vertices data and start adding the vertices by reading the vertex data from the temporary array.
You need to be careful with the bulge values though. As the traverse direction changes, the bulge values will be negative of their previous values. Another crucial point is that the bulge value of a vertex applies between itself and the next vertex. Therefore while reversing the vertices, the last vertex (which will become first after reversing) will have the negative bulge value of the previous (last-but-one) vertex. And this applies for all the vertices. The first vertex (which will become last after reversing) will be assigned the negative bulge value from the last vertex.
The following code shows how to reverse the vertices of Light Weight Polyline(AcDbPolyline). The code also takes care of the start and end widths.
#include <vector>
  void fRevLWPolyline();
  //custom class to hold the bulge and the AcGePoint2d
class ClsVertData
{
public:
ClsVertData ()
{
  m_Bulge = 0.0;
  m_Pt.x = 0.0;
  m_Pt.y = 0.0;
  m_StartWidth = -1;
  m_EndWidth = -1;
};
   double m_Bulge;
AcGePoint2d m_Pt;
 double m_StartWidth;
 double m_EndWidth;
};
  //vector to hold the data
typedef std::vector<ClsVertData> vVertData;
  void fRevLWPolyline()
{
ads_name mSelEnt;
ads_point mPt;
   if(RTNORM != acedEntSel(_T("\nSelect an lwpolyline"),mSelEnt,mPt))
  return;
  AcDbObjectId mID;
AcDbPolyline *pPline = NULL;
  mID.setFromOldId(mSelEnt[0]);
  AcDbEntity *pEnt= NULL;
   if(Acad::eOk != acdbOpenObject(pEnt,mID,AcDb::kForRead))
{
  acutPrintf(_T("\nError: unable to open the object"));
  return;
}
  pPline = AcDbPolyline::cast(pEnt);
 if(NULL == pPline)
{
  pEnt->close();
  acutPrintf(_T("\nError: selected entity is not a lwpolyline"));
  return;
}
   //upgrade for write
pPline->upgradeOpen();
   //get the coordinates
 long mCount;
Adesk::Boolean mClosed;
   //get the number of vertices
mCount = pPline->numVerts() - 1 ;
mClosed = pPline->isClosed();
  ClsVertData mVert;
vVertData mVec;
   //get the bulge, Start Width and End Width
 //of the previuos Vertex list for later use
 double mLastBulge, mLastStWidth, mLastEnWidth;
pPline->getBulgeAt(pPline->numVerts() - 1, mLastBulge);
pPline->getWidthsAt(pPline->numVerts() - 1,
  mLastStWidth, mLastEnWidth);
   double mStWidth,mEnWidth;
   //read the vertices reverse
 for(;mCount>=0;mCount--)
{
  pPline->getBulgeAt(mCount-1, mVert.m_Bulge);
  pPline->getPointAt(mCount,mVert.m_Pt);
  pPline->getWidthsAt(mCount-1,mStWidth,mEnWidth);
    //as the traverse direction is changing
  // the bulge value will negate
  //so does the start and end widths
  mVert.m_Bulge = - mVert.m_Bulge;
  mVert.m_EndWidth = mStWidth;
  mVert.m_StartWidth = mEnWidth;
    //store it in the vector
  mVec.push_back(mVert);
}
   //set the bulge for the last vertex from
 // the last vertex of the previos Vertex list
ClsVertData *pVertData;
pVertData = &mVec.back();
pVertData->m_Bulge = -mLastBulge;
pVertData->m_StartWidth = mLastEnWidth;
pVertData->m_EndWidth = mLastStWidth;
   //reset the polyline
pPline->reset(Adesk::kFalse,0);
   //add the vertices
 for(mCount=0; mCount < mVec.size(); mCount++)
{
  mVert = mVec.at(mCount);
  pPline->addVertexAt(mCount,mVert.m_Pt,mVert.m_Bulge,
   mVert.m_StartWidth,mVert.m_EndWidth);
}
   //close it if was originally
pPline->setClosed(mClosed);
pPline->close();
}

