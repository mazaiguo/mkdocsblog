---
title: "Setting plot configuration name And Media Names using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Plot
description: "To query the all the available plot configurations you should use plotDeviceList() method of AcDbPlotSettingsValidator class and to get the list of..."
author: Autodesk
---
# Setting plot configuration name And Media Names using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-plot-configuration-name-and-media-names-using-objectarx.html

## 文章内容

By Virupaksha Aithal
To query the all the available plot configurations you should use plotDeviceList() method of AcDbPlotSettingsValidator class and to get the list of available media names for a given plot configuration, use canonicalMediaNameList() method AcDbPlotSettingsValidator class.
The sample code below lists the available plot configurations and asks the user to select one. After user enters his choice, all the available media are listed and user can select one to set it current.
void fSetPlotMedia()
{
 AcApLayoutManager *pLayMan = NULL;
 pLayMan = (AcApLayoutManager *)
                    acdbHostApplicationServices()->layoutManager();
 //get the active layout
 AcDbLayout *pLayout = pLayMan->findLayoutNamed(
                            pLayMan->findActiveLayout(TRUE),TRUE);
   //get the PlotSettingsValidator
 AcDbPlotSettingsValidator *pPSV =NULL;
 pPSV = acdbHostApplicationServices()->plotSettingsValidator();
 //refresh the Plot Config list
 pPSV->refreshLists(pLayout);
   //get all the Plot Configurations
 AcArray<const ACHAR *> mDeviceList;
 pPSV->plotDeviceList(mDeviceList);
   acutPrintf(_T("\nPlot Configuration List :"));
 int nLength = mDeviceList.length();
   for(int nCtr = 0;nCtr<nLength ;nCtr++)
 {
  acutPrintf(_T("\n %i) - %s"),(nCtr + 1), mDeviceList.at(nCtr));
 }
   //get the user input for listing the Media Names
 int nSel;
 int mRes =  RTNONE;
   while(RTNORM != mRes)
 {
  acedInitGet((RSG_NONULL + RSG_NONEG + RSG_NOZERO),NULL);
  mRes = acedGetInt(_T("\nSelect the Plot Configuration number: "),
                                                            &nSel);
  if (nSel > nLength)
  {
   acutPrintf(_T("\nEnter a number between 1 to %i"),nLength);
   mRes = RTNONE;
  }
 }
   //select the selected Plot configuration
 pPSV->setPlotCfgName(pLayout,mDeviceList.at(--nSel));
 //list all the paper sizes in the given Plot configuration
 AcArray<const ACHAR *> mMediaList;
 const ACHAR *pLocaleName;
 pPSV->canonicalMediaNameList(pLayout,mMediaList);
   acutPrintf(_T("\nMedia list for Plot Configuration - %s:"),
                                            mDeviceList.at(nSel));
   nLength = mMediaList.length();
 int nCtr ;
 for(nCtr = 0;nCtr<nLength ;nCtr++)
 {
  //get the localename
  pPSV->getLocaleMediaName(pLayout,mMediaList.at(nCtr),pLocaleName);
  acutPrintf(_T("\n %i)\n   Name:  %s \n   Locale Name: %s "),
                        (nCtr + 1),mMediaList.at(nCtr),pLocaleName);
 }
 mRes =  RTNONE;
 while(RTNORM != mRes)
 {
  acedInitGet((RSG_NONULL + RSG_NONEG + RSG_NOZERO),NULL);
  mRes = acedGetInt(
                _T("\nSelect the Media by entering the number: "),
                    &nSel);
    if (nSel > nLength)
  {
   acutPrintf(_T("\nEnter a number between 1 to %i"),nLength);
   mRes = RTNONE;
  }
 }
 //set selected Media for the layout
 pPSV->setCanonicalMediaName(pLayout,mMediaList.at(--nSel));
 pLayout->close();
}

## 评论

**内容**: Nick G. said...
Hi, Virupaksha.
What is the sence of your (or may be not your) code.
The same code is posted here: http://adn.autodesk.com/adn/servlet/devnote?siteID=4814862&id=6844959&linkID=4900509
May be the main reason of this blog is to make adn sources open for everybody? :):):)
1. try to add something new to this code(for example setPlotPaperUnits). My default units - MM, but if I select inches's paper size I get result in inches (but paper units within print dialog are millimeters)
2. may be it's time to create a useful function from this code :), for example
bool addLayout(
ACHAR * wantedLayoutName, // want this name for layout
double viewportWidth, // layout's viewport width
double viewportHeight, // layout's viewport height
AcGePoint2d minPtDCS, // min model point for vewport
AcGePoint2d maxPtDCS, // max model point for vewport
const ACHAR * printerName, // printer name
AcDbPlotSettings::PlotPaperUnits paperUnits, // paper units
const ACHAR * paperSize, // format
bool landscapeMode, // landscape or book mode
bool setLocked // lock viewport
)
Reply
06/11/2012 at 04:23 AM

---
**内容**: haha said...
sorry,I am not very good at English.I try to use these code fSetPlotMedia() to plot DWG,I successfully select plotDevice and Media,but after select,Autocad “Fatal Error”.I con't find the reason of the failure,I'm stuck on the question a few months.i need help ,thanks.
Reply
07/16/2018 at 09:45 PM

---
