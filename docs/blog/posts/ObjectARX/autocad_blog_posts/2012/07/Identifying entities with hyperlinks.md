---
title: "Identifying entities with hyperlinks"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "The entities which contain the hyperlinks will have an xdata called “PEURL”. So you can use “SelectAll’ API with xdata filter to get all the entiti..."
author: Autodesk
---
# Identifying entities with hyperlinks

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/identifying-entities-with-hyperlinks.html

## 文章内容

By Virupaksha Aithal
The entities which contain the hyperlinks will have an xdata called “PE_URL”. So you can use “SelectAll’ API with xdata filter to get all the entities with hyperlinks. Refer below code.
[CommandMethod("HyperLinkCount")]
public void HyperLinkCount()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      TypedValue[] tvs = new TypedValue[1];
    tvs[0] = new TypedValue((int)DxfCode.ExtendedDataRegAppName,
                                                        "PE_URL");
      SelectionFilter filter = new SelectionFilter(tvs);
    PromptSelectionResult acSSPrompt = ed.SelectAll(filter);
      if (acSSPrompt.Status == PromptStatus.OK)
    {
        ed.WriteMessage(acSSPrompt.Value.Count.ToString());
          ObjectId[] ids = acSSPrompt.Value.GetObjectIds();
        using (Transaction Tx =
                      db.TransactionManager.StartTransaction())
        {
            foreach (ObjectId id in ids)
            {
                Entity ent = Tx.GetObject(id,
                                        OpenMode.ForRead) as Entity;
                  HyperLinkCollection HyperCollection = ent.Hyperlinks;
                foreach (HyperLink link in HyperCollection)
                {
                    ed.WriteMessage(link.Name + "\n");
                }
            }
        }
    }
}

