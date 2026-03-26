---
title: "Plotting Layouts using the ActiveX Plot Object in ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - COM
  - ObjectARX
  - Plot
description: "The sample code below, (function in the attached project) shows how plot all the layouts in batch mode using the ActiveX API in C++."
author: Autodesk
---
# Plotting Layouts using the ActiveX Plot Object in ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/plotting-layouts-using-the-activex-plot-object-in-objectarx.html

## 文章内容

By Gopinath Taget
The sample code below, (function in the attached project) shows how plot all the layouts in batch mode using the ActiveX API in C++.
The key points to batch plot layouts are:
1) Set the number of layouts be plotted using the method StartBatchMode() of the IAcadPlot object.
2) Preparing a variant array of BSTRs having the names of the layouts to be plotted and then pass it as argument to SetLayoutsToPlot() method.
3) Finally to plot, use PlotToDevice() method.
//use MFC to test this code
#import "acax19enu.tlb" raw_interfaces_only no_namespace
void fBatchPlotLayouts()
{
 try
{
  //get the AutoCAD application
  IAcadApplicationPtr pApp = NULL;
  pApp = acedGetAcadWinApp()->GetIDispatch(TRUE);
  //get the Active Document
  IAcadDocumentPtr pDoc = NULL;
  pApp->get_ActiveDocument(&pDoc);
  IAcadLayoutsPtr pLayOuts;
  IAcadLayoutPtr pLayOut;
  long mNumberOflayouts;
  //get the layouts collection and the number of layouts
  pDoc->get_Layouts(&pLayOuts);
  pLayOuts->get_Count(&mNumberOflayouts);
  //create the variant array that will hold the layout names
  VARIANT mLayArr;
  SAFEARRAYBOUND mSAB;
  mSAB.lLbound = 0;
  mSAB.cElements = mNumberOflayouts;
  VariantInit(&mLayArr);
  mLayArr.vt = VT_ARRAY | VT_BSTR;
  mLayArr.parray = SafeArrayCreate(VT_BSTR,1,&mSAB);
  //populate the variant array
  long mCtr;
  //note that array here has zero based index
  for(mCtr = 0; mCtr < mNumberOflayouts; mCtr ++)
  {
   pLayOuts->Item(_variant_t(mCtr), &pLayOut);
   BSTR strName;
   pLayOut->get_Name(&strName);
   SafeArrayPutElement(mLayArr.parray, &mCtr, strName);
  }
  //print the layout names that are being plotted
  BSTR bstrName;
  acutPrintf(_T("\nLayouts to be plotted:"));
  for(mCtr = 0; mCtr < mNumberOflayouts;mCtr ++)
  {
   SafeArrayGetElement(mLayArr.parray,&mCtr,&bstrName);
   acutPrintf(_T("\n%s"),(TCHAR*)(_bstr_t)bstrName);
  }
  acutPrintf(_T("\nPlotting started...\n"));
  //plot the layouts
  IAcadPlotPtr pPlot;
  pDoc->get_Plot(&pPlot);
  //set the number of plots and error mode to quiet
  pPlot->put_NumberOfCopies(1);
  pPlot->put_QuietErrorMode(VARIANT_TRUE);
  //number of layouts to be plotted
  pPlot->StartBatchMode(mNumberOflayouts);
  //set the layouts to plot
  pPlot->SetLayoutsToPlot(mLayArr);
  VARIANT_BOOL returnBool;
  pPlot->PlotToDevice(_variant_t("DWF6 ePlot.pc3"), &returnBool);
  //clean up
  VariantClear(&mLayArr);
}
 catch (_com_error &e)
{
  acutPrintf(
   _T("\nError while batch plotting. %s"),e.ErrorMessage());
}
}

