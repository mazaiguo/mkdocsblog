---
title: "Setting formula in table"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "You can set the value of a cell in table to the result of a formula.  Below code shows the same. Below code sets the cell [2, 0] to formula “==A23...."
author: Autodesk
---
# Setting formula in table

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-formula-in-table.html

## 文章内容

By Virupaksha Aithal
You can set the value of a cell in table to the result of a formula.  Below code shows the same. Below code sets the cell [2, 0] to formula “==A2*3.123”.
[CommandMethod("CreateTableFormula")]
public void CreateTableFormula()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptPointOptions ppo = new
                PromptPointOptions("\nSpecify insertion point: ");
      PromptPointResult ppr = ed.GetPoint(ppo);
      if (ppr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Table table = new Table();
          table.Position = ppr.Value;
          table.InsertColumns(0, 2.0, 2);
        table.InsertRows(0, 1.0, 2);
        table.Cells[0, 0].Value = "Table Title";
        table.Cells[1, 0].Value = "1.0";
        table.Cells[2, 0].Contents.Add();
          string formula = "=A2*3.123";
        table.Cells[2, 0].Contents[0].Formula = formula;
          ObjectId ModelSpaceId =
                    SymbolUtilityServices.GetBlockModelSpaceId(db);
        BlockTable bt = Tx.GetObject(db.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
        BlockTableRecord btr = Tx.GetObject(ModelSpaceId,
                              OpenMode.ForWrite) as BlockTableRecord;
          btr.AppendEntity(table);
        Tx.AddNewlyCreatedDBObject(table, true);
        Tx.Commit();
    }
}

