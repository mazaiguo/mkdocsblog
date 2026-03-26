---
title: "Creating a block with multi-line attribute definition"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Here is a sample code to create a block definition with multi-line attribute definition and to create a block reference from it."
author: Autodesk
---
# Creating a block with multi-line attribute definition

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/creating-a-block-with-multi-line-attribute-definition.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a block definition with multi-line attribute definition and to create a block reference from it.
internal static void CreateMyBlock()
{
    Database db
        = Application.DocumentManager.MdiActiveDocument.Database;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
          if (bt.Has("MyBlock") == false)
        {
            bt.UpgradeOpen();
            BlockTableRecord btr = new BlockTableRecord();
            btr.Name = "MyBlock";
            btr.Origin = Point3d.Origin;
            bt.Add(btr);
            tr.AddNewlyCreatedDBObject(btr, true);
              // Attribute Definition
            AttributeDefinition attdef
                = new AttributeDefinition
                        (
                            Point3d.Origin,
                            @"MilliSeconds\PSeconds\PMinutes",
                            "Time",
                            "Time ?",
                            db.Textstyle
                        );
            attdef.IsMTextAttributeDefinition = true;
            btr.AppendEntity(attdef);
            tr.AddNewlyCreatedDBObject(attdef, true);
        }
        tr.Commit();
    }
}
  internal static void CreateMyBlockRef()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptPointOptions ppo
        = new PromptPointOptions("\nSpecify insertion point :");
      PromptPointResult ppr = ed.GetPoint(ppo);
    if (ppr.Status != PromptStatus.OK)
        return;
      Point3d insertionPoint = ppr.Value;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt
            = db.BlockTableId.GetObject(OpenMode.ForRead) as BlockTable;
        BlockTableRecord blockDef
            = bt["MyBlock"].GetObject(OpenMode.ForRead) as BlockTableRecord;
          BlockTableRecord ms
            = bt[BlockTableRecord.ModelSpace].GetObject
                        (OpenMode.ForWrite) as BlockTableRecord;
          BlockReference blockRef
            = new BlockReference(insertionPoint, blockDef.ObjectId);
          ms.AppendEntity(blockRef);
        tr.AddNewlyCreatedDBObject(blockRef, true);
          foreach (ObjectId id in blockDef)
        {
            DBObject obj = id.GetObject(OpenMode.ForRead);
            AttributeDefinition attDef = obj as AttributeDefinition;
            if ((attDef != null) && (!attDef.Constant))
            {
                AttributeReference attRef = new AttributeReference();
                attRef.SetAttributeFromBlock
                                (
                                    attDef,
                                    blockRef.BlockTransform
                                );
                attRef.TextString = String.Format
                    (
                    @"MilliSeconds : {0}\PSeconds : {1}\PMinutes : {2}",
                    DateTime.Now.Millisecond.ToString(),
                    DateTime.Now.Second.ToString(),
                    DateTime.Now.Minute.ToString()
                    );
                  blockRef.AttributeCollection.AppendAttribute(attRef);
                tr.AddNewlyCreatedDBObject(attRef, true);
            }
        }
          tr.Commit();
    }
}
  [CommandMethod("Test")]
static public void TestMethod()
{
    CreateMyBlock();
      CreateMyBlockRef();
}

## 评论

**内容**: Juan said...
What is the command to initiate this?
Reply
09/23/2014 at 04:09 PM

---
**内容**: Kerry Brown said in reply to Juan ...
Test
Reply
09/26/2014 at 10:52 PM

---
