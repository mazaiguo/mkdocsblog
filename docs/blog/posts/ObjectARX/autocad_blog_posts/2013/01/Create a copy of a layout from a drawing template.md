---
title: "Create a copy of a layout from a drawing template"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
  - Database
  - ObjectARX
description: "The AutoCAD User Interface will allow you to create a new layout based on a layout in a drawing template. You can replicate this behavior using Obj..."
author: Autodesk
---
# Create a copy of a layout from a drawing template

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-a-copy-of-a-layout-from-a-drawing-template.html

## 文章内容

By Gopinath Taget
The AutoCAD User Interface will allow you to create a new layout based on a layout in a drawing template. You can replicate this behavior using ObjectARX. To do this, load the drawing template in memory and get the pointer to the required layout. The copyFrom()method of the AcDbLayout class is then used to copy the layout properties to a new layout in the current drawing.
The following code sample shows how to copy a layout named "Layout1" to the current drawing from a drawing template. Note that there is minimal error checking for code brevity:
void f_createLayoutFromDwt()
{
Acad::ErrorStatus mEs;
AcDbDatabase *pDWTdb = new AcDbDatabase(false);
   if (Acad::eOk == pDWTdb->readDwgFile(
  L"D:\\Autodesk\\autocadmap4\\Template\\test.dwt"))
{
  //get the layout dictionary
  AcDbDictionary *pDict = NULL;
  pDWTdb->getLayoutDictionary(pDict,AcDb::kForRead);
    AcDbObject *pObj = NULL;
  AcDbLayout *pSrcLayout = NULL;
  AcDbLayout *pNewLayout = NULL;
    //assuming you want to copy the layout
  //"Layout1" from the drawing template
  //or you can use the AcDbDictionaryIterator
  //to get the required AcDbLayout from the database
  mEs = pDict->getAt(L"Layout1",pObj,AcDb::kForWrite);
  //close the dictionary
  pDict->close();
    if(mEs == Acad::eOk)
  {
   pSrcLayout = AcDbLayout::cast(pObj);
   //add new layout to the current document
   AcApLayoutManager *pLayoutMan =
   (AcApLayoutManager *)acdbHostApplicationServices()->
          layoutManager();
     AcDbObjectId pLayoutID,pBTRId;
     //get the name to create a new layout
   ACHAR* psName;
   psName = pLayoutMan->getNextNewLayoutName();
     //create a new layout
   pLayoutMan->createLayout(psName,pLayoutID,pBTRId);
   pNewLayout = pLayoutMan->findLayoutNamed(psName,TRUE);  
   //copy from the source layout in to the new layout
   pNewLayout->copyFrom(pSrcLayout);
     //open the new layout object to refresh the list
   //this required to refresh the device list
   pNewLayout->upgradeOpen();
   AcDbPlotSettingsValidator *pPltValid = NULL;
   pPltValid =
    acdbHostApplicationServices()->plotSettingsValidator();
   pPltValid->refreshLists(pNewLayout);
     //close the layouts
   pNewLayout->close();
   pSrcLayout->close();
     //update the layout tabs using the layout manager
   pLayoutMan->updateLayoutTabs();
  }
}
 delete pDWTdb;
}

