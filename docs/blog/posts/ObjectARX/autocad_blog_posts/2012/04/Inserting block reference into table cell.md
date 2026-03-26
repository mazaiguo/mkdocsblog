---
title: "Inserting block reference into table cell"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - Block
  - Database
description: "Below code shows the procedure to add block reference to a table cell. Code uses the “Cell. BlockTableRecordId” API to add the block reference to c..."
author: Autodesk
---
# Inserting block reference into table cell

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-insert-block-reference-into-table-cell.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to add block reference to a table cell. Code uses the “Cell. BlockTableRecordId” API to add the block reference to cell.
[CommandMethod("Table_insertBlockReference")]
static public void Table_insertBlockReference()
{
    Database db =
        Application.DocumentManager.MdiActiveDocument.Database;
    Editor ed =
        Application.DocumentManager.MdiActiveDocument.Editor;
    using (Transaction tr =
        db.TransactionManager.StartTransaction())
    {
        try
        {
            // Prompt the user to select an entity
            PromptEntityResult ers =
                        ed.GetEntity("Pick entity ");
              if (ers.Status == PromptStatus.OK)
            {
                // Open the selected entity
                Entity ent =
                    (Entity)tr.GetObject(ers.ObjectId,
                                            OpenMode.ForRead);
                if (ent is Table)
                {
                    Table table = (Table)ent;
                    BlockTable btable =
                        tr.GetObject(db.BlockTableId,
                           OpenMode.ForRead) as BlockTable;
                    if (btable.Has("test"))
                    {
                        table.UpgradeOpen();
                        //add the block reference to 1,1 cell
                        table.Cells[1, 1].BlockTableRecordId
                                            = btable["test"];
                    }
                }
                  tr.Commit();
            }
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage(ex.Message);
            tr.Abort();
        }
    }
}

