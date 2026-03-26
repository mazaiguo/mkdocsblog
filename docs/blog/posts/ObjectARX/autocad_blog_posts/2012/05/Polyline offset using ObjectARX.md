---
title: "Polyline offset using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "Here is a sample code to offset a selected AcDbPolyline entity on either side of the selected polyline. The offset distance value is stored in a pe..."
author: Autodesk
---
# Polyline offset using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/polyline-offset-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to offset a selected AcDbPolyline entity on either side of the selected polyline. The offset distance value is stored in a per-document variable. Before presenting the code to offset an AcDbPolyline, an overview of the process follows.
In offseting an existing AcDbPolyline entity, the user is asked to select an AcDbPolyline entity and the offset distance. With these parameters, "getOffsetCurves" method is used to get the offset curve.
Before trying this code, please add a variable to the DocData class which will store the value of the offset distance as explained in the code snippet.
// In DocData.h
// A public variable to store the offset distance
ads_real m_OffsetValue;
// In DocData.cpp
// Initialize the offset distance in the constructor
CDocData::CDocData ()
{
    m_OffsetValue = 1.0;
}
Here is the command implementation :
static void ADSProject_Test(void)
{
    AcDbPolyline *pPolyEnt = NULL;
    AcDbEntity *pObj;
    AcDbPolyline *pPolyPositive = NULL;
    AcDbPolyline *pPolyNegative = NULL;
    AcDbObjectId polyEntId, ownerId;
    AcDbVoidPtrArray ar_polyPositives;
    AcDbVoidPtrArray ar_polyNegatives;
      ads_real offset = 1.0;
    ads_name eName;
    ads_point pt;
    int rc;
      rc = acedEntSel(
                        ACRX_T("\nSelect Polyline to offset "),
                        eName,
                        pt
                    );
      if(rc != RTNORM)
    {
        acutPrintf(_T("\nNothing selected "));
        return;
    }
      // Get the selected entity object ID
    acdbGetObjectId(polyEntId, eName);
      // Is the selected entity an AcDbPolyline
    acdbOpenObject(pObj, polyEntId, AcDb::kForRead);
    if(pObj == NULL)
    {
        return;
    }
      pPolyEnt = AcDbPolyline::cast(pObj);
    if(!pPolyEnt)
    {
        acutPrintf(_T("\nNot an AcDbPolyline entity "));
        pPolyEnt->close();
        return;
    }
      // Now that we have a valid AcDbPolyline entity proceed
    rc = acedGetDist(
                        NULL,
                        ACRX_T("Polyline offset distance"),
                        &offset
                    );
    switch(rc)
    {
        case RTERROR:
            acutPrintf(_T("\nError with acedGetDist() "));
            pPolyEnt->close();
            return;
            break;
          case RTCAN:
            pPolyEnt->close();
            acutPrintf(_T("\nCancelled"));
            return;
            break;
          case RTNONE:
            offset = DocVars.docData().m_OffsetValue;
            break;
          case RTNORM:
            DocVars.docData().m_OffsetValue = offset;
            break;
    }
      try
    {
        // who owns the polyline Model Space or Paper Space
        ownerId = pPolyEnt->ownerId();
        pPolyEnt->getOffsetCurves(offset, ar_polyPositives);
          //offsetPolyline(pPolyEnt, ar_polyPositives, offset);
        if(ar_polyPositives.length() != 1)
        {
            deleteArray(ar_polyPositives);
            pPolyEnt->close();
            return;
        }
        else
        {
            pPolyPositive = (AcDbPolyline*)(ar_polyPositives[0]);
            appendEntity(pPolyPositive, ownerId);
        }
          pPolyPositive->getOffsetCurves(
                                        -2.0 * offset,
                                        ar_polyNegatives
                                      );
        if(ar_polyNegatives.length() != 1)
        {
            deleteArray(ar_polyNegatives);
            pObj->close();
            return;
        }
        else
        {
            pPolyNegative = (AcDbPolyline*)(ar_polyNegatives[0]);
            appendEntity(pPolyNegative, ownerId);
        }
    }
    catch(...)
    {
        acutPrintf(ACRX_T("Sorry, Error while offsetting."));
    }
      pPolyEnt->close();
      if(pPolyPositive)
    {
        pPolyPositive->close();
    }
      if(pPolyNegative)
    {
        pPolyNegative->close();
    }
}
  static void deleteArray(AcDbVoidPtrArray entities)
{
    AcDbEntity* pEnt;
    int nEnts;
      nEnts = entities.length();
    for(int i = 0; i < nEnts; i++)
    {
        pEnt = (AcDbEntity*)(entities[i]);
        delete pEnt;
    }
}
  static void appendEntity(
                            AcDbEntity* pEnt,
                            AcDbObjectId recordId
                        )
{
    AcDbBlockTableRecord* pRecord;
    acdbOpenObject(pRecord, recordId, AcDb::kForWrite);
    pRecord->appendAcDbEntity(pEnt);
    pRecord->close();
}

## 评论

**内容**: petcon said...
wcscpy
wcscat用法是错误的应该用通用的_t函数来做
另外这个code 我没测试，考虑到了在不能偏移的情况下，会崩溃的情况么？ 粗看了下，没找到关于这个的处理
Reply
05/03/2012 at 09:50 PM

---
**内容**: Balaji said...
I have tried this in AutoCAD 2013 and it worked ok. Ofcourse, not much error handling is built-in, so you will have to modify it to include that to suit your needs.
I used Google Translate to understand your comment, but it will be helpful if you could post your comment in English.
Thanks
Reply
05/03/2012 at 09:57 PM

---
**内容**: petcon said...
never use wcscpy wcscat use _tcscpy
Reply
05/03/2012 at 10:20 PM

---
**内容**: petcon said...
use _try before getOffsetCurves otherwise sometimes u will encounter fatal error ,that will shut down ur cad
Reply
05/03/2012 at 10:23 PM

---
**内容**: petcon said...
ARX高级专业群93864243前来围观
Reply
05/03/2012 at 10:25 PM

---
**内容**: Balaji said...
Thanks for your suggestions regarding _tcscpy and a try/catch. I will update the post to use them.
Reply
05/03/2012 at 10:28 PM

---
