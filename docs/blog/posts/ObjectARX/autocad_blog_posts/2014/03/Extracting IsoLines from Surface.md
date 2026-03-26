---
title: "Extracting IsoLines from Surface"
date: 2014-03-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Surface
description: "Here is a sample code to extract IsoLines along the U and V directions of a surface. The extracted curves are added to the database."
author: Autodesk
---
# Extracting IsoLines from Surface

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/extracting-isolines-from-surface.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to extract IsoLines along the U and V directions of a surface. The extracted curves are added to the database.
// 1) Enable support for the BRep API in StdAfx.h
#define _BREP_SUPPORT_            //- Support for the BRep API
  // 2) Code to retrieve the IsoLines from a surface
Acad::ErrorStatus es;
  ads_point pt;
ads_name ename;
if (RTNORM != acedEntSel(L"Select a Surface", ename, pt))
    return;
  AcDbEntity *pEnt = NULL;
AcDbObjectId id;
es = acdbGetObjectId(id, ename);
es = acdbOpenAcDbEntity(pEnt, id, AcDb::kForWrite);
AcDbSurface *pSurface = AcDbSurface::cast(pEnt);
if(NULL == pSurface)
{
    acutPrintf(ACRX_T("\nPlease select a surface."));
    return;
}
  AcDbNurbSurfaceArray nsArray;
es = pSurface->convertToNurbSurface(nsArray);
if(es == Acad::eOk)
{
    if(nsArray.length() == 1)
    {
        AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
          AcDbBlockTable *pBlockTable = NULL;
        es = pDb->getBlockTable(pBlockTable, AcDb::kForRead);
          AcDbBlockTableRecord *pMS = NULL;
        es = pBlockTable->getAt(
                       ACDB_MODEL_SPACE, pMS, AcDb::kForWrite);
          AcDbNurbSurface *pNS = NULL;
        pNS = AcDbNurbSurface::cast(nsArray.at(0));
          Adesk::UInt16 uIsoDensity = pSurface->uIsolineDensity();
        Adesk::UInt16 vIsoDensity = pSurface->vIsolineDensity();
          AcDbBody* pBody = new AcDbBody();
          es = pBody->setASMBody(pSurface->getLockedASMBody());
          AcBr::ErrorStatus ebs;
        AcBrBrep* pBrep = new AcBrBrep();
        ebs = pBrep->set(*pBody);
        if(AcBr::eOk == ebs)
        {
            AcBrBrepFaceTraverser* pFaceTrav
                                = new AcBrBrepFaceTraverser;
            ebs = pFaceTrav->setBrep(*pBrep);
            if(AcBr::eOk == ebs)
            {
                for(pFaceTrav->restart();
                        !pFaceTrav->done();pFaceTrav->next())
                {
                    AcBrFace face;
                    ebs = pFaceTrav->getFace(face);
                    if(AcBr::eOk == ebs)
                    {
                        AcGeSurface *pGeSurface;
                        ebs = face.getSurface(pGeSurface);
                          Adesk::Boolean isClosedInU
                                  = pGeSurface->isClosedInU();
                          Adesk::Boolean isClosedInV
                                  = pGeSurface->isClosedInV();
                          int ucMax = uIsoDensity+2;
                        if(isClosedInU)
                            ucMax = uIsoDensity;
                          int vcMax = vIsoDensity+2;
                        if(isClosedInV)
                            vcMax = vIsoDensity;
                          AcGeInterval intervalU, intervalV;
                        pGeSurface->getEnvelope
                                       (intervalU, intervalV);
                          double boundMinU = 0.0,
                               boundMaxU = 0.0,
                               boundMinV = 0.0,
                               boundMaxV = 0.0;
                          intervalU.getBounds
                                       (boundMinU, boundMaxU);
                          intervalV.getBounds
                                       (boundMinV, boundMaxV);
                          double paramIncrU =
                        (boundMaxU - boundMinU) /
                        (isClosedInU ? uIsoDensity :
                                       (uIsoDensity+1));
                          double paramIncrV =
                        (boundMaxV - boundMinV) /
                        (isClosedInV ? vIsoDensity :
                                       (vIsoDensity+1));
                          double paramU = boundMinU;
                        for(int uc = 0; uc < ucMax; uc++)
                        {
                            double paramV = boundMinV;
                            for(int vc = 0; vc < vcMax; vc++)
                            {
                                AcArray<AcDbCurve*> uIsoLines;
                                es = pNS->getIsolineAtU(
                                           paramU, uIsoLines);
                                  if(es == Acad::eOk)
                                {
                                    for(int cnt = 0;
                                        cnt < uIsoLines.length();
                                        cnt++)
                                    {
                                        AcDbCurve *pCurve
                                            = uIsoLines[cnt];
                                          pCurve->setColorIndex(1);
                                          pMS->appendAcDbEntity
                                                     (pCurve);
                                          pCurve->close();
                                    }
                                }
                                  AcArray<AcDbCurve*> vIsoLines;
                                es = pNS->getIsolineAtV(
                                           paramV, vIsoLines);
                                  if(es == Acad::eOk)
                                {
                                    for(int cnt = 0;
                                        cnt < vIsoLines.length();
                                        cnt++)
                                    {
                                        AcDbCurve *pCurve
                                             = vIsoLines[cnt];
                                          pCurve->setColorIndex(1);
                                          pMS->appendAcDbEntity
                                                     (pCurve);
                                          pCurve->close();
                                    }
                                }
                                  paramV += paramIncrV;
                            }
                            paramU += paramIncrU;
                        }
                    }
                    else
                    {
                        acutPrintf(
                              ACRX_T("\nSorry, BRep error."));
                          break;
                    }
                }
            }
            else
            {
                acutPrintf(ACRX_T("\nSorry, BRep error."));
            }
              delete pFaceTrav;
        }
        else
        {
            acutPrintf(ACRX_T("\nSorry, BRep error."));
        }
          delete pBrep;
          es = pMS->close();
        es = pBlockTable->close();
    }
    else
    {
        acutPrintf(ACRX_T("\nSorry, this code cannot handle
                               multiple Nurb surfaces yet."));
    }
      // Cleanup
    for(int cnt = 0; cnt < nsArray.length(); cnt++)
    {
        AcDbNurbSurface *pNS = NULL;
        pNS = AcDbNurbSurface::cast(nsArray.at(cnt));
        if(pNS != NULL)
        {
            delete pNS;
        }
    }
}
else
{
    acutPrintf(
        ACRX_T("\nSorry, could not convert to Nurb surface."));
}
  pSurface->close();
Here is a screenshot of the IsoLines extracted from a revolved surface

## 评论

**内容**: Charles said...
Hello, nice code!! How can I make it run?
Reply
12/30/2015 at 06:51 AM

---
**内容**: utku demir said...
Hello Dear Sir,
Code look like incredible.. But copy paste to notepad and saving .lsp than holding and dropping into autocad occurs an error look like this `extra right paren on input`
I decided to check the lisp from vlisp than at this time i`m getting this error `:CALLBACK-ENTRY` (debug- break an error checked!)
And another question is command name brep ?
I hope you can help us for correctly runing this lisp because it`s so important for us.
Thank you & Best Regards
Reply
04/26/2016 at 01:21 AM

---
**内容**: Rudy said...
Hello,
The help file says AcBrFace::getSurface(pSurface) instantiates the memory.
Shouldn't it be deleted after use?
Also, I can't find clarity on who is responsible for the the memory use of
AcGeExternalBoundedSurface::getBaseSurface(AcGeSurface*& surfaceDef);
The help file does not specify.
Is it newly instantiated and can I safely delete it?
Thanks,
Rudy
Reply
03/21/2018 at 03:11 PM

---
**内容**: Getae said...
What a waste of time this code is. Why people even bother to post something like that? Do they think they look smarter? They look dumber way way dumber.
Reply
03/10/2019 at 06:16 PM

---
