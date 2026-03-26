---
title: "Moving the end of an AcDbLeader using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Unicode
description: "How can I programmatically alter the end vertex of a leader? When I call"
author: Autodesk
---
# Moving the end of an AcDbLeader using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/moving-the-end-of-an-acdbleader-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
How can I programmatically alter the end vertex of a leader? When I call
AcDbLeader::setVertexAt, an error is not returned but when I next move the mtext
associated with the leader, the leader jumps back to its old position. I can do
it interactively, using Grip Points.
Solution
The issue is that when you drag the grip point, you are not just setting the end
vertex, but instead altering an internal value called the offset, which
determines how the leaders ends with respect to the MText object. Unfortunately,
there is currently no access to this offset through ObjectARX. You can,
however, alter the value through ads_entmod. The following sample alters the
leader object, then triggers the reactor function on the leader by changing the
MText.
#include "dblead.h"
  int gr()
{
  ads_name eName;
  ads_point pt;
  if( RTNORM != acedEntSel(L"\nPlease pick leader", eName, pt ) )
    return RTNORM;
    AcDbObjectId id;
  acdbGetObjectId( id, eName );
  AcDbObjectPointer <AcDbLeader> pLeader (id, AcDb::kForRead);
  if (pLeader.openStatus() == Acad::eOk)
  {
    ads_point oldPt;
    asPnt3d( oldPt ) = pLeader->lastVertex();
    AcDbObjectId annoId = pLeader->annotationObjId();
      ads_point newPt;
    acedGetPoint( oldPt, L"\nNew point", newPt );
    AcGeVector3d offset = asPnt3d( newPt ) - asPnt3d( oldPt );
    acutPrintf(_T("\nOffset is %f %f %f "), offset.x, offset.y, offset.z );
      struct resbuf*pRb = ads_entget(eName), *pTempRb;
    for(pTempRb=pRb; pTempRb != NULL; pTempRb=pTempRb->rbnext )
    {
      if( pTempRb->restype == 213 ) {
        pTempRb->resval.rpoint[0] = offset.x;
        pTempRb->resval.rpoint[1] = offset.y;
        pTempRb->resval.rpoint[2] = offset.z;
      }
    }
      int res = ads_entmod( pRb );
    acutPrintf(L"\nResult of entmod is %d", res );
    // now force an update on the annotation object
    AcDbObjectPointer<AcDbObject> pObj(annoId, AcDb::kForWrite);
    pObj->assertWriteEnabled();
  }
  return RTNORM;
}

