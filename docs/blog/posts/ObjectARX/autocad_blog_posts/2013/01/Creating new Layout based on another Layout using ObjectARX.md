---
title: "Creating new Layout based on another Layout using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Plot
description: "In AutoCAD, I need to create a layout with all plot settings based on a"
author: Autodesk
---
# Creating new Layout based on another Layout using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/creating-new-layout-based-on-another-layout-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
In AutoCAD, I need to create a layout with all plot settings based on a
pre-existing layout in the drawing. Also, how would one create a copy of a
layout in its entirety?
Solution
Applying the plot settings of a layout is accomplished by first creating a new
layout. Then, the method AcDbPlotSettings::copyFrom() is called through the new
layout object (see createLyt() below). CloneLayout() is used to copy a layout's
properties and entities (see createClone() below). Both clone and create layout
functions take care of appending the new layout to the ACAD_LAYOUT dictionary
and establishing the layout's connections to its paperspace block table record.
It is not advisable to change the name of the layout's associated BTR (block
table record). The name is automatically assigned to be "*PAPERSPACE"
concatenated with the number N-1, where N is the number of layouts already
available. When you activate a certain layout, a swap of BTR names takes place
- the BTR associated with the layout assumes the name "*PAPERSPACE" and the BTR of the formerly active layout assumes the name of the newly active BTR. Should
you alter the name of the layout's BTR, AutoCAD will crash soon after you
attempt to activate the layout's tab.
If it is simply the plot settings you wish to transplant to a new layout…

void createLyt()
{
    Acad::ErrorStatus es;   
  AcDbObjectId LObjId, BTRId;   
  AcDbDatabase *curDocDB =acdbHostApplicationServices()->workingDatabase();   
  AcApLayoutManager *layoutMngr =
(AcApLayoutManager*)(acdbHostApplicationServices()->layoutManager());       
  curDocDB->setTilemode(Adesk::kFalse);   
  const ACHAR *actLayoutName = layoutMngr->findActiveTab();   
  AcDbLayout* pSrc = layoutMngr->findLayoutNamed(actLayoutName, TRUE);   
  if (pSrc == NULL)       
   return;       
  //pSrc must be demoted to kForRead    
  pSrc->downgradeOpen();       
  //create new layout with next available name   
  ACHAR *newLName = layoutMngr->getNextNewLayoutName();  
  if (Acad::eOk != layoutMngr->createLayout(newLName, LObjId, BTRId))
  {        acutDelString(newLName);      
  return;
  //failure   
  }   
  AcDbLayout* pTarget = layoutMngr->findLayoutNamed(newLName, TRUE);   
  acutDelString(newLName);   
  if (pTarget != NULL)
  {        
   es = pTarget->copyFrom(pSrc);       
   pSrc->close();       
   if (es != Acad::eOk)
   {       
    //unsuccessful property copy - erase new layout           
    pTarget->erase();           
    pTarget->close();       
   }
   else
   {           
    pTarget->close();           
    layoutMngr->updateLayoutTabs();       
   }   
  }
}
To clone a complete layout with properties and entities…
void createClone()
{ 
  Acad::ErrorStatus es;   
  AcDbDatabase *curDocDB =acdbHostApplicationServices()->workingDatabase();   
  AcApLayoutManager *layoutMngr =
(AcApLayoutManager*)(acdbHostApplicationServices()->layoutManager());       
  curDocDB->setTilemode(Adesk::kFalse);   
  const ACHAR *actLayoutName = layoutMngr->findActiveTab();       
  //no layout objects may be open kForWrite during getNextNewLayoutName()   
  ACHAR *cloneName = layoutMngr->getNextNewLayoutName();   
  AcDbLayout *pSrc = layoutMngr->findLayoutNamed(actLayoutName, TRUE);   
  if (pSrc == NULL)
  {       
   acutDelString(cloneName);      
   return;   
  }   
  es = layoutMngr->cloneLayout(pSrc, cloneName);   
  acutDelString(cloneName);   
  pSrc->close();   
  if (es == Acad::eOk)       
   layoutMngr->updateLayoutTabs();
}

