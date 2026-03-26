---
title: "Creating a new document and activating it from a custom command"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
  - Unicode
description: "How can I create a new document and activate it from a custom command?"
author: Autodesk
---
# Creating a new document and activating it from a custom command

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/creating-a-new-document-and-activating-it-from-a-custom-command.html

## 文章内容

By Xiaodong Liang
Issue
How can I create a new document and activate it from a custom command?
Solution
There are two ways to do this:
Method #1
Register your command with ACRX_CMD_SESSION flag and use the appContextNewDocument API to create the new document. The drawback of this approach is that your command will be executed in the application context, therefore, you will need to do explicit document locking if you want to interact with any documents. Also, you cannot use acedCommand/acedCmd/acedInvoke APIs from the application context.
Method #2
Register your command with ACRX_CMD_MODAL flag and use the executeInApplicationContext API within your command handler to switch the application context.
ACED_ARXCOMMAND_ENTRY_AUTO(CArxProject3App, ArxProject3, _MyCommand2, MyCommand2, ACRX_CMD_MODAL, NULL)
 // command
static void MyARXProject_MyCommand2(void)
{        
    addDoc_By_Command_Modal();
}
static void addDoc_By_Command_Modal()
{
    // template of new drawing
     static TCHAR pData[] = _T(/*NOXLATE*/"acad.dwt");
      AcApDocument* pDoc = acDocManager->curDocument();
    if (pDoc) {
        acutPrintf(_T("\nCurrently in Document context : %s,  \
                      Switching to App.\n"),pDoc->fileName());
        acDocManager->executeInApplicationContext(
                newSyncDocHelper, (void *)pData);
    }   
}
static void
newSyncDocHelper( void *pData)
{
    // void function for executeInApplicationContext
    AcApDocument* pDoc = acDocManager->curDocument();
    if (acDocManager->isApplicationContext()) {
        acutPrintf(_T("\nSucessfully Switched to App. Context\n"));
        acDocManager->appContextNewDocument((const TCHAR *)pData);
        acutPrintf(_T("\nOpened a new document synchronously.\n"));
    } else
        acutPrintf(
        _T("\nERROR: in Document context : %s\n"),pDoc->fileName());
  }

