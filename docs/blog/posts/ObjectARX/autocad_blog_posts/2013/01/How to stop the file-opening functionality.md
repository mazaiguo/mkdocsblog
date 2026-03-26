---
title: "How to stop the file-opening functionality"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "Keeping AutoCAD from opening a drawing once the open command has been initiated is difficult. The solution is somewhat unorthodox, but works well."
author: Autodesk
---
# How to stop the file-opening functionality

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-stop-the-file-opening-functionality-1.html

## 文章内容

By Gopinath Taget
Keeping AutoCAD from opening a drawing once the open command has been initiated is difficult. The solution is somewhat unorthodox, but works well.
First, use an AcEditorReactor to handle the beginDwgOpen message. This handler is passed the drawing name as a string, so you can use CFile (CFile is an MFC class so you will need an MFC project for this) to rename it before AutoCAD has a chance to open it. When AutoCAD can't find find the chosen file, it responds by invoking the open-file dialog box, but we can prevent this by registering our own file-open callback function, which will be called instead. Within this callback function we can rename the drawing file back to its original name, and tell AutoCAD to behave normally the next time an open command is invoked. You can also post any message you like to the user here.
Example:
bool failOpen = true; // Global vars
TCHAR modFileName[128], originalFileName[128];
// ------------------------------------------------------------------
void ADSEdReactor::beginDwgOpen(ACHAR * filename)
{
 // Fail Open is a flag to indicate whether to abort the open...
 if(failOpen)
{
  _tcscpy(modFileName,_T("nlXXXXXX"));// global char
  _tmktemp(modFileName);// make a unique name
  _tcscpy(originalFileName,filename);// keep the original
  try
  {
   // try to rename the file
   CFile::Rename(filename,modFileName);
   // to the unique name...
  }
  catch(...)
  {
   //error renaming...abort the process
   failOpen=false;
   return;
  }
  // This will register fileOpenCB to be called when the
  // open command is issued.
  acdbHostApplicationServices()->
   registerSelectFileCallback(_T("AdskFileOpen"),
   fileOpenCB, false, true);
}
}
Acad::ErrorStatus fileOpenCB (short *userCancel, // [out]   
TCHAR*& chosenPath, // [out] 
 void* h, // HWND      
 const int nFlags,     
 const TCHAR* prompt,   
 const TCHAR* dir,    
 const TCHAR* name,
 const TCHAR* type,   
 int* pnChoice,    
 bool* pbReadOnly,
 const TCHAR* pszWSTags, 
 void* pReserved)
{
 // this is the callback function.
 if(failOpen)   
{   
  *userCancel=true;
  chosenPath=NULL;  
  // rename our file back to the 
  // original name       
  CFile::Rename(modFileName,originalFileName); 
  failOpen=false; // reset the flag  
}
 // This will tell AutoCAD to behave normally when the next open 
 // command is issued.
acdbHostApplicationServices()->
  registerSelectFileCallback(_T("AdskFileOpen"),
  fileOpenCB, true, false);
 return (Acad::eOk) ;
}

