---
title: "Plotting A Window To DWF using ObjectARX COM and LISP"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - COM
  - ObjectARX
  - Plot
description: "I want to Window plot a drawing to DWF, I'm using COM to plot the DWF but how do I setup the Plot Settings so that it plots using a couple of Windo..."
author: Autodesk
---
# Plotting A Window To DWF using ObjectARX COM and LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/plotting-a-window-to-dwf-using-objectarx-com-and-lisp.html

## 文章内容

By Fenton Webb
Issue
I want to Window plot a drawing to DWF, I'm using COM to plot the DWF but how do I setup the Plot Settings so that it plots using a couple of Window coordinates?
Solution
In ObjectARX you need to use the AcDbPlotSettingsValidator class to setup the Plot. Here is some code which shows you what to do. Note this is using the Window coordinates as the extents of the drawing. This is purely for test purposes - if you want to plot the extents then use setPlotType (pLayout, AcDbPlotSettings::kExtents). There is also a Visual LISP example following the ObjectARX code.
#import "acax19ENU.tlb" no_namespace
#include "acaplmgr.h"
static void ASDKTS66871_PlotWindow_COM_testPlot(void)
{
  // Use ActiveX interface to get the application object
  IAcadApplicationPtr pAcad = acedGetAcadWinApp()->GetIDispatch(FALSE);
    //get the path to plotter configuration
  _bstr_t szPrinterPath;
  szPrinterPath = pAcad->Preferences->GetFiles()->GetPrinterConfigPath() + _bstr_t("\\DWF6 ePlot.pc3");
  // get the current database
  AcDbDatabase *curDocDB = acdbHostApplicationServices()->workingDatabase();
  // get a pointer to the layout manager
  AcApLayoutManager *pLayoutManager = (AcApLayoutManager *)acdbHostApplicationServices()->layoutManager();
  const ACHAR *layoutName = pLayoutManager->findActiveLayout (true);
  // get the current layout
  AcDbLayout *pLayout = pLayoutManager->findLayoutNamed (layoutName, true); 
  // if we got it ok
  if (pLayout != NULL)
  {
    Acad::ErrorStatus es;
    // get the plotsetttings class
    AcDbPlotSettingsValidator *pPlotSettingsValidator = acdbHostApplicationServices()->plotSettingsValidator();
    // if we got it ok
    if (pPlotSettingsValidator != NULL)
    {
      // Refresh the layout lists in order to use it
      pPlotSettingsValidator->refreshLists (pLayout);
      // change the current layout plotter
      es = pPlotSettingsValidator->setPlotCfgName (pLayout, szPrinterPath);  
      // set the window to plot as the extents of the drawing
      es = pPlotSettingsValidator->setPlotWindowArea (pLayout,
        curDocDB->extmin ().x,
        curDocDB->extmin ().y,
        curDocDB->extmax ().x,
        curDocDB->extmax ().y);
      // set the orgin
      es = pPlotSettingsValidator->setPlotOrigin (pLayout,
        curDocDB->extmin ().x,
        curDocDB->extmin ().y);
      // set to plot centred
      es = pPlotSettingsValidator->setPlotCentered (pLayout, true);
      // setup the plot type to window
      es = pPlotSettingsValidator->setPlotType (pLayout, AcDbPlotSettings::kWindow);
      // set the scale
      es = pPlotSettingsValidator->setStdScaleType (pLayout, AcDbPlotSettings::StdScaleType::kScaleToFit);
        // we have to close the layout here because the last parameter of
      // findLayoutNamed is true, leave layout open
      pLayout->close ();
    } 
  }
      // get the current document
  IAcadDocumentPtr pDoc = pAcad->GetActiveDocument();
  // create a plot object
  IAcadPlotPtr pPlot = pDoc->GetPlot();
  // lets plot
  pPlot->PlotToFile("c:\\test.dwf", szPrinterPath);
}
  Note: You do not necessarily need to use COM to plot. Instead you can use ObjectARX functions. A good sample ships with the ObjectARX 2009 SDK. ( ..\ObjectARX 2009\samples\editor\AsdkPlotAPI )
Here is a Visual LISP example:
(defun c:testPlotWindow ( / acadObject acadDocument activeLayoutObject plt p1 point1
     pPt1 pPt1sa pt1 p2 point2 pPt2 pPt2sa pt2 )
  (vl-load-com)
  (setq acadObject (vlax-get-Acad-object))
  (setq acadDocument (vla-get-ActiveDocument acadObject))
  (setq activeLayoutObject (vla-Get-ActiveLayout acadDocument))
  (setq plt (vla-get-plot acadDocument))
  (vla-put-configname activeLayoutObject "DWF6 ePlot.pc3")
  (vla-put-canonicalmedianame
    activeLayoutObject
    "ISO_full_bleed_A3_(420.00_x_297.00_MM)"
    )
  (vla-put-paperunits activeLayoutObject acMillimeters)
  (vla-put-plotrotation activeLayoutObject ac0degrees)
  ; How to control the Plot Style Table
  ; (vla-put-StyleSheet activeLayoutObject "HP LaserJet 4MV.ctb")
  (setq p1 (getpoint "\nSelect Window Point No 1 (Lower Left): "))
  (setq point1 (list (car p1) (cadr p1)))
  (setq pPt1 (vlax-make-safearray vlax-vbDouble '(0 . 1)))
  (setq pPt1sa (vlax-safearray-fill pPt1 point1))
  (setq pt1 (vlax-make-variant
       pPt1sa
       (logior vlax-vbarray vlax-vbDouble)
       )
)
  (setq p2 (getpoint "\nSelect Window Point No 2 (Upper Right): "))
  (setq point2 (list (car p2) (cadr p2)))
  (setq pPt2 (vlax-make-safearray vlax-vbDouble '(0 . 1)))
  (setq pPt2sa (vlax-safearray-fill pPt2 point2))
  (setq pt2 (vlax-make-variant
       pPt2sa
       (logior vlax-vbarray vlax-vbDouble)
       )
)
  (vla-SetWindowToPlot activeLayoutObject pt1 pt2)
  (vla-put-plottype activeLayoutObject acWindow)
   (vla-plottofile plt "c:\\test.dwf" "DWF6 ePlot.pc3")
  )

