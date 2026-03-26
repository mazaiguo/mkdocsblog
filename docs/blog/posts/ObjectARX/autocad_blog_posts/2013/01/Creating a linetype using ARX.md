---
title: "Creating a linetype using ARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "To create a new linetype you need to create an instance of AcDbLinetypeTableRecord class and add it to the linetype table of the drawing."
author: Autodesk
---
# Creating a linetype using ARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/creating-a-linetype-using-arx.html

## 文章内容

By Gopinath Taget
To create a new linetype you need to create an instance of AcDbLinetypeTableRecord class and add it to the linetype table of the drawing.
The sample code below shows how to do this:
// Creates a new linetype and adds in to the linetype table
//-----------------------------------------------------------
static void createLinetype()
{
AcDbLinetypeTable *pLtypeTable = NULL ;
 // Get the linetype table from the drawing
 if( acdbHostApplicationServices()->workingDatabase()->
  getLinetypeTable(pLtypeTable, AcDb::kForWrite) ==Acad::eOk )
{
  AcDbLinetypeTableRecord *pLtypeTableRecord =
   new AcDbLinetypeTableRecord;
  // Set all of the properties of the linetype table record
  pLtypeTableRecord->setAsciiDescription(_T("T E S T -"));
  pLtypeTableRecord->setPatternLength(0.75);
  pLtypeTableRecord->setNumDashes(2);
  pLtypeTableRecord->setDashLengthAt(0, 0.5);
  pLtypeTableRecord->setDashLengthAt(1,-0.25);
  pLtypeTableRecord->setName(_T("T_E_S_T"));
  AcDbObjectId tmpId;
  // Add the new linetype to the linetype table
  if(pLtypeTable->add(tmpId, pLtypeTableRecord)==Acad::eOk)
  {
   pLtypeTableRecord->close();
   acutPrintf(_T("\nNew linetype successfully created."));
  }
  else
  {
   delete pLtypeTableRecord;
   acutPrintf(_T("\nCannot add new linetype to the drawing."));
  }
  pLtypeTable->close();
}
  } // end of createLinetype()

