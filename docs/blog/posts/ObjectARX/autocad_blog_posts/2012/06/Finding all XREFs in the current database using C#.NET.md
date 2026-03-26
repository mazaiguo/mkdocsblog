---
title: "Finding all XREFs in the current database using C#.NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
  - Database
  - XREF
description: "The db.GetHostDwgXrefGraph() method returns the Xref hierarchy for the current drawing as an XrefGraph object. Here’s a simple code snippet to demo..."
author: Autodesk
---
# Finding all XREFs in the current database using C#.NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/finding-all-xrefs-in-the-current-database-using-cnet.html

## 文章内容

By Stephen Preston
The db.GetHostDwgXrefGraph() method returns the Xref hierarchy for the current drawing as an XrefGraph object. Here’s a simple code snippet to demonstrate its use – in this case to print the Xref structure of the current drawing to the command line.
    [CommandMethod("XrefGraph")]
    public static void XrefGraph()
    {
      Document doc = Application.DocumentManager.MdiActiveDocument;
      Database db = doc.Database;
      Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
      {
        ed.WriteMessage("\n---Resolving the XRefs------------------");
        db.ResolveXrefs(true, false);
        XrefGraph xg = db.GetHostDwgXrefGraph(true);
        ed.WriteMessage("\n---XRef's Graph-------------------------");
        ed.WriteMessage("\nCURRENT DRAWING");
        GraphNode root = xg.RootNode;
        printChildren(root, "|-------", ed, Tx);
        ed.WriteMessage("\n----------------------------------------\n");
      }
    }
      // Recursively prints out information about the XRef's hierarchy
    private static void printChildren(GraphNode i_root, string i_indent,
                                      Editor i_ed, Transaction i_Tx)
    {
      for (int o = 0; o < i_root.NumOut; o++)
      {
        XrefGraphNode child = i_root.Out(o) as XrefGraphNode;
        if (child.XrefStatus == XrefStatus.Resolved)
        {
          BlockTableRecord bl =
            i_Tx.GetObject(child.BlockTableRecordId, OpenMode.ForRead)
                as BlockTableRecord;
          i_ed.WriteMessage("\n" + i_indent + child.Database.Filename);
          // Name of the Xref (found name)
          // You can find the original path too:
          //if (bl.IsFromExternalReference == true)
          // i_ed.WriteMessage("\n" + i_indent + "Xref path name: "
          //                      + bl.PathName);
          printChildren(child, "| " + i_indent, i_ed, i_Tx);
        }
      }
    }

## 评论

**内容**: Gautham said...
How will you change the saved path name from a full path to a relative path. I tried changing the BlockTableRecord.PathName but that didn't provide the desired result. I wanted to do this without using the reference manager.
Reply
07/05/2012 at 08:22 AM

---
**内容**: Mona said in reply to Gautham...
Hello, I need to do the same thing.
Were you able to sort it out?
Thanks in advance
Reply
07/21/2012 at 12:07 AM

---
**内容**: Gautham said in reply to Mona...
I ended up saving the changes I made by using db.SaveAs(). This is a hackish solution but nothing else seemed to work. If you don't want to use this you can try using one of the LISP scripts that will do it for you.
Reply
07/25/2012 at 05:59 AM

---
**内容**: Madhukar Moogala said...
Sorry I missed answering your question earlier. Does this help? - http://adndevblog.typepad.com/autocad/2012/07/changing-xref-paths-from-absolute-to-relative.html.
Maybe that's how you were doing it already?
Reply
07/25/2012 at 05:10 PM

---
**内容**: Gautham said...
Thanks for the reply Stephen. I ended up doing something similar to the code you posted. I thought there would be another way of doing this and hence asked the question. Hope you are having a great time with your new Collie puppy.
Reply
07/30/2012 at 09:15 AM

---
**内容**: Raman said...
Nice code fore retrieving XRef DWG files.
like above, is there any API methods for getting
Attached Image,DWG,DGN,PDF file details
Please help me on this
Reply
08/27/2012 at 05:21 AM

---
**内容**: Hardiksinh Jadeja said...
Hi Stephen,
I am also looking for How to retrieve other Attached Files,
Or API methods for getting Attached Image,DWG,DGN,PDF file details ???
Thanxs
Reply
03/07/2013 at 04:16 AM

---
**内容**: Viru said in reply to Hardiksinh Jadeja...
Hi Jadeja,
does this post helps http://adndevblog.typepad.com/autocad/2013/02/how-to-get-all-the-raster-image-references-from-the-image-definition-object.html?
You can use similar method to get DGN, PDF.
Thanks
Viru
Reply
03/11/2013 at 03:42 AM

---
**内容**: Łukasz Taraszka said...
Hello everyone,
I know solution for all situation You mentioned.
Another format like PDF, DGN, DWG, DWF, JPG, GIF, PNG etc. is not the only problem.
Imagine situation, when You have current drawing with attached reference which has attached another reference (neasted references).
Another problem occurs when there is reference used in many drawings.
How to change references paths?
How to copy xref and change reference paths in parent and child drawings?
I prepared special API which can do all of those things. Fully commented, tested and documented. Want get it? Just let me know.
Reply
05/14/2013 at 06:34 AM

---
**内容**: Shankar said in reply to Łukasz Taraszka...
can u please post the way to change the filename of the xref file and also maintain the xref link in parent file in C# ??
Reply
02/02/2015 at 08:01 PM

---
**内容**: Łukasz Taraszka said in reply to Shankar...
Hello Shankar,
It was so long time ago.
As I remember, the hardest thing was to find all references in drawing. Problem was when xref was in block.
There is a way to find all references not in current drawing database but inside stand alone file. I think it's the best way to do it.
http://adndevblog.typepad.com/autocad/2012/06/using-e-transmit-api-in-net-to-find-external-references-in-a-drawing.html
To change path for xrefs like PDF, DWF you can use this code:
private void RenameFiles(Transaction trans, DBDictionary dictionary,
string embeddedType, )
{
if (dictionary.Contains(embeddedType))
{
DBDictionary subDictionary = (DBDictionary)trans.GetObject(dictionary.GetAt(embeddedType), OpenMode.ForRead);
foreach (DBDictionaryEntry dictionaryEntry in subDictionary)
{
UnderlayDefinition underlayDefinition = (UnderlayDefinition)trans.GetObject(dictionaryEntry.Value, OpenMode.ForRead);
String absolutePath = "YOUR PATH"; //Insert path

if(//Check if definition is correct one){

underlayDefinition.UpgradeOpen();
underlayDefinition.SourceFileName = absolutePath

}
}
}
}

//Embedded types

private const string PDF_DEFINITION = "ACAD_PDFDEFINITIONS";
private const string DWF_DEFINITION = "ACAD_DWFDEFINITIONS";

For changing image xrefs path you need to use this code:
private void RenamePictures
(Transaction trans, DBDictionary dictionary, string embeddedType,
)
{
if (dictionary.Contains(embeddedType))
{
DBDictionary subDictionary = (DBDictionary)trans.GetObject(dictionary.GetAt(embeddedType), OpenMode.ForRead);
foreach (DBDictionaryEntry dictionaryEntry in subDictionary)
{
RasterImageDef rasterImage = (RasterImageDef)trans.GetObject(dictionaryEntry.Value, OpenMode.ForRead);
String absolutePath = //Your path
if(//Check if rasterImage is correct one){

rasterImage.UpgradeOpen();
rasterImage.SourceFileName = absolutePath;
rasterImage.Load();
}
}
}
}
//Image definition name
private const string IMAGE_DEFINITION = "ACAD_IMAGE_DICT";


You can get named dictionary like this:

DBDictionary dictionary = (DBDictionary)trans.GetObject(db.NamedObjectsDictionaryId, OpenMode.ForRead);

There is the way how to upgrade block reference path.

private void RenameBlockReferences(Transaction trans, Database db)
{
BlockTable blockTable = (BlockTable)trans.GetObject(db.BlockTableId, OpenMode.ForRead);
foreach (ObjectId blockTableRecordId in blockTable)
{
BlockTableRecord blockTableRecord = (BlockTableRecord)trans.GetObject(
blockTableRecordId, OpenMode.ForRead);
if (blockTableRecord.IsFromExternalReference)
{
string tmpPath = //Your path
if (//Check if reference is the one you are looking for)
{
blockTableRecord.UpgradeOpen();
blockTableRecord.PathName = tmpPath;
}
}
}
}

I hope it will help you, but I haven't done it for 3 years.

There may be possibility to change reference path by e-Transmit API. It could be the easiest way. I suggest you to check it.

Good luck.
Reply
02/03/2015 at 02:01 AM

---
**内容**: ally said...
Is there an option to do this with an external app, using interop?
So far I only managed to get document.FileDependencies, resulting with a list of AcadFileDependency. And there is no way to tell which of the dependent files is nested.
Thank you!
Reply
05/25/2013 at 03:04 PM

---
