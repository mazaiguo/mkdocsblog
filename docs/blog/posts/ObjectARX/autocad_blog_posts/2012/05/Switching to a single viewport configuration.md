---
title: "Switching to a single viewport configuration"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
description: "If there are multiple model-space viewports and to switch to a single model-space viewport configuration, you could use the -VPORTS command and spe..."
author: Autodesk
---
# Switching to a single viewport configuration

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/switching-to-a-single-viewport-configuration.html

## 文章内容

By Balaji Ramamoorthy
If there are multiple model-space viewports and to switch to a single model-space viewport configuration, you could use the -VPORTS command and specify the SI option.
For example :
acedCommand(RTSTR, L".-VPORTS", RTSTR, L"SI", RTNONE);
The other way to do this is to erase the viewport table records. When there are multiple model space viewports, you will find the same number of viewport table records in the viewport table. They all have the same name. To switch to a single viewport, all the viewports except one may be erased and the last remaining viewport can be set to cover the whole area.
Here is a sample code :
Acad::ErrorStatus es = acedVports2VportTableRecords();
AcDbDatabase* pDb
            = acdbHostApplicationServices()->workingDatabase();
  AcDbViewportTable* pVportTable = NULL;
es = pDb->getViewportTable(pVportTable, AcDb::kForRead);
if(es == Acad::eOk)
{
    int vpCnt = 0;
    AcDbViewportTableIterator *pIter = NULL;
    es = pVportTable->newIterator(pIter);
    if(es == Acad::eOk)
    {
        for (;!pIter->done();pIter->step())
        {
            AcDbViewportTableRecord *pVTR = NULL;
            es = pIter->getRecord(pVTR, AcDb::kForRead);
            if(es == Acad::eOk)
            {
                const TCHAR* vtrname;
                if(pVTR->getName(vtrname) == Acad::eOk)
                {
                    if (_tcscmp(vtrname, ACRX_T("*Active"))==0)
                    {
                        vpCnt++;
                    }
                }
                pVTR->close();
            }
        }
        delete pIter;
    }
      for(int x = 0; x < vpCnt-1; x++)
    {
        AcDbViewportTableRecord *pVTR = NULL;
        es = pVportTable->getAt(
                                    ACRX_T("*Active"),
                                    pVTR,
                                    AcDb::kForWrite
                                );
        if(es == Acad::eOk)
        {
            pVTR->erase(true);
            pVTR->close();
        }
    }
      // Set the last viewport to cover the full area
    AcDbViewportTableRecord *pVTR = NULL;
    es = pVportTable->getAt(
                                ACRX_T("*Active"),
                                pVTR,
                                AcDb::kForWrite
                            );
    if(es == Acad::eOk)
    {
        AcGePoint2d ll, ur;
        ll.set(0,0);
        ur.set(1,1);
        pVTR->setCenterPoint(AcGePoint2d(0, 0));
        pVTR->setHeight(100);
        pVTR->setWidth(100);
        pVTR->setViewDirection(AcDb::kTopView);
        pVTR->setLowerLeftCorner(ll);
        pVTR->setUpperRightCorner(ur);
        pVTR->close();
    }
    pVportTable->close();
}
es = acedVportTableRecords2Vports();

## 评论

**内容**: David said...
Hello Balaji.
Thanks for the Post.
Can you please show us(with code ) how to change a none rectangular paperspace viewport customscale and view center , when user is in model space .
I have several layout tabs and on each layout have several non rectangular viewports and need to change view center and zoomfactor of just one of them.
I am struggle for one week.
Thanks
David
Reply
12/11/2012 at 10:50 AM

---
