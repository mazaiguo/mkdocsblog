---
title: "Identifying whether dim style is Annotative or not"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Dimension
description: "Each Annotative dimension style will have an Xdata with name “AcadAnnotative”. This presence of particular xdata can be used to identify whether di..."
author: Autodesk
---
# Identifying whether dim style is Annotative or not

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/identifying-whether-dim-style-is-annotative-or-not.html

## 文章内容

By Virupaksha Aithal
Each Annotative dimension style will have an Xdata with name “AcadAnnotative”. This presence of particular xdata can be used to identify whether dim style is Annotative or not
[CommandMethod("DimStyleAnnotative")]
public void DimStyleAnnotative()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DimStyleTable dimStyleTable = Tx.GetObject(
                                       db.DimStyleTableId,
                                  OpenMode.ForRead) as DimStyleTable;
          foreach (ObjectId id in dimStyleTable)
        {
            DimStyleTableRecord style = Tx.GetObject(id,
                            OpenMode.ForRead) as DimStyleTableRecord;
            ResultBuffer xdata =
                       style.GetXDataForApplication("AcadAnnotative");
              if (xdata != null)
            {
                ed.WriteMessage("dim style " +
                                    style.Name + " is Annotative\n");
                  xdata.Dispose();
            }
            else
            {
                ed.WriteMessage("dim style " +
                                style.Name + " is non Annotative\n");
            }
        }
          Tx.Commit();
    }
  }

