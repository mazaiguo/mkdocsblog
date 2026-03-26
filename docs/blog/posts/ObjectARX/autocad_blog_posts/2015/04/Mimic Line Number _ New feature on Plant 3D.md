---
title: "Mimic Line Number > New feature on Plant 3D"
date: 2015-04-01
categories:
  - Plant 3D
tags:
  - Plant 3D
description: "This post is actually inspired on create a new line group previous post, but with some changes. This will actually mimic the Line Number >> New >> ..."
author: Autodesk
---
# Mimic Line Number > New feature on Plant 3D

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/mimic-line-number-new-feature-on-plant-3d.html

## 文章内容

By Augusto Goncalves
This post is actually inspired on create a new line group previous post, but with some changes. This will actually mimic the Line Number >> New >> Assign Tag feature on Plant 3D.
First, remove previous group related to the pipe, in order to avoid belong to more than one line group, which can be a modeling error. Second, just make the code simpler to include on your code. Note this will run for individual pipe making each pipe into a different line group (therefore different ISO production from each of them), you may adjust to a group of pipes.
private static void CreateNewTag(ObjectId partId, string newTagValue)
{
  PlantProject currentProj = PlantApplication.CurrentProject;
  PipingProject pipeProj = (PipingProject)currentProj.ProjectParts["Piping"];
  DataLinksManager dlm = pipeProj.DataLinksManager;
  PnPDatabase db = dlm.GetPnPDatabase();
 
  PnPTable p3dLineGroupTable = db.Tables["P3dLineGroup"];
  PnPRow lgRow = p3dLineGroupTable.NewRow();
  lgRow["Tag"] = newTagValue;
  p3dLineGroupTable.Rows.Add(lgRow);
 
  int prRowId = dlm.FindAcPpRowId(partId);
  PnPRow prRow = db.GetRow(prRowId); // not used yet
 
  // remove all line groups already related 
  // to this pipe, if any, to avoid this pipe
  // belong to multiple line groups
  PnPRowIdArray priorGroupIds = dlm.GetRelatedRowIds(
    "P3dLineGroupPartRelationship", "Part",
    prRowId, "LineGroup");
  if (priorGroupIds.Count != 1)
  {
    foreach (int id in priorGroupIds)
    {
      dlm.Unrelate("P3dLineGroupPartRelationship",
        "LineGroup", id, "Part", prRowId);
    }
  }
 
  // make the relation
  if (lgRow.RowId != -1 && prRowId != -1)
  {
    dlm.Relate("P3dLineGroupPartRelationship",
      "LineGroup", lgRow.RowId, "Part", prRowId);
  }

}
And here is a simple command to invoke this routine
[CommandMethod("customNewTag")]
public static void CmdCustomNewTag()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
 
  PromptEntityOptions peo = new PromptEntityOptions("\nSelect pipe: ");
  peo.SetRejectMessage("\nOnly pipes");
  peo.AddAllowedClass(typeof(Pipe), true);
  PromptEntityResult per = ed.GetEntity(peo);
  if (per.Status != PromptStatus.OK) return;
 
  PromptResult pr = ed.GetString("\nEnter new tag: ");
  if (pr.Status != PromptStatus.OK) return;
 
  CreateNewTag(per.ObjectId, pr.StringResult);
}

## 评论

**内容**: Grifo said...
Hi,
Can you help me....?
which references "using" should I insert?
(I use v.s 2022)
thanks
Grifo
Reply
12/01/2023 at 02:13 PM

---
**内容**: Sal said...
Thanks Augusto
This is a nice example. How to handle the case if the line tag user entered already exist. How to handle that case.
thanks
Reply
03/19/2024 at 02:14 PM

---
