---
title: "AcDb2d/3dpolyline vertex iterator problem with first erased vertex"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "I can't iterate through a modified AcDb2dPolyline or AcDb3dPolyline that has its first vertex marked as erased. How can I solve this problem?"
author: Autodesk
---
# AcDb2d/3dpolyline vertex iterator problem with first erased vertex

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/acdb2d3dpolyline-vertex-iterator-problem-with-first-erased-vertex.html

## 文章内容

Issue
I can't iterate through a modified AcDb2dPolyline or AcDb3dPolyline that has its first vertex marked as erased. How can I solve this problem?
Solution
This is a known issue with the iterator. The iterator for 2D and 3D polylines will not skip an erased first vertex when the iterator is first created. To work around this, get the objectId of the first vertex from the iterator, then use AcDbObjectId::isErased() to check to see if the vertex is erased before starting any processing using the iterator. If the vertex is erased, then step the iterator to the next vertex. This will automatically skip any erased vertices
immediately after the first vertex.
The code demo below shows the issue and solution.
static void iteratePLVer()
{
 // select the 2d polyline
  ads_name eName;
  ads_point pt;
  int res = ads_entsel(_T("\nPlease pick a polyline"), eName, pt);
  if (res != RTNORM)
    return;
    // convert the ename to an ObjectARX objectid
  AcDbObjectId id;
  acdbGetObjectId( id, eName );
    // AcDb2dPolyline or AcDb3dPolyline
    AcDbObjectPointer<AcDb2dPolyline> pPoly(id,
                                AcDb::kForWrite);
    //AcDbObjectPointer<AcDb3dPolyline> pPoly(id,
    //                            AcDb::kForWrite);
      if (pPoly.openStatus() == Acad::eOk)
    {
         AcDbObjectIterator *pIter = 
             pPoly->vertexIterator();
          int count = 0;
        for(; !pIter->done(); pIter->step() )
        {
            count++;
        }
          acutPrintf(
            _T("\nBefore erase, there are %d vertex:"),
            count);
        acutPrintf(
            _T("\n erase one vertex such as the first one"));       
          pIter->start();
        AcDbObjectId vid = pIter->objectId();
        AcDbObjectPointer<AcDb2dVertex> pVertex(vid,
                                    AcDb::kForWrite);
        if(pVertex.openStatus() ==
            Acad::eOk)
        {
          pVertex->erase();
        }
        else
        {
            return;
        }
        delete pIter;
          pIter = pPoly->vertexIterator();
        count = 0;
        acutPrintf(_T("\nIterate vertex again:"));
        for(; !pIter->done();
            pIter->step() )
        {
            count++;
        }
        acutPrintf(_T("\nWithout checking status of erase,\
                      there are %d vertex:"),count);
          acutPrintf(_T("\Now nIterate vertex again, \
                      checking status of erase"));
          count = 0;
        pIter->start();
        for(; !pIter->done();
            pIter->step() )
        {
             vid = pIter->objectId();
             if(!vid.isErased())
                count++;
        }
          acutPrintf(_T("\nchecking status of erase,\
                      there are %d valid vertex:"),count);
        delete pIter;
      }  
}

