---
title: "Creating a anonymous Layer"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Layer
description: "To create anonymous Layer, you need to call “AcDbLayerTable::setIsHidden()” API as shown in below code. Anonymous layers are not shown in layer man..."
author: Autodesk
---
# Creating a anonymous Layer

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-a-anonymous-layer.html

## 文章内容

By Virupaksha Aithal
To create anonymous Layer, you need to call “AcDbLayerTable::setIsHidden()” API as shown in below code. Anonymous layers are not shown in layer manager and hence users can not edit/delete the setting of anonymous layers.
void CreateAnonymousLayer()
{
    AcDbObjectId layerId = AcDbObjectId::kNull;
    AcDbLayerTable* lTable = NULL;
      AcDbDatabase *pDb = acdbHostApplicationServices()->
                                        workingDatabase();
      Acad::ErrorStatus es =
                pDb->getSymbolTable(lTable, AcDb::kForWrite);
      if(Acad::eOk == es && lTable)
    {
          AcDbLayerTableRecord* lTblRec =
                new AcDbLayerTableRecord();
          lTblRec->setName(ACRX_T("TEST"));
            lTblRec->setIsHidden(true);
            if (lTable->add(layerId, lTblRec) != Acad::eOk)
              ::acutPrintf(_T("ERROR Creating Layer\n"));
          else
            lTblRec->close();
            lTable->close();
    }
  }
.NET
  [CommandMethod("Hiddenlayer")]
public void Hiddenlayer()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   using (Transaction tr =
        db.TransactionManager.StartTransaction())
 {
     LayerTable table =
     tr.GetObject(db.LayerTableId, OpenMode.ForWrite) as LayerTable;
       LayerTableRecord Anonymous = new LayerTableRecord();
     Anonymous.Name = "Test";
     Anonymous.IsHidden = true;
         table.Add(Anonymous);
     tr.AddNewlyCreatedDBObject(Anonymous, true);
     tr.Commit();
   }
}

## 评论

**内容**: Maxence DELANNOY said...
Documentation on this topic is broken in the Managed Class Reference Guide. For the properties IsHidden and IsLoked, the description is "Assesses if the layer is frozen."
Reply
05/31/2012 at 01:48 AM

---
