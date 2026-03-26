---
title: "Inserting annotative blocks"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - DWG
description: "There are many blog posts related to insert blocks, like here. This post aims to show a simple but yet reusable sample."
author: Autodesk
---
# Inserting annotative blocks

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/inserting-annotative-blocks.html

## 文章内容

By Augusto Goncalves
There are many blog posts related to insert blocks, like here. This post aims to show a simple but yet reusable sample.
Basically to insert a block from an external drawing, it is required to insert the external .dwg into the main host .dwg, and then create a new block reference pointing to it. One additional trick is to set it annotative in case the source .dwg is already marked as annotative.
This sample is heavily based on this blog post, but jig features were removed.
[CommandMethod("createBlock")]
public static void CmdCreateBlock()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    PromptStringOptions pso =
    new PromptStringOptions(
      "\nEnter block name: ");
  PromptResult pr = ed.GetString(pso);
  if (pr.Status != PromptStatus.OK) return;
    PromptPointOptions ppo =
    new PromptPointOptions(
      "\nEntre block position: ");
  PromptPointResult ppr = ed.GetPoint(ppo);
  if (ppr.Status != PromptStatus.OK) return;
    CreateBlockReference(
    Application.DocumentManager.
    MdiActiveDocument.Database,
    pr.StringResult, ppr.Value);
}
  public static ObjectId GetBlockDefinition(
  Database db, string blockName)
{
  // Get the block definition by name
  using (Transaction trans = db.
    TransactionManager.StartTransaction())
  {
    BlockTable bt = trans.GetObject(
      db.BlockTableId, OpenMode.ForRead)
      as BlockTable;
    if (!bt.Has(blockName)) return ObjectId.Null;
    return bt[blockName];
  }
}
  // Place the reference at the model space
public static bool CreateBlockReference(
  Database db, string blockName, Point3d position)
{
  return CreateBlockReference(db,
    db.CurrentSpaceId, blockName,
    position);
}
  // Specifying the host space (e.g. model space)
public static bool CreateBlockReference(
  Database db, ObjectId hostSpaceId,
  string blockName, Point3d position)
{
  // First let's get the name of the block
  ObjectId blockDefId = GetBlockDefinition(
    db, blockName);
  bool blockDefIsAnnotative = false;
    using (Transaction trans = db.
    TransactionManager.StartTransaction())
  {
      if (blockDefId.IsNull)
    {
      // The definition with this name do not exist
      // Try insert if is a file name
      // If not possible, the file do not exist
      if (!System.IO.File.Exists(blockName)) return false;
        // Insert from external file
      using (Database sourceDb = new Database(false, true))
      {
        sourceDb.ReadDwgFile(blockName,
          FileOpenMode.OpenForReadAndAllShare,
          true, string.Empty);
        blockName = SymbolUtilityServices.RepairSymbolName(
          SymbolUtilityServices.GetSymbolNameFromPathName(
          blockName, "dwg"), false);
        blockDefId = db.Insert(blockName, sourceDb, false);
        blockDefIsAnnotative = db.AnnotativeDwg;
      }
    }
        // Create the block reference and
    BlockReference blockRef = new BlockReference(
      position, blockDefId);
    // Start annot-scale support code
    BlockTableRecord blockDef = trans.GetObject(
      blockDefId, OpenMode.ForRead) as BlockTableRecord;
      // If the source was annotative, then set the block as
    if (blockDefIsAnnotative)
    {
      blockDef.Annotative = AnnotativeStates.True;
      ObjectContextManager ocm = db.ObjectContextManager;
      ObjectContextCollection occ =
        ocm.GetContextCollection("ACDB_ANNOTATIONSCALES");
      ObjectContexts.AddContext(blockRef, occ.CurrentContext);
    }
      // If all is OK, let's go and add the
    // entity to the specified space
    BlockTableRecord hostSpace = trans.GetObject(
      hostSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    hostSpace.AppendEntity(blockRef);
    trans.AddNewlyCreatedDBObject(blockRef, true);
      // Add the attributes
    foreach (ObjectId entId in blockDef)
    {
      AttributeDefinition attDef = trans.GetObject(
        entId, OpenMode.ForRead) as AttributeDefinition;
      if (attDef == null) continue;
        // Create the attribute reference
      AttributeDefinition ad = (AttributeDefinition)attDef;
      AttributeReference ar = new AttributeReference();
      ar.SetAttributeFromBlock(ad, blockRef.BlockTransform);
      blockRef.AttributeCollection.AppendAttribute(ar);
      trans.AddNewlyCreatedDBObject(ar, true);
    }
    trans.Commit();
  }
  return true;
}

## 评论

**内容**: Sharpy said...
Hi,
Reading through this post and then trying the code out for myself, i find that if the file(block) being imported contains a AMPartRef this sometimes comes in and adds the part to the BOM and sometimes doesn't add the part to the BOM.
Is there a specific requirements on the way you handle a block definition import when a AmPartRef is concerned?
Interestingly if the Definition already exists (Via typing Insert the adding the block) The method of inserting the block reference into the drawing described above works perfectly!
Reply
09/20/2013 at 03:51 AM

---
**内容**: Augusto Goncalves said in reply to Sharpy...
Hi Sharpy,
This code is not doing anything specific to this kind of block... and I'm not sure if I got your question :)
Regards,
Augusto Goncalves
Reply
09/20/2013 at 07:29 AM

---
**内容**: Bevan Shervey (fieldguy) said...
Hi Augusto - thanks for the post. It's old but still valid.
I had to make a change for future reference. The blockDef btr has to be open for write in order to change the .Annotative property.
// Start annot-scale support code
BlockTableRecord blockDef = trans.GetObject(
blockDefId, OpenMode.ForRead) as BlockTableRecord;
*** blockDef.Annotative = AnnotativeStates.True; ***
requires blockDef open for write
Reply
06/22/2017 at 08:12 AM

---
