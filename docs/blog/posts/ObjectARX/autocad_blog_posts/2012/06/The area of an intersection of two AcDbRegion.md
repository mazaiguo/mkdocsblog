---
title: "The area of an intersection of two AcDbRegion"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The following sample demonstrates the function AcDbRegion::booleanOper() to perform intersection on two acdbRegion entities. If the entities select..."
author: Autodesk
---
# The area of an intersection of two AcDbRegion

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/the-area-of-an-intersection-of-two-acdbregion.html

## 文章内容

By Xiaodong Liang
The following sample demonstrates the function AcDbRegion::booleanOper() to perform intersection on two acdbRegion entities. If the entities selected are not regions, then they are converted to regions using
AcDbRegion::createFromCurves(). Since region intersection is handled by ACIS, it will be quite slow for a large number of regions.
  static void regionBoolean()
{
      // TODO: Implement the command
      ads_name e1;
      ads_name e2;
      ads_point p1;
      if (RTNORM != acedEntSel(L"\nSelect First \
                                 region",e1,p1))
      {
       acutPrintf(L"\nFailed to select first entity");
       return;
      }
      if (RTNORM != acedEntSel(L"\nSelect Second \
                                 region",e2,p1))
      {
       acutPrintf(L"\nFailed to select second entity");
       return;
      }
        AcDbObjectId objId1 = NULL;       
      AcDbObjectId objId2 = NULL;
      Acad::ErrorStatus es;
      es = acdbGetObjectId (objId1 , e1);
      if (Acad::eOk != es)
      {
       acutPrintf(L"\nFailed to get object Id of first \
                     entity");
       return;
      }
        es = acdbGetObjectId (objId2 , e2);
      if (Acad::eOk != es)
      {
       acutPrintf(L"\nFailed to get object Id of second \
                         entity");
       return;
      }
      //If entities selected are not regions
      // then convert them to regions
      AcDbRegion* pReg1=NULL;
      AcDbRegion* pReg2=NULL;;
        es = acdbOpenObject (pReg1,
                            objId1,
                            AcDb::kForWrite,
                            Adesk::kFalse);
      if(Acad::eOk != es)
      {
       acutPrintf(L"\nFirst entity selected is not a region,\
              it will be converted to a region internally");
      }
        es = acdbOpenObject
              (pReg2,objId2,AcDb::kForWrite,Adesk::kFalse);
      if(Acad::eOk != es)
      {
       acutPrintf(L"\nSecond entity selected is not a \
       region, it will be converted to a region internally");
      }
      AcDbVoidPtrArray curves;
      AcDbVoidPtrArray regions;
      AcDbEntity *pEnt1 = NULL;
      AcDbEntity *pEnt2 = NULL;
      if (pReg1 == NULL) //Not a region entity
      {
       es =acdbOpenAcDbEntity(pEnt1,objId1,
        AcDb::kForRead,Adesk::kFalse);
       if(Acad::eOk != es)
       {
        acutPrintf(L"\nFailed to open first entity for \
                         write");
        return;
       }
       curves.append(pEnt1);   
       pEnt1->close();
      }
      if (pReg2 == NULL) //Not a region entity
      {
           es =acdbOpenAcDbEntity(pEnt2,objId2,
            AcDb::kForRead,Adesk::kFalse);
           if(Acad::eOk != es)
           {
            acutPrintf(L"\nFailed to open second entity for \
                       write");
            return;
           }
           curves.append(pEnt2);   
           pEnt2->close();
      }
      if (pReg1 ==  NULL || pReg2 ==    NULL)
       es=AcDbRegion::createFromCurves(curves,regions);
      if (pReg1 ==  NULL)
       pReg1 = AcDbRegion::cast((AcRxObject*)regions[0]);
      if (pReg2 ==  NULL && regions.length() > 1)
       pReg2 = AcDbRegion::cast((AcRxObject*)regions[1]);
      if (pReg2 ==  NULL && regions.length() == 1)
       pReg2 = AcDbRegion::cast((AcRxObject*)regions[0]);
        // after boolean operation region 2 is deleted
      // and region 1 is updated
      // with resultant region.
      es = pReg1->booleanOper( AcDb::kBoolIntersect, pReg2);
      if(Acad::eOk == es)
      {
       double rarea;
       es = pReg1->getArea(rarea);
       if(Acad::eOk != es)
       {
        acutPrintf(L"\nFailed to get area");   
       }   
       else
       {
        acutPrintf(L"\nArea of intersected region is = %lf",
         rarea);
       }   
      }
      else
      {
       acutPrintf(L"\nFailed to intersect regions");
      }
      pReg1->close();
      pReg2->close();
}

