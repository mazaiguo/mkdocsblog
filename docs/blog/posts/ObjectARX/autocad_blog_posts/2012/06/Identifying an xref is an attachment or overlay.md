---
title: "Identifying an xref is an attachment or overlay"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
  - XREF
description: "Blocktable record’s “IsFromOverlayReference” property helps to identify the type of reference. Refer below code, which identifies the overlay or at..."
author: Autodesk
---
# Identifying an xref is an attachment or overlay

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identifying-an-xref-is-an-attachment-or-overlay.html

## 文章内容

By Virupaksha Aithal
Blocktable record’s “IsFromOverlayReference” property helps to identify the type of reference. Refer below code, which identifies the overlay or attachment type of reference in working document.
[CommandMethod("XrefType")]
static public void XrefType()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable table = tr.GetObject(db.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
          foreach (ObjectId id in table)
        {
            BlockTableRecord record = tr.GetObject(id,
                               OpenMode.ForRead) as BlockTableRecord;
              if (record.IsFromExternalReference)
            {
                if (record.IsFromOverlayReference)
                {
                    ed.WriteMessage(record.Name
                                    + " is a overlay reference\n");
                }
                else
                {
                    ed.WriteMessage(record.Name
                                    + " is a attacment reference\n");
                }
            }
        }
          tr.Commit();
    }
  }

