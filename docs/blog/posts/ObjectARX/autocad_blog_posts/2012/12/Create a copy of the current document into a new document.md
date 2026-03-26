---
title: "Create a copy of the current document into a new document"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Unicode
description: "How can I have an identical copy of the current document and create it as a new document?"
author: Autodesk
---
# Create a copy of the current document into a new document

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/create-a-copy-of-the-current-document-into-a-new-document.html

## 文章内容

By Xiaodong Liang
Issue
How can I have an identical copy of the current document and create it as a new document?
Solution
One of the solution is to create a temporary drawing template file from the current database first, then create a new drawing with the template. Then delete it if necessary. Here is an outline of required steps followed by a code fragment.
1. Wblock the current open drawing.
2. Save the wblocked drawing as a template file (with a DWT extension) to a temporary location on your hard drive.
3. From the application context create a NEW document using the previously saved template file.
4. If necessary, 'remove' the temporary template file from your hard drive.
//help fuction: create a new document
void newDocHelper(void *pData)
{
   AcApDocument* pDoc = acDocManager->curDocument();
   if (acDocManager->isApplicationContext())
   {
    acDocManager->appContextNewDocument((const ACHAR *)pData);
   }
   else
   {
    acutPrintf(L"\nERROR: in Document context : %s\n",pDoc->fileName());
   }
} 
// Please note, here we are using "C:/temp.dwt" as a location
// for our temporary template file. Please change this location
// to suit your requirements as appropriate.
  void copydwg()
{
   // TODO: Implement the command
   AcDbDatabase *pDb = NULL;
   AcDbDatabase *pnewDb = NULL;
      pDb = acdbHostApplicationServices()->workingDatabase();
   assert( pDb != NULL );
     if( pDb->wblock(pnewDb) != Acad::eOk ) {
    acutPrintf(L"Couldn't wblock.\n");
    return;
   }
     if( pnewDb->saveAs(L"C:/temp.dwt") != Acad::eOk) {
    acutPrintf(L"Couldn't saveAs C:/temp.dwt file.\n");
    delete pnewDb;
    return;
   } 
   delete pnewDb;  
   static wchar_t pData[] = L"c:/temp.dwt";
   acDocManager->executeInApplicationContext(newDocHelper, (void *)pData); 
   // 'remove' is a C function to delete a file and its syntax is
    //int remove(const wchar_t *path );
     remove("c:/temp.dwt");
}
NOTE: Do not register this command with flag 'ACRX_CMD_SESSION' because
AcDbDatabase::wblock() will fail in this context.

