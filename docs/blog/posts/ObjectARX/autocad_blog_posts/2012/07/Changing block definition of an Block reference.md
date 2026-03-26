---
title: "Changing block definition of an Block reference"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "Below code shows the procedure to modify the block definition for block reference. Code, prompts the user to select a block reference and changes i..."
author: Autodesk
---
# Changing block definition of an Block reference

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/changing-block-definition-of-an-block-reference.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to modify the block definition for block reference. Code, prompts the user to select a block reference and changes its definition so that block reference becomes reference for new block definition,
[CommandMethod("chageBlock")]
public static void chageBlock()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
        new PromptEntityOptions("\nSelect block reference");
    options.SetRejectMessage("\nSelect only block reference");
    options.AddAllowedClass(typeof(BlockReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the reference
        BlockReference blockRef = Tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as BlockReference;
          //block table record...
        BlockTable blockTable = Tx.GetObject(db.BlockTableId,
                                    OpenMode.ForRead) as BlockTable;
          //set the test as new block if present
        if (blockTable.Has("TEST"))
        {
            blockRef.UpgradeOpen();
              //set the id of the test block
            blockRef.BlockTableRecord = blockTable["TEST"];
        }
          Tx.Commit();
    }
}

## 评论

**内容**: Danny said...
I'm guessing this doesn't work well on blocks with attributes. My biggest API wish is to make the process of inserting blocks with attributes as easy as just inserting a BlockReference and the attributes just insert as is. Subsequently having to add AttributeReferences and trying to match their properties is an itch that needs scratching.
Reply
07/06/2012 at 04:40 PM

---
**内容**: Gerrit van Diepen said...
Is it possible to check if an existing block, for example a block called 'tree' in the drawing needs updating from a drawing named ' c:\Blocks\tree.dwg' This is because I have to check all the drawings created by a extern office who have to use our blocks without changing it.
Reply
06/10/2013 at 12:51 AM

---
**内容**: viru said in reply to Gerrit van Diepen...
Hi Gerrit,
No, at present it is not possible to check if the block need update from a source drawing file. You need to build your own logic to identify the block state.
regards
Viru
Reply
06/10/2013 at 01:36 AM

---
**内容**: Gerrit van Diepen said in reply to viru...
Hi Viru,
It is possible to add the "Tree.dwg" as a block called "test_tmp" without inserting it. But how can I check differences in the blocktablerecord between the blocks "tree" and "tree_tmp" ??
Thanks for the quick responce anyway ...
Regards,
Gerrit
Reply
06/10/2013 at 02:02 AM

---
**内容**: viru said in reply to Gerrit van Diepen...
Hi,
Again, there is no API for this. You have to build your logic, like comparing entities in blocks, or counting the entities in blocks or using bounding boxes etc… No direct method.
Regards
Viru
Reply
06/10/2013 at 02:22 AM

---
**内容**: André Cristino said...
Good afternoon. I'm trying to use this code, but I found a case that it not work as well. When I try to change the definition from a new block that I have created in my test DWG, it disappear from the model. I wonder what is causing this problem?
Reply
10/21/2013 at 10:29 AM

---
**内容**: Wesley said...
I am trying to port some AutoLISP Code to .NET C Sharp for deleting the text objects from within block references. I am running into difficulty. Can you have a look and see if there is a more efficient way to do this and indeed a way that will work?

public class Class1
{
[CommandMethod("DELTEXT")]
public void DelText()
{
// Get the current document and database, and start a transaction
Document acDoc = Application.DocumentManager.MdiActiveDocument;
Database acCurDb = acDoc.Database;
using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
{
// Open the Block table record for read
BlockTable acBlkTbl;
acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,OpenMode.ForRead) as BlockTable;
// Open the Block table record Model space for read
BlockTableRecord acBlkTblRec;
acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],OpenMode.ForRead) as BlockTableRecord;
int nCnt = 0;
acDoc.Editor.WriteMessage("\nModel space objects: ");
// Step through each object in Model space and display the Name of the Object
foreach (ObjectId acObjId in acBlkTblRec)
{
//If the ObjectClass.DxFName is INSERT, then this block is a reference.
if (acObjId.ObjectClass.DxfName == "INSERT")
{
//acDoc.Editor.WriteMessage("\n" + myBlk.Name);
//acDoc.Editor.WriteMessage("\n" + myBlk.BlockName);
//acDoc.Editor.WriteMessage("\n" + myBlk.ObjectId.ObjectClass.DxfName);
//acDoc.Editor.WriteMessage("\n" + myBlk.ObjectId.ObjectClass.Name);
//Open the Block Reference
BlockReference myBlkReference = acTrans.GetObject(acObjId, OpenMode.ForRead) as BlockReference;
BlockTableRecord xRefBlkTableRecs = acTrans.GetObject(myBlkReference.BlockTableRecord,OpenMode.ForRead) as BlockTableRecord;

//For each Object in the Block Table Record of the Block Reference
foreach (ObjectId myBlkObjId in xRefBlkTableRecs)
{
acDoc.Editor.WriteMessage("\n Object Class Name: " + myBlkObjId.ObjectClass.Name);
acDoc.Editor.WriteMessage("\n Object Class DxFName: " + myBlkObjId.ObjectClass.DxfName);
//Check if the object is a text object
if (myBlkObjId.ObjectClass.DxfName.ToString().Equals("TEXT"))
{
acDoc.Editor.WriteMessage("\n This is a Text Item and Will be Deleted");
//This is certainly a text object - count it.
nCnt = nCnt + 1;
//Delete it
myBlkReference.UpgradeOpen();
myBlkObjId.GetObject(OpenMode.ForWrite).Erase();
acTrans.Commit();
//acDoc.Editor.Regen();
}
}

}
else
{
acDoc.Editor.WriteMessage("\n" + acObjId.ObjectClass.Name.ToString());
acDoc.Editor.WriteMessage("\n" + acObjId.ObjectClass.DxfName.ToString());
}
//acTrans.Commit();
//acDoc.Editor.Regen();
}
acDoc.Editor.WriteMessage("\n" + nCnt + "Text Objects in Document");
// If no objects are found then display a message
if (nCnt == 0)
{
acDoc.Editor.WriteMessage("\n No Text objects found");
}
}
}
}
Reply
07/25/2016 at 04:22 AM

---
