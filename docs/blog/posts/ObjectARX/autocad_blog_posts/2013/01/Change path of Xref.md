---
title: "Change path of Xref"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - XREF
description: "The following code snippet shows how to change the path of all the Xrefs in a given drawing, to point to a new location. The code sample runs recur..."
author: Autodesk
---
# Change path of Xref

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/change-path-of-xref.html

## 文章内容

By Gopinath Taget
The following code snippet shows how to change the path of all the Xrefs in a given drawing, to point to a new location. The code sample runs recursively to change the paths of the Xref even in the nested Xrefs. This code is useful in situations where the Xrefed drawings are being migrated from one folder/server to another folder/server. For complete VC++ ARX project download the attachment.
/////////////////////////////////////////////////////////////
//Description: fGetXYPlane
//1)Call this from ARX defined command
/////////////////////////////////////////////////////////////
void fTest()
{
acutPrintf(_T("\nTrying to change the paths of XREFs..."));
 //feel free to change the path as required
fXrefRePath(_T("c:\\test.dwg"),_T("c:\\newlocation\\"));
}
  ///////////////////////////////////////////////////////////////
//Description: fGetXYPlane
//Parameters:
//a)pDwgPath: Drawing name to repath the XREFs
//b)pNewLocation: The new folder where the XREF are available
//c)nDepth: Do not use. It specifies the nest level. It is
//optional and is used while running recursively
///////////////////////////////////////////////////////////////
void fXrefRePath(const TCHAR* pDwgPath,
 const TCHAR* pNewLocation,long nDepth)
{
 //preparing the prefix
TCHAR mPrefix[255];
   if (1 < nDepth)
{
  mPrefix[nDepth] = _T('\0');
}
 else
{
  mPrefix[0] = _T('\0');
}
  AcDbBlockTable *pBT;
AcDbBlockTableRecord *pBTR;
AcDbBlockTableIterator *pBTIter;
  AcDbDatabase *pDB = new AcDbDatabase(Adesk::kFalse);
Acad::ErrorStatus mEs;
  mEs = pDB->readDwgFile(pDwgPath);
   if(Acad::eOk != mEs)
{
  acutPrintf(_T("\n%sError: reading database: %s"),
   mPrefix,pDwgPath);
  delete pDB;
  return;
}
  pDB->getBlockTable(pBT,AcDb::kForRead);
pBT->newIterator(pBTIter);
pBT->close();
   const TCHAR *pOldPathName;
TCHAR *pNewPathName = new TCHAR[255];
   //path buffers
TCHAR mOldDrive[_MAX_DRIVE];
TCHAR mOldDir[_MAX_DIR];
TCHAR mOldFname[_MAX_FNAME];
TCHAR ext[_MAX_EXT];
  TCHAR mNewDrive[_MAX_DRIVE];
TCHAR mNewDir[_MAX_DIR];
TCHAR mNewFname[_MAX_FNAME];
TCHAR mNewExt[_MAX_EXT];
  acutPrintf(_T("\n%s-%s"),mPrefix,pDwgPath);
   while(!pBTIter->done())
{
  if(Acad::eOk != pBTIter->getRecord(pBTR,AcDb::kForRead))
   continue;
    if (pBTR->isFromExternalReference())
  {
   //changing the path name
   pBTR->pathName(pOldPathName);
     //split the old location
   _wsplitpath_s(pOldPathName, mOldDrive,
    mOldDir, mOldFname, ext);
     //split the new location
   //file name and ext not used
   //and is not expected to be supplied
   _wsplitpath_s(pNewLocation, mNewDrive,
    mNewDir, mNewFname, mNewExt);
     _wmakepath_s(pNewPathName, MAX_PATH,mNewDrive,
    mNewDir, mOldFname, ext);
     //break if unable to upgrade to write
   if(Acad::eOk != pBTR->upgradeOpen()) break;
   mEs = pBTR->setPathName(pNewPathName);
     //recurse to update all the drawings that
   //are refered too
   fXrefRePath(pNewPathName,pNewLocation,nDepth+1);
  }
    pBTR->close();
  pBTIter->step();
  }
   //save the changes
 if(Acad::eOk != pDB->saveAs(pDwgPath))
  acutPrintf(_T("\n%sError: unable to save the changes to %s "),
  mPrefix,pDwgPath);
   //clean up
 delete pBTIter;
 delete pDB;
}

