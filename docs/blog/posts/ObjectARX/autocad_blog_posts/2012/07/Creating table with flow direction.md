---
title: "Creating table with flow direction"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "You can use API “setFlowDirection” to set the direction of the table entity in AutoCAD. Table can be top to bottom or bottom to top. Below code sho..."
author: Autodesk
---
# Creating table with flow direction

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/creating-table-with-flow-direction.html

## 文章内容

By Virupaksha Aithal
You can use API “setFlowDirection” to set the direction of the table entity in AutoCAD. Table can be top to bottom or bottom to top. Below code shows the procedure to create a table with bottom to top direction.
void TableTest()
{
    AcDbTable *pTable = new AcDbTable();
      //  Get the table style
    //
    AcDbDictionary *pDict = NULL;
    AcDbObjectId styleId;
      AcDbDatabase *pDb =
      acdbHostApplicationServices()->workingDatabase();
      pDb->getTableStyleDictionary(pDict,AcDb::kForRead);
    Acad::ErrorStatus es = pDict->getAt(_T("Standard"), styleId);
    pDict->close();
      // Set the table style Id
    pTable->setTableStyle(styleId);
      //5 row, 6 columns
    pTable->setSize(5, 6);
      //Flow Direction From Bottom To Top
    pTable->setFlowDirection(AcDb::kBtoT);
      // Generate the table layout based on the table style
    pTable->generateLayout(); 
      pTable->setPosition(AcGePoint3d::kOrigin);
      AcDbObjectId modelId;
    modelId = acdbSymUtil()->blockModelSpaceId(pDb);
      AcDbBlockTableRecord *pBlockTableRecord;
    es = acdbOpenAcDbObject((AcDbObject*&)pBlockTableRecord,
                                    modelId, AcDb::kForWrite);
      if(es == Acad::eOk)
    {
        // Add to Db
        AcDbObjectId objectId;
        pBlockTableRecord->appendAcDbEntity(objectId, pTable);
          pBlockTableRecord->close();
        pTable->close();
    }
    else
    {
        delete pTable;
    }
}

