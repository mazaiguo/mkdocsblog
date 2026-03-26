---
title: "Applypartialopenfilters(NULL,NULL) does nothing"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
description: "How do I load all entities in a partially open drawing? According to the documentation, I should call applyPartialOpenFilters(NULL,NULL), however, ..."
author: Autodesk
---
# Applypartialopenfilters(NULL,NULL) does nothing

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/applypartialopenfiltersnullnull-does-nothing.html

## 文章内容

By Xiaodong Liang
Issue
How do I load all entities in a partially open drawing? According to the documentation, I should call applyPartialOpenFilters(NULL,NULL), however, this does not load anything.
Solution
This is a known issue. You need to specify NULL for the special filter and a layer filter containing all layers of the drawing. The following code does this and loads all entities:
 static void partialLoadCommand()
{
    // Just call filterDatabase on the active database
    AcDbDatabase* pDb =
     acdbHostApplicationServices()->workingDatabase();
    if (pDb != NULL && pDb->isPartiallyOpened())
    {
        AcDbLayerFilter layerFilter;
        AcDbLayerTable* pLayerTable;
        Acad::ErrorStatus es;
        if ((es =
            pDb->getLayerTable(pLayerTable,
               AcDb::kForRead)) ==
                Acad::eOk)
        {
            AcDbLayerTableIterator* pLayerIterator;
            if ((es = pLayerTable->newIterator
                    (pLayerIterator,
                Adesk::kTrue, Adesk::kTrue)) ==
                         Acad::eOk)
            {
                for(;!pLayerIterator->done();pLayerIterator->step())
                {
                    AcDbLayerTableRecord* pL;
                    if ((es =
                        pLayerIterator->getRecord(pL,
                        AcDb::kForRead)) == Acad::eOk)
                    {
                        const ACHAR* strName;
          if ((es= pL->getName(strName))==Acad::eOk)
                            layerFilter.add(strName);
                        pL->close();
                    }
                }
                delete pLayerIterator;
            }
            pLayerTable->close();
        }
        pDb->applyPartialOpenFilters(NULL,&layerFilter);
    }
}

