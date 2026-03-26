---
title: "How to access or generate a block preview Icon in .Net?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - C#
  - Unicode
description: "The C# command below illustrates how to save a block preview icon as an image on the disk:"
author: Autodesk
---
# How to access or generate a block preview Icon in .Net?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-access-or-generate-a-block-preview-icon-in-net.html

## 文章内容

By Philippe Leefsma
The C# command below illustrates how to save a block preview icon as an image on the disk:
[DllImport("acad.exe",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acedCommand")]
private static extern int acedCommand(
    int type1,
    string command,
    int type2,
    string blockName,
    int end);
  [CommandMethod("BlkPreview")]
static public void BlkPreview()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptStringOptions pso = new PromptStringOptions(
        "\nEnter block name: ");
      PromptResult pr = ed.GetString(pso);
      if (pr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable table = Tx.GetObject(
            db.BlockTableId,
            OpenMode.ForRead)
                as BlockTable;
          if (!table.Has(pr.StringResult) == true)
        {
            ed.WriteMessage(
                "\nNo block with name " + pr.StringResult);
            return;
        }
          BlockTableRecord blk = Tx.GetObject(
            table[pr.StringResult],
            OpenMode.ForRead)
                as BlockTableRecord;
          if (blk.PreviewIcon == null)
        {
            acedCommand(
                5005,
                "BLOCKICON",
                5005,
                pr.StringResult,
                5000);
        }
          blk.PreviewIcon.Save(
            "c:\\Temp\\" + pr.StringResult + ".bmp");
          Tx.Commit();
    }
}

## 评论

**内容**: Kerry Brown said...

Thanks Philippe,
Could you also show this functionality for AutoCAD 2013 .. I believe it may differ.
Regards
Reply
05/09/2012 at 03:01 AM

---
**内容**: Account Deleted said...
Hi, Philippe!
Two remarks:
1. With AutoCAD 2013 not acad.exe but accore.dll export function acedCommand
2. Instead of "BLOCKICON" more correct using "_.BLOCKICON" in order to support localized version of AutoCAD
Reply
05/09/2012 at 03:04 AM

---
**内容**: Sailor said in reply to Account Deleted...
I tried the code above in AutoCAD 2013, but the image files are 32*32 pixels.
I want the images to be larger. So I used
blk.PreviewIcon.GetThumbnailImage(64, 64,
(System.Drawing.Image.GetThumbnailImageAbort)(() => { return true; }), IntPtr.Zero),
and the image turned out to be very fuzzy. What could I do. Like the block preview from CAD command INSERT dialog.
By the way, the command BLOCKICON is shown in the CAD Console, can it be hidden?
Thanks!
Reply
06/10/2014 at 10:56 PM

---
**内容**: Mark said in reply to Sailor...
Is this working? ive tried it on 2013 with
acedCommand(
5005,
"_.BLOCKICON",
5005,
,
5000);
and use accore.dll, but nothing is happening. it just passes ton the code and still the previewicon is still null.
Reply
12/04/2014 at 12:13 PM

---
**内容**: G. Rohith vinay said...
Hi, Philippe,
As like Blocks I want a preview icon for Entities. how can we get?
Thanks in Advance.
Reply
02/09/2021 at 10:46 PM

---
