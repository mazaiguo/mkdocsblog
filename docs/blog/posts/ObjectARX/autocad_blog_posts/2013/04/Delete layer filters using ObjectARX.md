---
title: "Delete layer filters using ObjectARX"
date: 2013-04-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - Layer
  - ObjectARX
description: "I have a customer who uses many dwgs with many filters on the layer. How can I delete the filters using a program?"
author: Autodesk
---
# Delete layer filters using ObjectARX

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/delete-layer-filters-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
I have a customer who uses many dwgs with many filters on the layer. How can I delete the filters using a program?
Solution
Layer filters exist as AcDbXRecord entries in two dictionaries (with name "ACAD_LAYERFILTERS" and "ACLYDICTIONARY") contained in the extension dictionary of Layer Table. To delete the layer filters, you need to iterate through the "ACAD_LAYERFILTERS" and "ACLYDICTIONARY" dictionaries and delete all AcDbXRecords.
The code below opens a dummy drawing and deletes all layer filters inside of the drawing:
static void ASDKLayerFilterDelete_DeleteLayerFilters(void)
{
  // Set constructor parameter to kFalse so that the
  // database will be constructed empty.  This way only
  // what is read in will be in the database.
  AcDbDatabase *pDb = new AcDbDatabase(Adesk::kFalse);
    // The AcDbDatabase::readDwgFile() function
  // automatically appends a DWG extension if it is not
  // specified in the filename parameter.
  pDb->readDwgFile(_T("c:\\drawing1.dwg"));
  // ensure the whole dwg is read
  pDb->closeInput(true);
    // Get the Layer Table
  AcDbLayerTablePointer pLyrTbl(pDb->layerTableId(), AcDb::kForRead);
  if (pLyrTbl.openStatus() == Acad::eOk)
  {
    // Get Extention dictionary
    AcDbObjectId pExtDicId = pLyrTbl->extensionDictionary();
      if(pExtDicId.isValid())
    {        
      AcDbDictionaryPointer pDict(pExtDicId,AcDb::kForRead);
      if(Acad::eOk == pDict.openStatus())
      {
        // Get Layer Filter Dictionary from extension dictionary
        AcDbObjectId pObjId;
        pDict->getAt(_T("ACAD_LAYERFILTERS"),pObjId);
          if(pObjId.isValid())
        {
          AcDbDictionaryPointer pFiltDict(pObjId,AcDb::kForRead);
            if(Acad::eOk == pFiltDict.openStatus())
          {
            // Get objects in layer filter dictionary
            AcDbObjectId filtObjId;
            AcDbDictionaryIterator *pItr = pFiltDict->newIterator();
            if (NULL != pItr)
            {
              for(;!pItr->done();pItr->next())
              {
                AcDbObjectPointer<AcDbXrecord> pLyrFltr(pItr->objectId(),AcDb::kForWrite);
                if(Acad::eOk == pLyrFltr.openStatus())
                {
                  pLyrFltr->erase();
                }
              }
              delete pItr;
            }
          }
        }    
          pDict->getAt(_T("ACLYDICTIONARY"),pObjId);
            if(pObjId.isValid())
        {
          AcDbDictionaryPointer pFiltDict(pObjId,AcDb::kForRead);
          if(Acad::eOk == pFiltDict.openStatus())
          {
            // Get objects in layer filter dictionary
            AcDbObjectId filtObjId;
              AcDbDictionaryIterator *pItr = pFiltDict->newIterator();
            if(NULL != pItr)
            {
              for(;!pItr->done();pItr->next())
              {
                AcDbObjectPointer<AcDbXrecord> pLyrFltr(pItr->objectId(),AcDb::kForWrite);
                if(Acad::eOk == pLyrFltr.openStatus())
                {
                  pLyrFltr->erase();
                }       
              }
              delete pItr;
            }
          }    
        }
      }
    }  
  } 
    Acad::ErrorStatus es = pDb->saveAs(_T("c:\\drawing1.dwg"));
  delete pDb; 
}

