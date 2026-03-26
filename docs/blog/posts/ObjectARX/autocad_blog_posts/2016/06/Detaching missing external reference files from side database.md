---
title: "Detaching missing external reference files from side database"
date: 2016-06-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
  - XREF
description: "Below code shows the procedure to detach the missing external reference files from a side database"
author: Autodesk
---
# Detaching missing external reference files from side database

发布日期: 2016-06-01

原始链接: https://adndevblog.typepad.com/autocad/2016/06/detaching-missing-external-reference-files-from-side-database.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to detach the missing external reference files from a side database
[CommandMethod("DetachXref")]
public void detach_xref()
{
    Document Doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = Doc.Editor;
    string mainDrawingFile = @"C:\xref\RectHost.dwg";
    using(Database db = new Database(false, false))
    {
        try
        {
            db.ReadDwgFile(mainDrawingFile, System.IO.FileShare.ReadWrite, false, "");
        }
        catch (System.Exception)
        {
            ed.WriteMessage("\nUnable to read the drawingfile.");
            return;
        }
        bool saveRequired = false;
        db.ResolveXrefs(true, false);
        using (Transaction tr = db.TransactionManager.StartTransaction())
        {
            XrefGraph xg = db.GetHostDwgXrefGraph(true);
            int xrefcount = xg.NumNodes;
            for (int j = 0; j < xrefcount; j++)
            {
                XrefGraphNode xrNode = xg.GetXrefNode(j);
                String nodeName = xrNode.Name;
                if (xrNode.XrefStatus == XrefStatus.FileNotFound)
                {
                    ObjectId detachid = xrNode.BlockTableRecordId;
                    db.DetachXref(detachid);
                    saveRequired = true;
                    ed.WriteMessage("\nDetached successfully");
                    break;
                }
            }
            tr.Commit();
        }
        if (saveRequired)
            db.SaveAs(mainDrawingFile, DwgVersion.Current);
    }
}

## 评论

**内容**: Jemmy said...
Hi Mr. Virupaksha Aithal, first i'm sorry to post use this link to ask. I'm Jemmy from Indonesia. I have a question, how to save (or export /ex. oraexport) my topology into my oracle spatial using c# from my autocad map 3d 2009. Thanks for helping me.
Reply
07/24/2016 at 09:03 PM

---
**内容**: viru said in reply to Jemmy...
Hi Jemmy,
My suggestion is to ask this question on MAP 3d api forum http://forums.autodesk.com/t5/autocad-map-3d-developer/bd-p/84
I have no knowledge of MAP 3D API.
Thanks
Viru
Reply
07/25/2016 at 03:15 AM

---
**内容**: Jemmy said in reply to viru...
thanks for your suggestion mr. Viru.
Reply
07/25/2016 at 06:50 AM

---
