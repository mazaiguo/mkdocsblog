---
title: "Programmatically using acedgrdraw for temporary graphics in all viewports"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I want to draw some temporary lines in all the model space viewports, but acedGrDraw draws only in the current viewport. How can I draw programmati..."
author: Autodesk
---
# Programmatically using acedgrdraw for temporary graphics in all viewports

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/programmatically-using-acedgrdraw-for-temporary-graphics-in-all-viewports.html

## 文章内容

By Xiaodong Liang
Issue
I want to draw some temporary lines in all the model space viewports, but acedGrDraw draws only in the current viewport. How can I draw programmatically do this in all viewports?
Solution
You need to use acedVports(...) to retrieve the active viewports, and then loop in acedSetVar("CVPORT"...) before setting acedGrDraw.
This is the only method for doing because you cannot reliably use AcDbViewportTableRecords that have the name "*ACTIVE". In addition, you cannot use them to retrieve the viewport numbers required by acedSetVar.
The following sample code demonstrates how the DRAWALLVP command selects a line. Red lines are drawn to indicate the mid segment of lines that are segmented into thirds.
To remove the temporary graphics, use REDRAWALL command.
#include "dbxutil.h"
#include "geassign.h"
#include <vector>
static void asdkDrawAllVP()
{
struct resbuf rb;
  acedGetVar(L"TILEMODE", &rb);
  if(rb.resval.rint == 0)  
  { 
   acutPrintf(L"\nSorry, cannot do it in the PAPER Space!");  
   return; 
  }
  // // Select a line
  ads_point   adsPt;
  ads_name    adsName;
  AcDbObjectId     id;
  AcDbLine*   pLine;
  if(acedEntSel(L"\nSelect a Line: ", adsName, adsPt) != RTNORM)  
  {
   acutPrintf(L"\nLine not selected!");  
   return;
  }
  acdbGetObjectId(id, adsName);
  if(acdbOpenObject(pLine, id, AcDb::kForRead) != Acad::eOk)
  { 
   acutPrintf(L"\nNot a line or cannot open the line for read!");  
   return; 
  } // Get line's "one third" and "two thirds" points in WCS
  AcGePoint3d p3dThrd1 = pLine->startPoint() +0.33333*(pLine->endPoint()).asVector() -0.33333*(pLine->startPoint()).asVector();
  AcGePoint3d p3dThrd2 = pLine->startPoint() +0.66667*(pLine->endPoint()).asVector() -0.66667*(pLine->startPoint()).asVector();
  pLine->close();
  // // Get all active viewports //
  struct resbuf *pRbVports = NULL;
  if(acedVports(&pRbVports) != RTNORM) 
  { 
   acutPrintf(L"\nError in acedVports!");
   return;  
  }
  std::vector<int> ivecVport;
  ivecVport.reserve(5);
  // // Loop the result buffer and store viewport numbers in the vector
  // while(pRbVports) 
  {
   // Skip RTLB  
   pRbVports = pRbVports->rbnext;
   // Store viewport number 
   if(pRbVports->restype != RTSHORT) 
   {  
    acutPrintf(L"\nError in pRbVports: RTSHORT expected!"); 
    return;   
   }  
   ivecVport.push_back(pRbVports->resval.rint); 
   // Skip LowerLeft Point, UpperRight Point and RTLE 
   pRbVports = pRbVports->rbnext;  
   pRbVports = pRbVports->rbnext; 
   pRbVports = pRbVports->rbnext;
   pRbVports = pRbVports->rbnext;
  }
  acutRelRb(pRbVports);
  //     // Loop all viewports to draw the line //
  AcGePoint3d  p3dUCS1, p3dUCS2;
  for(int iVP=0; iVP<ivecVport.size(); ++iVP)
  {
   // Set Current Viewport 
   rb.restype = RTSHORT;  
   rb.resval.rint = ivecVport[iVP];
   acedSetVar(L"CVPORT",&rb);
   // Transform points to UCS  
   acdbWcs2Ucs(asDblArray(p3dThrd1),
    asDblArray(p3dUCS1), Adesk::kFalse);
   acdbWcs2Ucs(asDblArray(p3dThrd2), asDblArray(p3dUCS2), Adesk::kFalse); 
   // Draw the line 
   acedGrDraw(asDblArray(p3dUCS1), asDblArray(p3dUCS2), 1, 0);  
  }
  // // Re-set original viewport //
  rb.restype = RTSHORT;
  rb.resval.rint = ivecVport[0];
  acedSetVar(L"CVPORT",&rb);
  return;
}

