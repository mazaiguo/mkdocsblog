---
title: "Setting the paper size and orientation of a layout"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Plot
description: "How can I set the paper size of a layout and change the page orientation so that it is either landscape or portrait?"
author: Autodesk
---
# Setting the paper size and orientation of a layout

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/setting-the-paper-size-and-orientation-of-a-layout.html

## 文章内容

By Xiaodong Liang
Issue
How can I set the paper size of a layout and change the page orientation so that it is either landscape or portrait?
Solution
You can do this using the AcDbPlotSettingsValidator class. You can obtain a pointer to a global instance of this class with the call:
AcDbPlotSettingsValidator *pPlotSettingsValidator =
acdbHostApplicationServices()->plotSettingsValidator();
To obtain a pointer to the layout you want to change, you should first obtain a pointer to the global layout manager through the call
AcApLayoutManager *pLayoutManager = (AcApLayoutManager*)
acdbHostApplicationServices()->layoutManager();
then obtain a pointer to the layout with:

AcDbLayout *pLayout = pLayoutManager->findLayoutNamed(_T("Name"),true);
To obtain a list of the available plot settings for the layout, you can call

pPlotSettingsValidator->refreshLists(pLayout);
Then simply call the appropriate set function of AbDbPlotSettingsValidator before closing your layout. The following code shows how to set a layout's paper size to A3 Landscape.
Refer to the ObjectARX Reference Guide for a list of all the set functions provided by AcDbPlotSettingsValidator.
static void changePlotSetting()
{
     Acad::ErrorStatus es;  
     TCHAR str[125]; 
     TCHAR mediaName[] =
         _T("ISO_A3_(297.00_x_420.00_MM)"); 
     // Input layout name.
     if (acedGetString(Adesk::kTrue,
         _T("Layout to change: "),
         str)!=RTNORM)
          return;  
       // Get layout nanager pointer 
     AcApLayoutManager *pLayoutManager =
          (AcApLayoutManager*)acdbHostApplicationServices()->
                layoutManager();
     assert(pLayoutManager != NULL);
       // Get the specific layout
     AcDbLayout *pLayout =
         pLayoutManager->findLayoutNamed(str,true);
     if (pLayout == NULL)
          return;   
       // Get the plot settings validator  
     AcDbPlotSettingsValidator
         *pPlotSettingsValidator =  
     acdbHostApplicationServices()->
      plotSettingsValidator(); 
     assert( pPlotSettingsValidator != NULL );
       // Refresh the layout lists in order to use it.
     pPlotSettingsValidator->refreshLists(pLayout);
       // Set the media name to ISO_A3. If fail,
     //then set it to the fourth item inthe media name list
     es = pPlotSettingsValidator->
         setCanonicalMediaName(pLayout, mediaName);
     if( es != Acad::eOk )  
     { 
          acutPrintf(
              _T("Media name %s does not exist.  \
                 Set it to the fourth item \
                 in the media name list.\n"));
            AcArray<const TCHAR*> mediaList;  
          pPlotSettingsValidator->
       canonicalMediaNameList(pLayout, mediaList);
          es = pPlotSettingsValidator->
              setCanonicalMediaName(pLayout,mediaList[3]);  
          if( es != Acad::eOk )
          {   
         acutPrintf(_T("Fails to set the media name \
            to the fourth item in themedia\
                  name list.\n")); 
               return; 
          } 
     } 
     // AcDbPlotSettings::k0degrees is considered as portrait.
     // AcDbPlotSettings::k90degrees is considered as landscape.
     // We set it as landscape here.
     pPlotSettingsValidator->
         setPlotRotation(pLayout,AcDbPlotSettings::k90degrees);
     pLayout->close();

