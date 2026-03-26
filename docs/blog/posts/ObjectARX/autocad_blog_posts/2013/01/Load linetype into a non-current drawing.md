---
title: "Load linetype into a non-current drawing"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "The code below loads linetypes starting with character 'H' from the acad.lin file into all the open documents. Note that the command should be regi..."
author: Autodesk
---
# Load linetype into a non-current drawing

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/load-linetype-into-a-non-current-drawing.html

## 文章内容

By Xiaodong Liang
The code below loads linetypes starting with character 'H' from the acad.lin file into all the open documents. Note that the command should be registered in the application context (for example, with the ACRX_CMD_SESSION flag).
void asdkgttrial()
{
   AcApDocumentIterator* pIter =
       acDocManager->newAcApDocumentIterator();
   if(!pIter)
    return;
   AcApDocument *pDocCur=curDoc();
   for(;!pIter->done();
       pIter->step())
   {
    AcApDocument *pDoc1;
    pDoc1 = pIter->document();
    acDocManager->setCurDocument(pDoc1,
                        AcAp::kWrite);
    AcDbDatabase* pDwg=pDoc1->database();
    pDwg->loadLineTypeFile(_T("H*"),
                        _T("acad.lin"));
    acDocManager->unlockDocument(pDoc1);
   }
   delete pIter;
   acDocManager->activateDocument(pDocCur);
}

