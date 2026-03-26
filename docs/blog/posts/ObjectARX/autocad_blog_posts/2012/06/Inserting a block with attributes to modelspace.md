---
title: "Inserting a block with attributes to modelspace"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - Block
  - C#
  - Database
  - Unicode
description: "The definition of a block is stored in a BlockTableRecord. If that block has attributes, these are stored in the BlockTableRecord as AttributeDefin..."
author: Autodesk
---
# Inserting a block with attributes to modelspace

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/inserting-a-block-with-attributes-to-modelspace.html

## 文章内容

By Stephen Preston
The definition of a block is stored in a BlockTableRecord. If that block has attributes, these are stored in the BlockTableRecord as AttributeDefinitions – just like any other entity is stored in the BlockTableRecord.
When we insert a block into a drawing (e.g. into modelspace), we insert a BlockReference. If the block has attributes, then each (non-constant) AttributeDefinition in the BlockTableRecord has a matching AttributeReference attached to the BlockReference. Constant attributes are treated slightly differently because their text is constant across all instances of the block (across all BlockReferences). They are stored in the BlockTableRecord, and there is no corresponding AttributeReference  attached to the BlockReference.
Here is some simple C# code to insert an instance of a block with attributes into model space. Create a drawing containing a block definition named “CHECK” that has several attributes (some constant, some non-constant) to test the code.
[CommandMethod("AddBlockTest")]
static public void AddBlockTest()
{
  Database db = Application.DocumentManager.MdiActiveDocument.Database;
  using (Transaction myT = db.TransactionManager.StartTransaction())
  {
    //Get the block definition "Check".
    string blockName = "CHECK";
    BlockTable bt =
        db.BlockTableId.GetObject(OpenMode.ForRead) as BlockTable;
    BlockTableRecord blockDef =
      bt[blockName].GetObject(OpenMode.ForRead) as BlockTableRecord;
    //Also open modelspace - we'll be adding our BlockReference to it
    BlockTableRecord ms =
      bt[BlockTableRecord.ModelSpace].GetObject(OpenMode.ForWrite)
                                              as BlockTableRecord;
    //Create new BlockReference, and link it to our block definition
    Point3d point = new Point3d(2.0, 4.0, 6.0);
    using (BlockReference blockRef =
            new BlockReference(point, blockDef.ObjectId))
    {
      //Add the block reference to modelspace
      ms.AppendEntity(blockRef);
      myT.AddNewlyCreatedDBObject(blockRef, true);
      //Iterate block definition to find all non-constant
      // AttributeDefinitions
      foreach (ObjectId id in  blockDef)
      {
        DBObject obj = id.GetObject( OpenMode.ForRead);
        AttributeDefinition attDef = obj as AttributeDefinition;
        if ((attDef != null) && (!attDef.Constant))
        {
          //This is a non-constant AttributeDefinition
          //Create a new AttributeReference
          using (AttributeReference attRef = new AttributeReference())
          {
            attRef.SetAttributeFromBlock(attDef, blockRef.BlockTransform);
            attRef.TextString = "Hello World";
            //Add the AttributeReference to the BlockReference
            blockRef.AttributeCollection.AppendAttribute(attRef);
            myT.AddNewlyCreatedDBObject(attRef, true);
          }
        }
      }
    }
    //Our work here is done
    myT.Commit();
  }
}
I recommend installing and using the MdgDbg utility to better understand how objects are stored in the DWG Database.

## 评论

**内容**: Michiel said...
Thanks, this is very helpfull to understand the releations between attributes and blocks.
Reply
01/06/2014 at 10:31 PM

---
