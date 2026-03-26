---
title: "MLeader may throw eInvalidContext exception"
date: 2014-08-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Unicode
description: "The MLeader object (and the equivalent AcDbMLeader in C++) support a block as the text component, as described at this previous blog post. One of t..."
author: Autodesk
---
# MLeader may throw eInvalidContext exception

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/mleader-may-throw-einvalidcontext-exception.html

## 文章内容

By Augusto Goncalves
The MLeader object (and the equivalent AcDbMLeader in C++) support a block as the text component, as described at this previous blog post. One of the required steps is set the BlockPosition property (or setBlockPosition in C++), but this may throw eInvalidException.
In fact this exception is expected if the extents of the block cannot be defined, for instance, if there are invisible attributes defined on it.
To avoid this, simply set the MLeader points with AddLeaderLine and/or AddFirsVertex before setting the block data.

## 评论

**内容**: Gofatw said...
We are using C# and this is starting to popup in the last few months. Has something changed in the API to cause this? Assigning the block contents after the assigning AddLeaderLine and AddFirstVertext and/or LastVertex no longer seems to help.
Anything else to help fix this?
Reply
01/16/2020 at 02:44 PM

---
**内容**: Madhukar Moogala said in reply to Gofatw...
Tried this code, I’m able to attach Block Content to MLeader correctly, may I know the problem you are facing ?

public static void BlockMLeader()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
using (Transaction Tx = db.TransactionManager.StartTransaction())
{
BlockTable table = Tx.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
BlockTableRecord model = Tx.GetObject(table[BlockTableRecord.ModelSpace], OpenMode.ForWrite)
as BlockTableRecord;
if (!table.Has("BlkLeader"))
{
ed.WriteMessage("\nYou need to define a \"BlkLeader\" first...");
return;
}
MLeader leader = new MLeader();
leader.SetDatabaseDefaults();
leader.ContentType = ContentType.BlockContent;
leader.BlockContentId = table["BlkLeader"];
leader.BlockPosition = new Point3d(4, 2, 0);
int idx = leader.AddLeaderLine(new Point3d(1, 1, 0));
leader.AddFirstVertex(idx, new Point3d(0, 0, 0));
int AttNumber = 0;
BlockTableRecord blkLeader = Tx.GetObject(leader.BlockContentId, OpenMode.ForRead)
as BlockTableRecord;
Matrix3d Transfo = Matrix3d.Displacement(leader.BlockPosition.GetAsVector());
foreach (ObjectId blkEntId in blkLeader)
{
AttributeDefinition AttributeDef = Tx.GetObject(blkEntId, OpenMode.ForRead)
as AttributeDefinition;
if (AttributeDef != null)
{
AttributeReference AttributeRef = new AttributeReference();
AttributeRef.SetAttributeFromBlock(AttributeDef, Transfo);
AttributeRef.Position = AttributeDef.Position.TransformBy(Transfo);
AttributeRef.TextString = "Attrib #" + (++AttNumber);
leader.SetBlockAttribute(blkEntId, AttributeRef);
}
}
model.AppendEntity(leader);
Tx.AddNewlyCreatedDBObject(leader, true);
Tx.Commit();
}
}
Reply
01/21/2020 at 02:01 AM

---
