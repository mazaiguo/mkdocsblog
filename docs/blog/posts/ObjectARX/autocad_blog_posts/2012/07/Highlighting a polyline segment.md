---
title: "Highlighting a polyline segment"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
  - Polyline
description: "Finishing off my Friday afternoon by quickly migrating another DevNote. Its really quiet in the office today – a lot of people have taken time off ..."
author: Autodesk
---
# Highlighting a polyline segment

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/highlighting-a-polyline-segment.html

## 文章内容

By Stephen Preston
Finishing off my Friday afternoon by quickly migrating another DevNote. Its really quiet in the office today – a lot of people have taken time off around the July 4th public holiday.
This code demonstrates how to use a subentitypath to highlight a specific segment of a polyline. You can use the equivalent Unhighlight method to to unhighlight the segment (not shown). Make sure you read the ObjectARX Managed Reference Guide entry on this method before you use it in your code – there are a few details documented there that you need to be aware of.
[CommandMethod("HighlightPolySeg")]
public static void HighlightPolySeg()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Database db = doc.Database;
  Editor ed = doc.Editor;
  //Ask user to select polyline
  PromptEntityOptions peo = new PromptEntityOptions("\nSelect a polyline: ");
  peo.SetRejectMessage("\nMust be a polyline...");
  peo.AddAllowedClass(typeof(Polyline), true);
  PromptEntityResult per = ed.GetEntity(peo);
  if (per.Status != PromptStatus.OK) return;
  using (Transaction Tx = db.TransactionManager.StartTransaction())
  {
    Polyline pline =
        Tx.GetObject(per.ObjectId, OpenMode.ForRead) as Polyline;
    int nbSegments = pline.NumberOfVertices;
    if (!pline.Closed) --nbSegments;
    //Ask user which segment to highlight
    PromptIntegerOptions pio = new PromptIntegerOptions(
          "\nEnter segment id [1-" + nbSegments.ToString() + "] :");
    pio.LowerLimit = 1;
    pio.UpperLimit = nbSegments;
    PromptIntegerResult pir = ed.GetInteger(pio);
    if (pir.Status != PromptStatus.OK) return;
    //Define subentpath for segment
    FullSubentityPath path =
        new FullSubentityPath(new ObjectId[] { pline.Id },
        new SubentityId(SubentityType.Edge, new IntPtr(pir.Value)));
    //Highlight segment
    pline.Highlight(path, true);
  }
}

