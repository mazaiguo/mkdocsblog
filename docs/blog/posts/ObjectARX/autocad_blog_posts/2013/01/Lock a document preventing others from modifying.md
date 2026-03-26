---
title: "Lock a document preventing others from modifying"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - Layer
description: "If some system variables are valid on a per-document basis, such as CLAYER, and you are modifying a document, some other applications could try to ..."
author: Autodesk
---
# Lock a document preventing others from modifying

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/lock-a-document-preventing-others-from-modifying.html

## 文章内容

By Gopinath Taget
If some system variables are valid on a per-document basis, such as CLAYER, and you are modifying a document, some other applications could try to modify it at the same time before your application ends. This could cause CLAYER variable's value to be unreliable for your application. How do you prevent this from happening?
Many system variables such as CLAYER are on a per-document basis. The situation as stated can occur; to avoid this, you'll need to lock the current document that you're working on before you try to modify a per-document system variable such as CLAYER. This way, depending on the lock mode you specify, undesirable modifications can be blocked.
The following code demonstrates how you can add a layer to the current document and set it to be the current layer while preventing other documents from modifying the database. Notice that some error handling code is omitted for code brevity.
// Note: you could place the lock on a broader scope depending on
// your actual needs.
void testLock()
{
Acad::ErrorStatus es;   
 // exclusive write so only you app can write to the document 
 // before you unlock the document 
es = acDocManager->lockDocument(curDoc(), AcAp::kXWrite, NULL,
  NULL,false); 
assert(es == Acad::eOk); 
AcDbDatabase* pDb = curDoc()->database();
AcDbLayerTable* pTable;
es = pDb->getLayerTable(pTable, AcDb::kForRead);  
 const ACHAR layName[] = L"testLayer";   
AcDbLayerTableRecord* pRecord; 
 if(pTable->has(layName))
{
  es = pTable->getAt(layName, pRecord, AcDb::kForRead);   
  assert(es == Acad::eOk);
}   
 else 
{ 
  pRecord = new AcDbLayerTableRecord;   
  pRecord->setName(layName);
  pTable->upgradeOpen();
  es = pTable->add(pRecord);    
  assert(es == Acad::eOk);
} 
AcDbObjectId id = pRecord->objectId();  
pTable->close();  
pRecord->close();
es = curDoc()->database()->setClayer(id); 
assert(es == Acad::eOk);   
es = acDocManager->unlockDocument(curDoc());  
assert(es == Acad::eOk);
}

