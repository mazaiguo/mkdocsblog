---
title: "Iterate block table records to make a selection set of block references on a particular layout"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Selection
description: "How do I get all block references on a particular layout, such as "Layout1"?"
author: Autodesk
---
# Iterate block table records to make a selection set of block references on a particular layout

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/iterate-block-table-records-to-make-a-selection-set-of-block-references-on-a-particular-layout.html

## 文章内容

By Xiaodong Liang
Issue
How do I get all block references on a particular layout, such as "Layout1"?
Solution
These steps show how this can be done:
1. Iterate through AcDbBlockTables and get the AcDbBlockTableRecords.
2. Check to see if AcDbBlockTableRecord is a layout using AcDbBlockTableRecord::isLayout(). If the AcDbBlockTableRecord is of type layout,then get its Id, open the layout using the Id and get the name of the layout.
3. When you have retrieved the required name, create an iterator for that AcDbBlockTableRecord.
4. Cycle through all entities for the layout. If the entity type is AcDbBlockReference, add it to the selection set. The sample code shown below demonstrates how to select all AcDbBlockReferences on the layout named "Layout1".
  void findBlokRefInLayout(void)
{
  ads_name ss;
  acedSSAdd(NULL,NULL,ss);
    Acad::ErrorStatus es;
  es=selectBlocksOnLayout(_T("Layout1"), ss);
  if (es != Acad::eOk)
  {
   acutPrintf(_T("Error selecting blocks on Layout1"));
   return;
  }
  long len;
  acedSSLength(ss,&len);
  acutPrintf(_T("\nNo. of blocks selected on Layout1= %ld"),len);
  acedSSFree(ss);        
}
    // help function: find the layout and
// the blockreferenes within it
Acad::ErrorStatus selectBlocksOnLayout(ACHAR *lname ,
                                              ads_name& ss  )
{
    //select all blocks on Layout1
    Acad::ErrorStatus es;
    AcDbBlockTable *pBT;
    es=acdbHostApplicationServices()->workingDatabase()
            ->getSymbolTable(pBT,
                    AcDb::kForRead);
    if (es!= Acad::eOk)
        return es;
      AcDbBlockTableIterator* pIter;
    es=pBT->newIterator(pIter);
    if (es!= Acad::eOk)
    {
        pBT->close();
        return es;
    }
      for(; !pIter->done(); pIter->step())
    {
        AcDbBlockTableRecord* pBTR;
        es=pIter->getRecord(pBTR, AcDb::kForRead);
        if (es!= Acad::eOk)
        {
            pBT->close();
            delete pIter;
            return es;
        }
          // if this is a layout
        if(pBTR->isLayout())
        {
            AcDbObjectId layoutId = pBTR->getLayoutId();
            AcDbLayout *pLayout;
            es=acdbOpenAcDbObject((AcDbObject*&)pLayout,
                                    layoutId,
                                 AcDb::kForRead);
            if (es!= Acad::eOk)
            {
                pBT->close();
                delete pIter;
                pBTR->close();
                return es;
            }
              // get name of the layout
            ACHAR* pName;
            es=pLayout->getLayoutName(pName);
            if (es!= Acad::eOk)
            {
                pBT->close();
                delete pIter;
                pBTR->close();
                pLayout->close();
                return es;
            }
            es=pLayout->close();
            if (es!= Acad::eOk)
            {
                pBT->close();
                delete pIter;
                pBTR->close();
                return es;
            }
              // if this is "layout1"
            if (wcscmp(lname, pName)==0)
            {
                AcDbBlockTableRecordIterator* pBtblrIter;
                es=pBTR->newIterator(pBtblrIter);
                if (es!= Acad::eOk)
                {
                    pBT->close();
                    delete pIter;
                    pBTR->close();
                    pLayout->close();
                    return es;
                }
                  // iterate the entities within the layout
                for(;!pBtblrIter->done();pBtblrIter->step())
                {
                    AcDbEntity* pEnt;
                    es=pBtblrIter->getEntity(pEnt,
                                        AcDb::kForRead);
                    if (es!= Acad::eOk)
                    {
                        pBT->close();
                        delete pIter;
                        pBTR->close();
                        pLayout->close();
                        delete pBtblrIter;
                        return es;
                    }
                      // if this is a block reference
                    if(pEnt->isKindOf
                        (AcDbBlockReference::desc()))
                    {
                        AcDbObjectId objId;
                        pBtblrIter->getEntityId(objId);
                        ads_name eName;
                        acdbGetAdsName(eName,objId);
                        acedSSAdd(eName,ss,ss);
                        // highlight it
                        pEnt->highlight();
                    }
                      es=pEnt->close();
                    if (es!= Acad::eOk)
                    {
                        pBT->close();
                        delete pIter;
                        pBTR->close();
                        pLayout->close();
                        delete pBtblrIter;
                        return es;
                    }
                  }
                delete pBtblrIter;
            }
        }
        es=pBTR->close();
        if (es!= Acad::eOk)
        {
            pBT->close();
            delete pIter;
            return es;
        }
    }
    es=pBT->close();
    delete pIter;
    return es;

