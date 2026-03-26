---
title: "Redefining a block"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Block
  - DWG
  - Database
description: "Ed Jobe very kindly emailed me some suggestions for the blog (thanks Ed ). After we’d chatted for a while, he also asked a quick coding question:"
author: Autodesk
---
# Redefining a block

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/redefining-a-block.html

## 文章内容

By Stephen Preston
Ed Jobe very kindly emailed me some suggestions for the blog (thanks Ed ). After we’d chatted for a while, he also asked a quick coding question:
“Can you post a sample to redefine a block? I've seen some for inserting from file, but I haven't seen one for redefining. The db.Insert() function only creates new block table records.”
Here is some simple code demonstrating how to insert a DWG into your current drawing as a block named 'TEST'. If the a block named 'TEST' already exists in your drawing, then it is redefined:
    <CommandMethod("ReplaceBlock")> _
    Public Sub ReplaceBlock()
        Dim doc As Document = Application.DocumentManager.MdiActiveDocument
      Dim db As Database = doc.Database
      Dim blockName As String = "TEST"
        Dim blkDb As Database = New Database(False, True)
      blkDb.ReadDwgFile("C:\\Temp\\TEST.dwg",
                        System.IO.FileShare.Read, True, "")
        Using Tx As Transaction = db.TransactionManager.StartTransaction()
          Dim blockTable As BlockTable =
        Tx.GetObject(db.BlockTableId, OpenMode.ForRead, False, True)
          Dim btrId As ObjectId = db.Insert(blockName, blkDb, True)
          If btrId <> ObjectId.Null Then
            Dim btr As BlockTableRecord =
            Tx.GetObject(btrId,
                         OpenMode.ForRead, False, True)
            Dim brefIds As ObjectIdCollection =
            btr.GetBlockReferenceIds(False, True)
            For Each id As ObjectId In brefIds
            Dim bref As BlockReference =
            Tx.GetObject(id, OpenMode.ForWrite, False, True)
            bref.RecordGraphicsModified(True)
          Next
          End If
          Tx.Commit()
      End Using
        blkDb.Dispose()
      End Sub
Alternatively, if you want to programmatically edit the contents of a block (not inserting from another database), you can open up the BlockTableRecord for write, erase all the current entities it holds, and add your new ones. Here is a quick edit to the above function to redefine the block to just contain a single line:
    <CommandMethod("ReplaceBlock")> _
    Public Sub ReplaceBlock()
        Dim doc As Document = Application.DocumentManager.MdiActiveDocument
      Dim db As Database = doc.Database
        Dim blockName As String = "TEST"
        Using Tx As Transaction = db.TransactionManager.StartTransaction()
          Dim blockTable As BlockTable =
          Tx.GetObject(db.BlockTableId, OpenMode.ForRead, False, True)
          If (blockTable.Has(blockName)) Then
            Dim btr As BlockTableRecord =
            Tx.GetObject(blockTable(blockName),
                         OpenMode.ForWrite, False, True)
            'Erase all entities in btr
          For Each id As ObjectId In btr
            Dim ent As Entity = id.GetObject(OpenMode.ForWrite)
            ent.Erase()
          Next
            'Add new entities to btr
          Dim aLine As New Line(New Point3d(50, 50, 0), New Point3d(100, 100, 0))
          btr.AppendEntity(aLine)
          Tx.AddNewlyCreatedDBObject(aLine, True)
            Dim brefIds As ObjectIdCollection =
            btr.GetBlockReferenceIds(False, True)
            'Update blockrefs to display new graphics
          For Each id As ObjectId In brefIds
            Dim bref As BlockReference =
              Tx.GetObject(id, OpenMode.ForWrite, False, True)
            bref.RecordGraphicsModified(True)
          Next
            Tx.Commit()
        End If
        End Using
      End Sub
  Notice that in both code snippets we iterate through all the BlockReferences associated with the BlockTableRecord we’re editing and call their RecordGraphicsModified method. This is because a BlockTableRecord doesn’t automatically notify its BlockReferences when it is edited, so we have to explicitly tell the BlockReferences to regenerate their graphics.
Hope this is helpful Ed.
______________________
Updated May 7th 2012 to incorporate Norman Yuan's comment. I prefer calling RecordGraphicsModified on the BlockReference rather than to Regen the entire drawing, but that is personal choice.

## 评论

**内容**: Viktor K said...
Stephen thanks for this helpful article, here's another question that would/could be interesting to cover, if you're looking for topics.
Is there a method in .net api to search for a text string in the entire file and return values from dbtext, mtext, attributes, cells, etc... Basically how "find" command searches. I would imagine that you'd get objectids back of all the entities found with that text string. Or even better a find/replace functionality?
Maybe wishful thinking?
Thanks,
Viktor.
Reply
05/03/2012 at 04:54 PM

---
**内容**: Ed said...
Thanks Stephen. The second method is the one I was planning. However I didn't know about the RecordGraphicsModified() method.
Reply
05/04/2012 at 08:06 AM

---
**内容**: Norman Yuan said...
Hi Stephen,
I am not sure I understand the reason why the code has to go through the route of "inserting block with temporary name->redirect block references to the newly inserted block->erase old block->rename the new block".
If you insert a block with the block name that already exists in the current database, the newly inserted database (block) simply redefine the existing block automatically.
Here is code I tested (Acad2012 or older):
class MyCommands
{
[CommandMethod("RedeBlk")]
public static void RedifineBlock()
{
string blkFile = @"C:\TestBlock.dwg";
string blkName="TestBlock";
Document dwg =
Application.DocumentManager.MdiActiveDocument;
Editor ed = dwg.Editor;
using (Transaction tran = dwg.Database.
TransactionManager.StartTransaction())
{
using (Database db = new Database(false, true))
{
db.ReadDwgFile(blkFile,
System.IO.FileShare.Read, false, null);
dwg.Database.Insert(blkName,db,true);
}
tran.Commit();
}
ed.Regen();
}
}
Before run the code, the drawing have a block called "TestBlock". And the block file TestBlock.dwg is a block with completely different geometric entities. After running the code, the TestBlock in current drawing is redefined.
So, why not just go ahead to insert instead of temporarily naming, erasing and renaming?
if one want to prevent block to be accidently redefined, then, before inserting, search for the same named block, if found, warn user and let user decide to redefine or not.
Reply
05/04/2012 at 08:14 AM

---
**内容**: Madhukar Moogala said...
Hi Norman,
Oops. That's embarrassing :-(.
I didn't test doing that directly. I just took the info I read at face value and posted some existing code I found. Thanks for pointing this out. I'm on vacation today, but I'll go back and update the post soon.
Cheers,
Stephen
Reply
05/04/2012 at 08:43 AM

---
**内容**: David Osborne said...
I just checked this out because Alexander posted it as a helpful post to a discussion group question. I think neither of these appropriately address the issue of Attribute changes (additions or subtractions).
Otherwise, I'am going to have to go back and look at my code, because I thought it would cause an exception if I tried to insert a block that already existed, whether I wanted to redefine it or not.
Reply
05/14/2012 at 02:59 PM

---
**内容**: Madhukar Moogala said...
That is correct. This code snippet doesn't include updating AttributeReference values for BlockReferences already referencing the BlockTableRecord you're redefining.
To do that, you'd use the BlockReference.AttributeCollection property, and iterate through the contents of the AttributeCollection instance returned.
Reply
05/14/2012 at 03:07 PM

---
**内容**: Matus Brlit said...
Hello, I'm not sure if it has something to do with the issue that David mentioned, but I get this exception when I try to redefine a block (insert block with the same name).
Managed Debugging Assistant 'FatalExecutionEngineError' has detected a problem in 'E:\AutoCAD Civil 3D 2013\acad.exe'.
Additional Information: The runtime has encountered a fatal error. The address of the error was at 0xf4a4d4cc, on thread 0x510. The error code is 0xc0000005. This error may be a bug in the CLR or in the unsafe or non-verifiable portions of user code. Common sources of this bug include user marshaling errors for COM-interop or PInvoke, which may corrupt the stack.
It doesn't happen for all blocks, only when I provide attribute values, which is strange, because the attributes don't come to play at this point, yet.
I also tested on 32-bit and it works there, the exception is only thrown on 64-bit system and in release mode it results in unresponsive AutoCAD.
Reply
06/27/2013 at 06:56 AM

---
**内容**: dario said...

can someone help?
--------------------------
hello
My name is Dario (Brazil)
I need help please

insert a block and catch sequence data of this block
how to get the data inserted block properties, insertion point, extended data layer, rotation, color etc. ..
and then delete this block

[CommandMethod("Block")]
public void block()
{
doc = Host.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
string[] Dados = new string[3];
Dados[0] = "dado 1";
Dados[1] = "dado 2";
Dados[2] = "dado 3";
BlockReference br = CadGlobal.InsertBlockFromFile(doc, @"C:\wbc\orienta.dwg", new Point3d(50, 50, 50), Math.PI * 0.25,
"wbc_insert" , Dados, 30, 30, 1, 7, true, null, "wbcd");
help example:????
???? br.insertioPoint
???? br.rotation
???? br.layerName
???? br.Xpropierts[0]

???? br.Erase();
}

------------------------
Reply
03/06/2014 at 11:57 AM

---
**内容**: Madhukar Moogala said in reply to dario...
Hi Dario,
To monitor entities being inserted into a DWG, you can subscribe to the Database.ObjectAppended event. However, if you're looking for someone to write sample code for you, I suggest you ask your question over on the AutoCAD .NET forum (forums.autodesk.com).
Cheers,
Stephen
Reply
03/06/2014 at 12:03 PM

---
**内容**: dario said in reply to Madhukar Moogala...
Stephen
thank you very much
Reply
03/07/2014 at 03:52 AM

---
**内容**: Kevin said...
Stephen,
Thank you for the blog.
I work for a company which is VB.NET only (unfortunately). Therefore I rewrote your code for redefining a block in vb.net:
Public Shared Function TryRedifineBlock(BlockName As String, BlockFilePath As String) As Boolean
Dim result As Boolean = False
Dim doc As Document = ApplicationServices.Application.DocumentManager.MdiActiveDocument
Using lock As DocumentLock = doc.LockDocument()
Using tran As Transaction = doc.TransactionManager.StartTransaction()
Try
Dim blockDB As Database = New Database(False, True)
blockDB.ReadDwgFile(BlockFilePath, FileOpenMode.OpenForReadAndReadShare, True, "")
Dim blockTable As BlockTable = tran.GetObject(doc.Database.BlockTableId, OpenMode.ForRead, False, True)
Dim blockTableRecordID As ObjectId = doc.Database.Insert(BlockName, blockDB, True)
If Not blockTableRecordID.IsNull Then
Dim btr As BlockTableRecord = tran.GetObject(blockTableRecordID, OpenMode.ForRead, False, True)
For Each bRefID As ObjectId In btr.GetBlockReferenceIds(False, True)
Dim bRef As BlockReference = tran.GetObject(bRefID, OpenMode.ForWrite, False, True)
bRef.RecordGraphicsModified(True)
Next
End If
tran.Commit()
blockDB.Dispose()
result = True
Catch ex As System.Exception
tran.Abort()
result = False
Try
EventLog.WriteEntry("DynamicBlockHelper.TryRedifineBlock", ex.GetType().Name + ": " + ex.Message + Environment.NewLine + ex.StackTrace, EventLogEntryType.Error)
Catch eex As Exception
End Try
End Try
End Using
End Using
Return result
End Function
No exception is throw. However, the call to btr(BlockTableRecord).GetBlockReferenceIds returns an empty collection even when there are one or more instances of the original block in a given drawing.
The result is strange. The geometry of the block is not updated. However, editing one of the pre-existing blocks shows that the replacement block definition is in place.
I'd rather avoid throwing your code in a c# project and referencing the resulting assembly. Any insights you may have would be much appreciated.
Regards,
Kevin
Reply
04/02/2014 at 03:08 PM

---
**内容**: Kevin said...
Stephen,
Please disregard my question submitted yesterday. I must have confused your post with another which I failed to book mark. The forum post I was referring to was indeed written in c#, or I'm losing my mind, yet now that I revisit this page to check for a response I realize you provided vb.net code...
Very sorry. Somehow I failed to notice this yesterday when searching for the original source of the code I wrote. I suspect someone provided a translation of your code to c# and I stumbled on it. Maybe you had a nice laugh.
Thank you,
Kevin
Reply
04/03/2014 at 10:57 AM

---
**内容**: Kevin said...
Stephen,
Unfortunately, you code behaves just as mine does. The new definition is put in place, but no references are found for existing instances of the updated block definition.
I wonder if the nature of the block is at fault. The block is dynamic and 3D. I tried to test the provided method by copying the dwg file containing only the dynamic block definition and making a simple change to its geometry.
Running the code does not affect the geometry of existing block instances. However, new insertions of the block after running your code results in blocks which reflect the change I made.
I tried running regen after running your code, but nothing changed. I am fairly new to the ACAD APIs, and ACAD in general. So I am at a loss as to why no references are found. I tried retrieving the references using the block name, and still no instances are found.
I am able to accomplish the redefinition by simply running Insert within ACAD and selecting the updated block. I am then prompted to redefine, and all instances are updated. This is the behavior I am trying to reproduce pragmatically.
Regards,
Kevin
Reply
04/03/2014 at 12:56 PM

---
**内容**: Madhukar Moogala said in reply to Kevin...
Hi Kevin,
Your problem is because you're trying to do this with a Dynamic Block. See this blog post (and the post referenced near the beginning of it for details of how Dynamic Blocks work - http://adndevblog.typepad.com/autocad/2012/06/finding-all-block-references-of-a-dynamic-block.html.
I've not tried redefining a Dynamic Block. You could try applying the technique above to the primary block definition all the anonymous blocks created for the Dynamic Block, but I'm not sure if it will work.
Reply
04/04/2014 at 02:49 AM

---
**内容**: karl said...
hi,
i'm somewhat new to c#. what are the "true" & "false" references? \\\GetObject(db.BlockTableId, OpenMode.ForRead, False, True)\\\
karl
Reply
06/24/2014 at 07:52 AM

---
**内容**: Paulo Henrique said...
Its possible to do it using COM-Interop?
I can't access database.ReadDwgFile..
Reply
10/17/2014 at 07:37 AM

---
