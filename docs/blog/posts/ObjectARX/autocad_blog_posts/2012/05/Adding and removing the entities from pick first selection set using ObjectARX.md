---
title: "Adding and removing the entities from pick first selection set using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - ObjectARX
  - Plugin
  - Selection
description: "You can use “acedSSSetFirst” API to set the pick first (selection with grips) selection set. The code below is a code for sample command, which pro..."
author: Autodesk
---
# Adding and removing the entities from pick first selection set using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/adding-and-removing-the-entities-from-pick-first-selection-set-using-objectarx.html

## 文章内容

By Virupaksha Aithal
You can use “acedSSSetFirst” API to set the pick first (selection with grips) selection set. The code below is a code for sample command, which prompts for entity selection and places it to pick first selection set. Code also shows a WIN32 message box, once you press OK, the selection is removed from pick first selection set. Note, the command which selects the entity with grip should have command flags set as ACRX_CMD_USEPICKSET and ACRX_CMD_REDRAW
void selectTest()
{
    int nReturn ;
    ads_name name;
    ads_point pt;
      nReturn = acedEntSel(_T("Select entity\n"), name, pt);
      if(nReturn != RTNORM)
     return;
    //get the object Id of the entity
    AcDbObjectId Id;
    if(acdbGetObjectId(Id, name) != Acad::eOk)
     return;
      //from object id to selection set
    ads_name ss, ename;
      //create a selection set
    acedSSAdd( NULL, NULL, ss );
      //get the ads name from objectID
    acdbGetAdsName( ename, Id );
      //add the selected entity ads name to selection set
    acedSSAdd( ename, ss, ss );
      //select with grip
    acedSSSetFirst( ss, NULL );
      acedSSFree( ss );
      ::MessageBox(NULL, L"Selected", L"AutoCAD", MB_OK);
    //cancel the selection
    acedSSSetFirst( NULL, NULL );
}

