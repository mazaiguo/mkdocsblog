---
title: "Identifying active space and active layout"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "Database.CurrentSpaceId holds a objectID to current space. You can use this variable to identify whether the active space is model space or paper s..."
author: Autodesk
---
# Identifying active space and active layout

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identifying-active-space-and-active-layout.html

## 文章内容

By Virupaksha Aithal
Database.CurrentSpaceId holds a objectID to current space. You can use this variable to identify whether the active space is model space or paper space. With use of “LayoutManager”, you can identify the current layout.
[CommandMethod("ActiveSpace")]
public void ActiveSpace()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
      ObjectId SpaceId = db.CurrentSpaceId;
      //check if this is model psace.
    ObjectId ModelSpaceId =
            SymbolUtilityServices.GetBlockModelSpaceId(db);
      if (ModelSpaceId == SpaceId)
    {
        ed.WriteMessage("Model space is active\n");
    }
    else
    {
        ed.WriteMessage("Paper space is active\n");
    }
      //use layer manager to get the current layout
    LayoutManager layoutMgr = LayoutManager.Current;
      ed.WriteMessage(layoutMgr.CurrentLayout +
                                    " is current layout\n");
}

## 评论

**内容**: dsfkdjgk said...
When i use VLIDE in AUTOCAD and copy-paste this program, it doesn't work. Why is it so ????
Reply
08/20/2013 at 04:00 AM

---
