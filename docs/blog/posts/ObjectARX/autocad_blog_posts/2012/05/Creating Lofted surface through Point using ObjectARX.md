---
title: "Creating Lofted surface through Point using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
  - Surface
description: "The crossection of a lofted surface can defined using entities such as a AcDbCurve or a AcDbPoint. When a point is picked, a temporary AcDbPoint en..."
author: Autodesk
---
# Creating Lofted surface through Point using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-lofted-surface-through-point-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
The crossection of a lofted surface can defined using entities such as a AcDbCurve or a AcDbPoint. When a point is picked, a temporary AcDbPoint entity can be created and added to the database. Using the AcDbSurface::createLoftedSurface method, the lofted surface can now be created and the temporary AcDbPoint entity can be erased. For more details, please refer the ObjectARX documentation on "createLoftedSurface" to know more about using points to define cross-section of a lofted surface.
Here is a sample code :
static void ADSCreateLoft(void)
{
    Acad::ErrorStatus es;
      int result = 0;
    int entityToErase = -1;
    AcArray<AcDbEntity*> crossSectionCurves;
    AcDbEntity* pEntity = NULL;
    for(int input = 0; input < 2; input++)
    {
        ads_name  ename;
        ads_point ptres;
        acedInitGet(0, _T("Point"));
        result = acedEntSel
                (
                    _T("\nSelect CrossSection curve [Point] <Curve>: "),
                    ename,
                    ptres
                );
          if (result == RTKWORD)
        {
            CString strKeyWord;
            result = acedGetInput(strKeyWord.GetBuffer(50));
            if (result == RTNORM)
            {
                if (strKeyWord == _T("Point"))
                {
                    ads_point pt;
                    result = acedGetPoint
                                (
                                    NULL,
                                    L"\nSpecify point location:",
                                    pt
                                );
                    if(result != RTNORM)
                        return;
                       AcGeMatrix3d ucs;
                     acedGetCurrentUCS(ucs);
                     AcGePoint3d wcsPt
                         = asPnt3d(pt).transformBy(ucs);
                     AcDbObjectId entId = AcDbObjectId::kNull;
                     AcDbPoint *pPoint = new AcDbPoint(wcsPt);
                     postToDb(pPoint, &entId);
                       es = acdbOpenObject(
                                            pEntity,
                                            entId,
                                            AcDb::kForWrite,
                                            Adesk::kFalse
                                        );
                     crossSectionCurves.append(pEntity);
                     entityToErase = input;
                }
            }
        }
        else if(result == RTNORM)
        {
            AcDbObjectId profileCurveId = AcDbObjectId::kNull;
            es = acdbGetObjectId(profileCurveId, ename);
              es = acdbOpenObject(
                                    pEntity,
                                    profileCurveId,
                                    AcDb::kForRead,
                                    Adesk::kFalse
                                );
            crossSectionCurves.append(pEntity);
        }
        else
            return;
    }
      // Create the loft surface
    AcDbLoftedSurface *pSurf = new AcDbLoftedSurface();
    AcArray<AcDbEntity*> guideCurves;
    AcDbLine *pPathCurve = NULL;
    AcDbLoftOptions loftOptions;
      es = pSurf->createLoftedSurface
                                (
                                    crossSectionCurves,
                                    guideCurves,
                                    pPathCurve,
                                    loftOptions
                                );
    if (es == Acad::eOk)
    {
        pSurf->setColorIndex(2);
        postToDb(pSurf, NULL);
    }
    else
        delete pSurf;
      for(int cnt = 0; cnt < crossSectionCurves.length(); cnt++)
    {
        AcDbEntity *pTempEntity = crossSectionCurves.at(cnt);
        if(cnt == entityToErase)
            pTempEntity->erase();
        pTempEntity->close();
    }
}
  static void postToDb( AcDbEntity* pEnt, AcDbObjectId *pOid)
{
    AcDbBlockTable* pBlockTable;
    AcDbDatabase *pDb
        = acdbHostApplicationServices()->workingDatabase();
    pDb->getBlockTable(pBlockTable, AcDb::kForRead);
      AcDbBlockTableRecord* pModelSpaceBTR =  NULL;
    pBlockTable->getAt
                    (
                        ACDB_MODEL_SPACE,
                        pModelSpaceBTR,
                        AcDb::kForWrite
                    );
      AcDbObjectId oid = AcDbObjectId::kNull;
    if(pOid != NULL)
    {
        pModelSpaceBTR->appendAcDbEntity(*pOid, pEnt);
    }
    else
    {
        pModelSpaceBTR->appendAcDbEntity(oid, pEnt);
    }
    pEnt->close();
      pModelSpaceBTR->close();
    pBlockTable->close();
}

## 评论

**内容**: petcon said...
what is lofted surface
Reply
05/07/2012 at 10:04 PM

---
**内容**: Balaji said...
Simply put :
You can choose two curves that define the end cross-sections. A surface will be created such that the transition between the different cross-sections are considered.
Here is a more detailed explanation from the AutoCAD help :
http://docs.autodesk.com/ACD/2010/ENU/AutoCAD%202010%20User%20Documentation/index.html?url=WS1a9193826455f5ffa23ce210c4a30acaf-685c.htm,topicNumber=d0e95526
Hope this helps.
Reply
05/07/2012 at 10:10 PM

---
