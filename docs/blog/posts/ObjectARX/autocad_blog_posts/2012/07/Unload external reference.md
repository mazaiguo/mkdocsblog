---
title: "Unload external reference"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - XREF
description: "You need to use database API “UnloadXrefs” API to unload the external reference. Below code shows the procedure to unload one external reference."
author: Autodesk
---
# Unload external reference

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/unload-external-reference.html

## 文章内容

By Virupaksha Aithal
You need to use database API “UnloadXrefs” API to unload the external reference. Below code shows the procedure to unload one external reference.
[CommandMethod("XREFUnload")]
static public void XREFUnload()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
          new PromptEntityOptions("\nSelect a external Reference");
    options.SetRejectMessage("\nSelect only external References");
    options.AddAllowedClass(typeof(BlockReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      ObjectId xrefId = ObjectId.Null;
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the BlockReference
        BlockReference blockref = Tx.GetObject(acSSPrompt.ObjectId,
                                OpenMode.ForRead) as BlockReference;
        //get the definiation
        BlockTableRecord block = (BlockTableRecord)Tx.GetObject(
                         blockref.BlockTableRecord, OpenMode.ForRead);
          //check if it is a external reference.
        if (block.IsFromExternalReference)
        {
            xrefId = block.ObjectId;
        }
        else
        {
            ed.WriteMessage("block is not a external reference\n");
        }
          Tx.Commit();
    }
      if (xrefId != ObjectId.Null)
    {
        ObjectIdCollection collection = new ObjectIdCollection();
        collection.Add(xrefId);
        db.UnloadXrefs(collection);
    }
}

## 评论

**内容**: SteveO said...
Hi Virupaksha,
This is very handy for me, and I can use it to reload xrefs too! What code would I use to detect if the current xref is unloaded?
Reply
10/03/2012 at 08:57 AM

---
