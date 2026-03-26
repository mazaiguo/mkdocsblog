---
title: "Iterating and Retrieving System Variable Information"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "A new API AcEdSysVarIterator is introduced in ACAD 2015, and I’m writing now when we are about to release AutoCAD 2016 [a moment of self embarrassm..."
author: Autodesk
---
# Iterating and Retrieving System Variable Information

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/iterating-and-retrieving-system-variable-information.html

## 文章内容

By Madhukar Moogala
A new API AcEdSysVarIterator is introduced in ACAD 2015, and I’m writing now when we are about to release AutoCAD 2016 [a moment of self embarrassment ].
This class “AcEdSysVarIterator” provides a way to iterate over all of the public system variables and get their names, data type, range (if applicable), read-only status, and how they are stored.
A caveat being System variables that have their secret flag set or that have a "*" as the first character in their name are skipped by this iterator. Currently we can get entire information from “SYSVDLG” including anonymous variables, this API may come handy for those who want to automate at client application.
Various other information is available on documentation.
void SysVarInfo()
{
/*Iterating through all system variables*/
AcEdSysVarIterator* pIterator = new AcEdSysVarIterator();
while (pIterator->done() != true)
{
const AcRxVariable* rxvar = pIterator->getSysVar();
acutPrintf(_T("\n********Sysvar Informataion*************"));
const AcString name = rxvar->name();
acutPrintf(_T("\nName of Sysvar : %s"),
           name.kACharPtr());
short pt = rxvar->primaryType();
acutPrintf(_T("\nPrimary Type : %d"),pt);
AcRxVariable::SecondaryType secondaryType = rxvar->secondaryType();
acutPrintf(_T("\nSecondary Type : %s"),
           getSecondaryType(secondaryType).kACharPtr());
short tf = rxvar->typeFlags();
acutPrintf(_T("\nFlags : %d"),tf);
AcRxVariable::StorageType storageType = rxvar->storageType();
acutPrintf(_T("\nStorage Type : %s"),
           getStorageType(storageType).kACharPtr());
const AcRxVariable::Range* range = rxvar->range();
  int lowerBound=-1,upperBound=-1;
if(range != nullptr)
{
lowerBound = range->lowerBound;
upperBound = range->upperBound;
}
acutPrintf(_T("\nRange of SysVar : %d  to %d"),
           lowerBound,upperBound);
bool isRO = rxvar->isReadOnly();
AcString readwrite =
isRO ? _T("Read Only") : _T("Read and Write");
  acutPrintf(_T("\nSystem Variable is : %s"),readwrite.kACharPtr());
acutPrintf(_T("\n-----------------------"));
  pIterator->step();
  }
/*resets to First sysvar*/
pIterator->reset();
delete pIterator;
}
/*Helper Functions*/
const AcString getStorageType(AcRxVariable::StorageType storageType)
{
AcString storageInfo = "";
  switch(storageType)
{
case 0:
storageInfo =
_T("Application wide, does not persist");
break;
  case 1:
storageInfo =
_T("Application wide, persists per user");
break;
case 2:
storageInfo =
_T("Application wide, persists per AutoCAD profile");
break;
case 3:
storageInfo =
_T("document wide, persists in drawing");
break;
case 4:
storageInfo =
_T("viewport (AcDbViewport and AcDbViewportTableRecord) wide, persists in drawing.");
break;
default:
break;
  }
return storageInfo;
}
  const AcString getSecondaryType(AcRxVariable::SecondaryType secondaryType)
{
AcString secondaryInfo = _T("");
switch(secondaryType)
{
case 0:
secondaryInfo =
_T("No secondary data type is specified");
break;
case 1:
secondaryInfo =
_T("The variable is a boolean. Only valid when primaryDataType==RTSHORT");
break;
case 2:
secondaryInfo =
_T("The variable is a RealDWG symbol name. Only valid when primaryDataType==RTSTR");
break;
case 3:
secondaryInfo =
_T("The variable represents area value. Only valid when primaryDataType==RTREAL");
case 4:
secondaryInfo =
_T("The variable represents distance value. Only valid when primaryDataType==RTREAL");
break;
case 5:
secondaryInfo =
_T("The variable represents an angle value. Only valid when primaryDataType==RTREAL");
break;
case 6:
if(secondaryType == AcRxVariable::kSecondaryTypeUnitlessReal)
secondaryInfo =
_T("The variable represents a unitless real value. Only valid when primaryDataType==RTREAL");
else
secondaryInfo =
_T("Marks the last item in the enumeration");
break;
default:
break;
}
return secondaryInfo;
    }
  System variable information is retrieved on command line:

