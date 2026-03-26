---
title: "Changing xref paths from absolute to relative"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - XREF
description: "I was just checking recent comments on the blog (as part of my ongoing war on spammers ), and noticed a new comment by Gautham on an old post of mi..."
author: Autodesk
---
# Changing xref paths from absolute to relative

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/changing-xref-paths-from-absolute-to-relative.html

## 文章内容

By Stephen Preston
I was just checking recent comments on the blog (as part of my ongoing war on spammers ), and noticed a new comment by Gautham on an old post of mine which reminded me I’d forgotten to respond to the original question he asked about that post.
To change the path of an xref from absolute to relative, you simply have to edit the BlockTableRecord.PathName to a string that defines the relative path you need (or to have no path at all, if you want to rely on FindFile to locate your Xref). Here’s some simple code written by Balaji in response to a similar question from an ADN partner:
[CommandMethod("ChangeXRefPath")]
public void ChangeXRefPathMethod()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
  ObjectIdCollection collection = new ObjectIdCollection();
  using (Database db = new Database(false, true))
  {
    db.ReadDwgFile("c:\\Temp\\Test.dwg",
                FileOpenMode.OpenForReadAndWriteNoShare, false, "");
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
      BlockTable bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead)
                                                        as BlockTable;
      foreach (ObjectId btrId in bt)
      {
        BlockTableRecord btr = tr.GetObject(btrId, OpenMode.ForRead)
                                                as BlockTableRecord;
        if (btr.IsFromExternalReference)
        {
          btr.UpgradeOpen();
          String oldPath = btr.PathName;
          String newPath = oldPath.Replace(@"C:\Temp", ".");
          btr.PathName = newPath;
          collection.Add(btrId);
          ed.WriteMessage(String.Format("{0}Old Path : {1} New Path : {2}",
            Environment.NewLine, oldPath, newPath));
        }
      }
      tr.Commit();
    }
    if (collection.Count > 0)
    {
      //Perform the reload operation
      db.ReloadXrefs(collection);
    }
    db.SaveAs(db.OriginalFileName, true, db.OriginalFileVersion,
                                            db.SecurityParameters);
  }
}
The code is quite simple in that it assumes a drawing is located in c:\temp, and that the xrefs are in a subfolder of that. Its also loading the drawing being processed as a side database, which means that (in this example) the drawing mustn’t be open in the AutoCAD editor when you run the command.
I’ll leave it as an exercise to the reader to edit it to be more generic. I don’t have time for that just now because I’m off home to spend some quality time with the latest addition to my family. He’s the one on the left -

## 评论

**内容**: Matus Brlit said...
you are using the LISP double backslashes in the path, where you load the side database
the more generic approach:
String newPath = ".\" + System.IO.Path.GetFileName(oldPath)
also be careful when dealing with nested xrefs, I don't remember exactly why, but when I chacked my routine, I skip the nested xrefs there
Reply
07/26/2012 at 03:06 AM

---
**内容**: Pam said...
A Collie puppy! YEAY!
I just finished reading Albert Payson Terhune's THE HEART OF A DOG (1924), which is several short stories about brave Collies.
Who cares about AutoCAD when you've got a new Collie puppy! YEAY!
Reply
07/26/2012 at 04:20 PM

---
