---
title: "When using Editor.SelectAll(), how can I filter entities on frozen layers out? (.NET)"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Layer
description: "If I call Editor.SelectAll(), will it return only entities currently visible on the screen?"
author: Autodesk
---
# When using Editor.SelectAll(), how can I filter entities on frozen layers out? (.NET)

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/when-using-editorselectall-how-can-i-filter-entities-on-frozen-layers-out-net.html

## 文章内容

By Marat Mirgaleev
Issue
If I call Editor.SelectAll(), will it return only entities currently visible on the screen?
Solution
No, Editor.SelectAll() returns also entities, which are placed on frozen layers. In our program we need to check whether an entity's layer is frozen. Here is a sample:
[CommandMethod("_SANF")]
public static void SelectAllExceptFrozenLayers()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
  PromptSelectionResult selection = ed.SelectAll();
  if (selection.Status == PromptStatus.OK)
  {
    using (Transaction tr =
                doc.Database.TransactionManager.StartTransaction())
    {
      foreach (ObjectId id in selection.Value.GetObjectIds())
      {
        Entity ent = (Entity)tr.GetObject(id, OpenMode.ForRead);
        LayerTableRecord layer = (LayerTableRecord)tr.GetObject(
                                    ent.LayerId, OpenMode.ForRead);
        if (!layer.IsFrozen)
          ed.WriteMessage("\n{0}", ent.ToString());
      }
      tr.Commit();
    } // using
  } // if
} // SelectAllExceptFrozenLayers()

## 评论

**内容**: Tony Tanzillo said...
I think we can do a little better than this.
First open every layer in the database, and if the layer is frozen, add its ObjectId to a HashSet. Then, while visiting entities, one only needs to check to see if the entity's LayerId property is in the HashSet, and if it is, the entity is on a frozen layer. Doing that way requires that each layer only be opened once, rather numerous times.
Reply
12/27/2012 at 01:17 AM

---
**内容**: Alexander Rivlis said in reply to Tony Tanzillo...
Also it is possible after checking all frozen layers adds all its ObjectId to filter
Reply
12/27/2012 at 02:36 AM

---
