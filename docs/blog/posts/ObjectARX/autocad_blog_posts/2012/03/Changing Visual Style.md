---
title: "Changing Visual Style"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "Here is a code snippet to change the visual style using the AutoCAD .Net API :"
author: Autodesk
---
# Changing Visual Style

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/changing-visual-style-using-autocad-net-api.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to change the visual style using the AutoCAD .Net API :
[CommandMethod("ChangeVisualStyle")]
public static void changeVisualStyleMethod()
{
    Document activeDoc =
        Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
    String visualStyleName = "Realistic";
    try
    {
        using(Transaction tr =
           db.TransactionManager.StartTransaction())
        {
            ViewportTable vt = tr.GetObject(
              db.ViewportTableId,
              OpenMode.ForRead)as ViewportTable;
            ViewportTableRecord vtr =
              tr.GetObject(vt["*Active"],
              OpenMode.ForWrite)as ViewportTableRecord;
            DBDictionary dict = tr.GetObject(
                        db.VisualStyleDictionaryId,
                        OpenMode.ForRead) as DBDictionary;
              vtr.VisualStyleId = dict.GetAt(visualStyleName);
            tr.Commit();
        }
        ed.UpdateTiledViewportsFromDatabase();
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}
  Here is the ObjectARX equivalent of the code with minimal error checking
static void AdsProjectChangeVS(void)
{
    Acad::ErrorStatus es = Acad::eOk;
    AcDbDatabase* pDb
            = acdbHostApplicationServices()->workingDatabase();
      AcDbViewportTable* pVportTable = NULL;
    es = pDb->getViewportTable(pVportTable, AcDb::kForRead);
      AcDbViewportTableRecord *pVportTableRec = NULL;
    es = pVportTable->getAt(
                                ACRX_T("*Active"),
                                pVportTableRec,
                                AcDb::kForWrite
                            );
      AcDbDictionaryPointer pNOD (
                                    pDb->visualStyleDictionaryId(),
                                    AcDb::kForRead
                                ) ;
    AcDbObjectId vsId = AcDbObjectId::kNull;
    pNOD->getAt(ACRX_T("Realistic"), vsId);
    pVportTableRec->setVisualStyle(vsId);
    pVportTableRec->close ();
    pVportTable->close();
      es = acedVportTableRecords2Vports();
}

## 评论

**内容**: nolan said...
hi,
the ObjectARX example only work on model space, how about the layout?
Reply
09/14/2017 at 01:23 AM

---
