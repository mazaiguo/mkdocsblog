---
title: "Close all documents including the current one"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Unicode
description: "The sample code closes all documents, including the current one by first closing all documents except the current one in the document context. The ..."
author: Autodesk
---
# Close all documents including the current one

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/close-all-documents-including-the-current-one.html

## 文章内容

By Balaji Ramamoorthy
The sample code closes all documents, including the current one by first closing all documents except the current one in the document context. The current document is then closed from the application context using the executeInApplicationContext API. This allows the current document to be closed from the same command which is running in the document context.
// Close the other documents
AcApDocumentIterator *Iter
                    = acDocManager->newAcApDocumentIterator();
while(!Iter->done())
{
    if (Iter->document()!=acDocManager->curDocument())
    {
        acDocManager->closeDocument(Iter->document());
    }
    Iter->step();
}
delete Iter;
  // Now close the current document
::acDocManagerPtr()->appContextCloseDocument
                                (acDocManager->curDocument());

