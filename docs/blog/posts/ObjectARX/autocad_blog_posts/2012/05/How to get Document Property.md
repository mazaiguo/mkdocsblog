---
title: "How to get Document Property"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
description: "If you want to access the document property as DWGPROPS does, you will need to use acdbGetSummaryInfo. that is a global function to retrieve file i..."
author: Autodesk
---
# How to get Document Property

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-get-document-property.html

## 文章内容

By Xiaodong Liang
If you want to access the document property as DWGPROPS does, you will need to use acdbGetSummaryInfo. that is a global function to retrieve file information.
  void testCmd()
{
      // assume a drawing is opened
      AcDbDatabaseSummaryInfo *pSummaryInfo = NULL;
    if (Acad::eOk !=
        acdbGetSummaryInfo(acdbHostApplicationServices()
        ->workingDatabase(),
        pSummaryInfo))
        {  return; }
      for(int i = 0;
        i < pSummaryInfo->numCustomInfo();
        i++)
    {
        // get custom properties
       ACHAR *pName, *pValue;
       pSummaryInfo->getCustomSummaryInfo(i,pName, pValue);
        acutPrintf(L"\nKey: %s, Value = %s",pName, pValue);
    }
      acdbFree(pSummaryInfo);
}

