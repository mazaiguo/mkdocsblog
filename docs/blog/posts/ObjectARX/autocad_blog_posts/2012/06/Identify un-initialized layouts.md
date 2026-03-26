---
title: "Identify un-initialized layouts"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "One way to identify the un- initialized layout is check the number of viewports in the layout. If the number of viewports are greater than 0, then ..."
author: Autodesk
---
# Identify un-initialized layouts

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/identify-un-initialized-layouts.html

## 文章内容

By Virupaksha Aithal
One way to identify the un- initialized layout is check the number of viewports in the layout. If the number of viewports are greater than 0, then layout is initialized. Refer below sample code
[CommandMethod("Testlayout")]
public static void Testlayout()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DBDictionary dic = Tx.GetObject(db.LayoutDictionaryId,
                                   OpenMode.ForRead) as DBDictionary;
          Layout layout = null;
        foreach (DBDictionaryEntry entry in dic)
        {
            layout = Tx.GetObject(entry.Value,
                                         OpenMode.ForRead) as Layout;
              if (!layout.ModelType)
            {
                ObjectIdCollection ids = layout.GetViewports();
                  if (ids.Count == 0)
                {
                    ed.WriteMessage(layout.LayoutName +
                            " is not initialized\n");
                }
                else
                {
                    ed.WriteMessage(layout.LayoutName +
                            " is initialized\n");
                }
            }           
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Igor said...
I have a 2015 dwg file where some layouts contains entities + viewports, but the GetVieports function gives me empty collection. Is this behaviour planed?
Once you switch to a layout, GetVieports should return one viewport permanently. or am I wrong?
Reply
02/16/2017 at 03:01 AM

---
**内容**: Maxence DELANNOY said...
You can not use Layout.GetViewports() to find if a layout is initialized because it returns an empty collection if the layout has never been activated. It is explained in the docs.
You can use Database.GetViewport(bGetPaperspaceVports: true) to get all the viewports in the drawing. After that, you can find the layout of each viewport: get the owner BlockTableRecord with viewport.BlockId, then you have a property LayoutId which allow you to match the viewport to its layout.
Reply
02/26/2020 at 09:37 AM

---
