---
title: "AcDbDictUtil utility class"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Plot
description: "AcDbDictUtil utility class functions are very handy for quick one-time access to the name or ID of a dictionary entry. Below sample shows the proce..."
author: Autodesk
---
# AcDbDictUtil utility class

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/acdbdictutil-utility-class.html

## 文章内容

By Virupaksha Aithal
AcDbDictUtil utility class functions are very handy for quick one-time access to the name or ID of a dictionary entry. Below sample shows the procedure to use AcDbDictUtil to get the layout id given its name. Similar there are function to get group, material, plotstyle etc.
void getLayout()
{
    ACHAR nameBuf[150];
    if (acedGetString(Adesk::kTrue,
        _T("\nEnter layout name to get: "), nameBuf) != RTNORM)
               return;
      AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      AcDbObjectId Id;
    Acad::ErrorStatus es = AcDbDictUtil::getLayoutId(Id, nameBuf,
                                                                pDb);
      if(es == Acad::eOk)
    {
        acutPrintf(_T("Layout %s found \n"), nameBuf);
    }
    else
    {
        acutPrintf(_T("Unabale to find layout with name %s\n"),
                        nameBuf);
    }
  }

