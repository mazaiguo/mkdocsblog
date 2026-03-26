---
title: "How to create MLeader objects in .Net?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
  - Database
  - Unicode
description: "Below are two samples that illustrates MLeader creation in C#:"
author: Autodesk
---
# How to create MLeader objects in .Net?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-create-mleader-objects-in-net.html

## 文章内容

By Philippe Leefsma
  Below are two samples that illustrates MLeader creation in C#:
The first creates a MLeader with a MText content:
  [CommandMethod("netTextMLeader")]
public static void netTextMLeader()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable table = Tx.GetObject(
            db.BlockTableId,
            OpenMode.ForRead)
                as BlockTable;
          BlockTableRecord model = Tx.GetObject(
            table[BlockTableRecord.ModelSpace],
            OpenMode.ForWrite)
                as BlockTableRecord;
          MLeader leader = new MLeader();
        leader.SetDatabaseDefaults();
          leader.ContentType = ContentType.MTextContent;
          MText mText = new MText();
        mText.SetDatabaseDefaults();
        mText.Width = 100;
        mText.Height = 50;
        mText.SetContentsRtf("MLeader");
        mText.Location = new Point3d(4, 2, 0);
          leader.MText = mText;
          int idx = leader.AddLeaderLine(new Point3d(1, 1, 0));
        leader.AddFirstVertex(idx, new Point3d(0, 0, 0));
          model.AppendEntity(leader);
        Tx.AddNewlyCreatedDBObject(leader, true);
          Tx.Commit();
    }
}
  The second creates a MLeader with a Block content. It also handles the case where the MLeader block contains attributes and set them to a default value:
  [CommandMethod("netBlockMLeader")]
public static void netBlockMLeader()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable table = Tx.GetObject(
            db.BlockTableId,
            OpenMode.ForRead)
                as BlockTable;
          BlockTableRecord model = Tx.GetObject(
            table[BlockTableRecord.ModelSpace],
            OpenMode.ForWrite)
                as BlockTableRecord;
          if (!table.Has("BlkLeader"))
        {
            ed.WriteMessage(
                "\nYou need to define a \"BlkLeader\" first...");
            return;
        }
          MLeader leader = new MLeader();
        leader.SetDatabaseDefaults();
          leader.ContentType = ContentType.BlockContent;
          leader.BlockContentId = table["BlkLeader"];
        leader.BlockPosition = new Point3d(4, 2, 0);
          int idx = leader.AddLeaderLine(new Point3d(1, 1, 0));
        leader.AddFirstVertex(idx, new Point3d(0, 0, 0));
          //Handle Block Attributes
        int AttNumber = 0;
        BlockTableRecord blkLeader = Tx.GetObject(
            leader.BlockContentId,
            OpenMode.ForRead)
                as BlockTableRecord;
          //Doesn't take in consideration oLeader.BlockRotation
        Matrix3d Transfo = Matrix3d.Displacement(
            leader.BlockPosition.GetAsVector());
          foreach (ObjectId blkEntId in blkLeader)
        {
            AttributeDefinition AttributeDef = Tx.GetObject(
                blkEntId,
                OpenMode.ForRead)
                    as AttributeDefinition;
              if (AttributeDef != null)
            {
                AttributeReference AttributeRef =
                    new AttributeReference();
                  AttributeRef.SetAttributeFromBlock(
                    AttributeDef,
                    Transfo);
                  AttributeRef.Position =
                    AttributeDef.Position.TransformBy(Transfo);
                  AttributeRef.TextString = "Attrib #" + (++AttNumber);
                  leader.SetBlockAttribute(blkEntId, AttributeRef);
            }
        }
          model.AppendEntity(leader);
        Tx.AddNewlyCreatedDBObject(leader, true);
          Tx.Commit();
    }
}

## 评论

**内容**: nav said...
Hi thanks for the great article.
I have one question if I want to use built in source blocks like Box, Circle, detail callout,etc as blockcontent how I access them from drawing.
thanks
Reply
06/02/2014 at 06:03 AM

---
**内容**: Philippe Leefsma said in reply to nav...
I'm not sure what you mean, there is no such thing as built-in blocks like box or circle, those are entities that can be inserted inside a block. So if the block already exist, you have to use its ObjectId that can be found if you know the block name, this is pretty much what is exposed in that sample. Otherwise you may have to create the block on the fly and insert whatever entities you want inside it. We have multiple samples on that blog that should help you create a block.
Reply
06/04/2014 at 03:59 AM

---
