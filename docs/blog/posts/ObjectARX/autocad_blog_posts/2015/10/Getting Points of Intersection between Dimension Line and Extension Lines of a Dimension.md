---
title: "Getting Points of Intersection between Dimension Line and Extension Lines of a Dimension"
date: 2015-10-01
categories:
  - AutoCAD
tags:
  - DWG
  - Dimension
description: "It was quite a hectic task getting intersection between said lines, the problem seems pretty straight forward for AcDbAlignedDimension,"
author: Autodesk
---
# Getting Points of Intersection between Dimension Line and Extension Lines of a Dimension

发布日期: 2015-10-01

原始链接: https://adndevblog.typepad.com/autocad/2015/10/getting-points-of-intersection-between-dimension-line-and-extension-lines-of-a-dimension.html

## 文章内容

By Madhukar Moogala
It was quite a hectic task getting intersection between said lines, the problem seems pretty straight forward for AcDbAlignedDimension,
the amount of work increased when the logic was to stretch to AcDbRotatedDimension, things really started messy for me.
The objective of this work is to get these points as shown in screenshot.
You can download the sample from here, sample contains utility functions and custom dwgfiler class, which was needed for getting intersections
for AcDbRotatedDimension.
The code for AcDbAlignedDimension:
void test1()
{
    Adesk::Boolean status = false;
    ads_name ename;
    ads_point pt;
    if(RTNORM !=(acedEntSel(_T("Select Aligned Dimension"),ename,pt)))return;
    AcDbObjectId objid;
    if(!eOkVerify(acdbGetObjectId(objid,ename)))return;
    AcDbObjectPointer<AcDbAlignedDimension> entity(objid,AcDb::kForRead);
      if(entity != NULL)
    {
          /*Some point lying somewhere on Dimension line*/
        AcGePoint3d dimLoc = entity->dimLinePoint();
          /*Extension Line Orgins*/
        AcGePoint3d xPt1 = entity->xLine1Point();
        AcGePoint3d xPt2 = entity->xLine2Point();
          /*Do the geometry work*/
        AcGeLine2d entityLine = AcGeLine2d(AcGePoint2d(xPt1.x,xPt1.y),AcGePoint2d(xPt2.x,xPt2.y));
        AcGeLine2d dimensionLine = AcGeLine2d(AcGePoint2d(dimLoc.x,dimLoc.y),entityLine.direction());
        AcGeLine2d lineStartingFromxPt1;
        entityLine.getPerpLine(get2dPoint(xPt1),lineStartingFromxPt1);
        AcGeLine2d lineStartingFromxPt2;
        entityLine.getPerpLine(get2dPoint(xPt2),lineStartingFromxPt2);
        AcGePoint2d interSection1;
        status = lineStartingFromxPt1.intersectWith(dimensionLine,interSection1);
        if(status)
        {
            /*Utility to create and post Point entity*/
            makePointEnt(AcGePoint3d(interSection1.x,interSection1.y,0.00),3);
        }
          AcGePoint2d interSection2;
        status = lineStartingFromxPt2.intersectWith(dimensionLine,interSection2);
        if(status)
        {
            makePointEnt(AcGePoint3d(interSection2.x,interSection2.y,0.00),3);
        }
      }
  }
The code for AcDbRotatedDimension:
The logic is to explode the dimension entity and find intersections between the line segments, if explode was not possible for dimension
like if the dimension is parametric and has dynamic constraint form, then we need to dig in to database of the dimension object and find its
owner holding dimension entities like lines,mtext etc.
void test2()
{
    Adesk::Boolean isConstraintChanged = false;
    ads_name ename;
    ads_point pt;
    if(RTNORM !=(acedEntSel(_T("Select Rotated Dimension"),ename,pt)))return;
    AcDbObjectId objid;
    if(!eOkVerify(acdbGetObjectId(objid,ename)))return;
    AcDbSmartObjectPointer<AcDbRotatedDimension> entity(objid,AcDb::kForWrite);
    AcArray<AcDbLine*> lines;
      if(entity != NULL )
    {
        /*Explode is not possible on Constraint Dynamic*/
        if(!entity->isConstraintDynamic())
        {
            AcDbVoidPtrArray entitySet;
                if(!eOkVerify(entity->explode(entitySet))) return;
              for(int i=0; i < entitySet.length(); i++)
            {
                AcDbObject* ent = (AcDbObject*&)entitySet.at(i);
                if(ent->isKindOf(AcDbLine::desc()))
                                {
                                    AcDbLine* pLine = new AcDbLine();
                                    pLine = AcDbLine::cast(ent->clone());
                                    if(pLine != NULL)
                                        lines.append(pLine);
                                    }
                else continue;
            }
            if(lines.length() > 0)
            {
                makeIntersectionPoints(lines);
                }
              /*Clear */
            for(int i=0; i < entitySet.length(); i++)
            {
                AcDbObjectId ObjId;
                AcDbEntity *pNewEnt=AcDbEntity::cast((AcRxObject*)entitySet[i]);
                if(pNewEnt != NULL)
                {
                    delete pNewEnt;
                }
                else continue;
            }
                }
        /* Logic is to dig in to hardpointer references of Dimension,
        find the owner holding dimension entity lines
        */
        else /*Could be Constrained on Dimension*/
        {
            /*We need to change constraint form, to help get Lines and restore back*/
            entity->setConstraintDynamic(false);
                if(!eOkVerify(entity->downgradeOpen())) return;
              ArxDbgReferenceFiler filer;
            AcDbObjectIdArray   hardPointerIds;
            AcDbObjectId tobePurgeLater;
            entity->dwgOut(&filer);
              hardPointerIds = filer.m_hardPointerIds;
            AcDbObject* tmpObj;
            int len = hardPointerIds.length();
            for (int i=0; i<len; i++)
            {
                // might have passed in erased ones
                if (!eOkVerify(acdbOpenAcDbObject(tmpObj, hardPointerIds[i], AcDb::kForRead, true))) return;
                  if(tmpObj->isKindOf(AcDbBlockTableRecord::desc()))
                {
                    AcDbBlockTableRecord* btr = AcDbBlockTableRecord::cast(tmpObj);
                    if(btr->isAnonymous())
                    {
                        tobePurgeLater = hardPointerIds[i];
                          AcDbBlockTableRecordIterator* iter = NULL;
                        btr->newIterator(iter);
                        AcDbEntity* ent;
                        /*Filter out only lines*/
                        for (; !iter->done(); iter->step()) {
                            if (!eOkVerify(iter->getEntity(ent, AcDb::kForRead))) return;
                            if(ent->isKindOf(AcDbLine::desc()))
                            {
                                AcDbLine* pLine = new AcDbLine();
                                pLine = AcDbLine::cast(ent->clone());
                                if(pLine != NULL)
                                    lines.append(pLine);
                                }
                            if(!eOkVerify(ent->close())) return;   
                            }
                        delete iter;
                        break; /*further dredging not required*/
                    }
                }
                /*Could be ltr,str,vtr etc*/
                else continue;
            }
              if(!eOkVerify(tmpObj->close())) return;
              if(lines.length() > 0)   
            {
                makeIntersectionPoints(lines);
            }
            /*Reverse the changes*/
            if(eOkVerify(entity->upgradeOpen()))
            {
                entity->setConstraintDynamic(true);
                if(!eOkVerify(entity->downgradeOpen())) return;
            }
              /*When we switch from Dynamic constraint form to annotation, Acad creates an anonymous.
            We don't want leave this trace in customer database, hence purge */
            AcDbObjectIdArray purgableIds;
            purgableIds.append(tobePurgeLater);
              if(!eOkVerify(acdbHostApplicationServices()->workingDatabase()->purge(purgableIds))) return;
        }
        }
}
Utility Functions:
void makePointEnt(const AcGePoint3d& pt, int colorIndex)
{
    int mode = 0;
     resbuf rb;
    if (acedGetVar(_T("PDMODE"), &rb)== RTNORM)
    {
        ASSERT(rb.restype == RTSHORT);
        mode = rb.resval.rint;
    }
      if (mode == 0)
    {
    rb.restype = RTSHORT;
    rb.resval.rint = 99;
    acedSetVar(_T("PDMODE"),&rb);
    }
      AcDbPoint* tmpPt = new AcDbPoint(pt);
    tmpPt->setColorIndex(colorIndex);
    AcDbObjectId idObj;
    postToDatabase(acdbHostApplicationServices()->workingDatabase(),tmpPt,idObj);
    tmpPt->close();
}
  AcGePoint2d get2dPoint(AcGePoint3d& pt3d)
{
    return AcGePoint2d(pt3d.x,pt3d.y);
}
  PCTSTR booleanToStr(bool b, CString& str)
{
    if (b)
        str = _T("True");
    else
        str = _T("False");
      return str;
}
  void cleanLineArray(AcArray<AcDbLine*> &lines)
{
    int sizeofArray = lines.length();
          for(int i =0; i< sizeofArray;i++)
        {
            AcDbLine* tempLine = lines.at(i);
            if(tempLine != NULL) delete tempLine;
        }
        lines.setLogicalLength(0);
}
  /*Creates intersection points and wipes off the array*/
void makeIntersectionPoints(AcArray<AcDbLine*> &lines)
{
      AcDb::Intersect type = AcDb::Intersect::kExtendBoth;
    AcGePoint3dArray points;   
        int sizeofArray = lines.length();
        /*As there are only 3 Lines in cylic order, this logic works! For other cases this logic is stupid*/
        for(int i =0; i< sizeofArray;i++)
        {
            AcDbObjectId id,rayId;
            AcDbLine* tempLine = lines.at(i);
            if(tempLine != NULL)
            {
              /*i+1 & i++ makes huge here difference*/
            bool good = eOkVerify(tempLine->intersectWith(lines.at(i== sizeofArray-1 ? 0:i+1),type,points));
              if(good && points.length() > 0 )
            {
                makePointEnt(points.first(),3);
                points.setLogicalLength(0);
            }
              }
          }
    cleanLineArray(lines);
  }
Here is a demonstration video or the link:

