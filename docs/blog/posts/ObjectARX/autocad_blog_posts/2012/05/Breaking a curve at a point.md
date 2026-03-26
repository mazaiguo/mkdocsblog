---
title: "Breaking a curve at a point"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "To break a curve at a point, use the AcDbCurve::getSplitCurves method. All you need to know are some points or parameters where you want to break t..."
author: Autodesk
---
# Breaking a curve at a point

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/breaking-a-curve-at-a-point.html

## 文章内容

By Balaji Ramamoorthy
To break a curve at a point, use the AcDbCurve::getSplitCurves method. All you need to know are some points or parameters where you want to break the curve. Here is a sample that lets you select a AcDbCurve (Line, Spline, Arc, ...) and a point near the curve. The point that is on the curve and closest to the selected point is chosen. It then splits the curve and adds the new curve segments to the model space.
static void ADSProjectBreak(void)
{
    AcDbObjectId id;  
    AcGePoint3d pick;  
    AcDbEntity* pEnt;  
      // Let the user select a curve  
    pEnt = selectEntity(
                            _T("\nSelect curve : "),
                            id,
                            pick,
                            AcDb::kForRead
                       );
    if(! pEnt)  
    {
        acutPrintf(_T("\nSelection failed "));   
        return;  
    }
      // Check that it is really a curve  
    AcDbCurve* pCurve = AcDbCurve::cast(pEnt);  
    if(! pCurve)  
    {   
        acutPrintf(L"\nYou didn't select a curve");   
        pEnt->close();   
        return;  
    }  
      // Get the break position and convert to WC coordinates  
    AcGePoint3d breakPnt;  
    if(acedGetPoint (     0,
                        L"\nPick a point on the curve: ",
                        asDblArray(breakPnt)
                    ) != RTNORM)  
    {
        pCurve->close();   
        return;  
    }  
      acdbUcs2Wcs (     asDblArray(breakPnt),
                    asDblArray(breakPnt),
                    Adesk::kFalse
                );
      // Check that the point is on the curve or
    // calculate the closest point tothe curve 
    Acad::ErrorStatus es;
    double dist;  
    es = pCurve->getDistAtPoint(breakPnt, dist);  
    if(es != Acad::eOk)  
    {
        es = pCurve->getClosestPointTo(breakPnt, breakPnt);   
        if(es != Acad::eOk)   
        {       
            acutPrintf(
                        L"\ngetClosestPointTo failed : es =%s",
                        acadErrorStatusText(es)
                      );      
            pCurve->close();       
            return;   
        }  
    }  
        AcGePoint3dArray breakPoints;
    AcDbVoidPtrArray newCurves;
    // Get the segments according to the trim points  
    breakPoints.append(breakPnt);  
    es = pCurve->getSplitCurves(breakPoints, newCurves);  
    if(es != Acad::eOk)  
    {
        acutPrintf  (
                        L"\ngetSplitCurves failed : es = %s",
                        acadErrorStatusText(es)
                    );   
        pCurve->close();   
        return;  
    }  
      pCurve->close();  
      // Here we add the segements to the database with different colors  
    for(int i=0; i < newCurves.length(); i++)  
    {   
        pEnt = (AcDbEntity*)newCurves[i];   
        pEnt->setColorIndex(i+1);   
        appendToBlock(    pEnt,
                        id,
                        ACDB_MODEL_SPACE,
                        acdbHostApplicationServices()->workingDatabase());   
        pEnt->close();  
    }
}
  static AcDbEntity* selectEntity(    const ACHAR* prompt,
                                    AcDbObjectId& id,
                                    AcGePoint3d& pick,
                                    AcDb::OpenMode openMode
                                )
{  
    AcDbEntity* ent = NULL; 
    Acad::ErrorStatus es;  
    ads_name ename; 
    if(acedEntSel(prompt, ename, asDblArray(pick)) != RTNORM) 
        return ent;     
      if(acdbGetObjectId(id,ename) != Acad::eOk) 
        return ent; 
      if((es = acdbOpenAcDbEntity(ent,id,openMode)) != Acad::eOk) 
    { 
        acutPrintf(
                    _T("\nselectEntity : acdbOpenEntity failed es =%s"),
                    acadErrorStatusText(es)
                  );   
        return NULL; 
    }  
    return ent;
}
    static Acad::ErrorStatus appendToBlock(    AcDbEntity* pEnt,
                                        AcDbObjectId& idEnt,
                                        const ACHAR* pcBlockName,
                                        AcDbDatabase * pDb
                                      )
{
    // Default to current database  
    if(!pDb)   
        pDb= acdbHostApplicationServices()->workingDatabase();  
      Acad::ErrorStatus es;
    AcDbBlockTable      * pBlockTable = NULL;  
    // Get block table  
    es = pDb->getBlockTable( pBlockTable, AcDb::kForRead );
    if(es != Acad::eOk)
        return es;  
      // Find block record
    AcDbBlockTableRecord  * pBlockTableRecord = NULL;  
    es = pBlockTable->getAt (
                                pcBlockName,
                                pBlockTableRecord,
                                AcDb::kForWrite
                            );
    if(es != Acad::eOk)
    {
        pBlockTable->close();   
        return es;  
    }
      // append new entity to block: 
    es = pBlockTableRecord->appendAcDbEntity( idEnt, pEnt ); 
    pBlockTableRecord->close();  
    pBlockTable->close();
      return es;
}

