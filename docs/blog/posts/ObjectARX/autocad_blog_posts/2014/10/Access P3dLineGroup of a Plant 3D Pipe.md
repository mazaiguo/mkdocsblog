---
title: "Access P3dLineGroup of a Plant 3D Pipe"
date: 2014-10-01
categories:
  - Plant 3D
tags:
  - Database
  - Plant 3D
description: "This question came from Jens Dorstewitz: how access the P3dLineGroup of a given Plant 3D pipe? To clarify, below is the project properties with the..."
author: Autodesk
---
# Access P3dLineGroup of a Plant 3D Pipe

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/access-p3dlinegroup-of-a-plant-3d-pipe.html

## 文章内容

By Augusto Goncalves
This question came from Jens Dorstewitz: how access the P3dLineGroup of a given Plant 3D pipe? To clarify, below is the project properties with the table we’re looking for.
To answer we have a problem: this information is not part of the properties of the pipe, but in fact stored somewhere else. So we need to understand the relationships of Plant 3D database.
There are a few steps: (1) from a Pipe ObjectId, use the Data Links Manager to get the RowId and (2) using the Plant 3D database, open and search at the P3dLineGroupPartRelationship table for a row where Part equals this RowId. With this row, (3) get the LineGroup column that will be the RowId of the line group we need. Finally (4) open the P3dLineGroup table and get the row we need. This row can be edited.
Actually Jens Dorstewitz (thanks again) wrote a sample based on this idea, below is an simplified version of it. Enjoy.
[CommandMethod("changeLineGroupData")]
public void CmdChangeP3dLineGroupData()
{
  // First, select a Plant 3D pipe
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  PromptEntityOptions peo = new PromptEntityOptions(
    "Select pipe to obtain properties : ");
  peo.SetRejectMessage("Only Plant 3D Pipes");
  peo.AddAllowedClass(typeof(Pipe), true);
  PromptEntityResult per = ed.GetEntity(peo);
  if (per.Status != PromptStatus.OK) return;
 
  ObjectId pipeId = per.ObjectId;
 
  // Get plant 3D project part
  PlantProject currentProj = PlantApplication.CurrentProject;
  PipingProject pipeProj = (PipingProject)currentProj.ProjectParts["Piping"];
  DataLinksManager dlm = pipeProj.DataLinksManager;
 
  // Convert the pipe ObjectId to RowId (used on P3D database
  int rowId = dlm.FindAcPpRowId(pipeId);
 
  // Get the P3dLineGroup table of the database
  PnPDatabase db = dlm.GetPnPDatabase();
  PnPTable tbl = db.Tables["P3dLineGroup"];
 
  // Find the relaship between the pipe RowId
  // This row registry contains the P3dLineGroup
  PnPRowIdArray lineGroupId = dlm.GetRelatedRowIds(
    "P3dLineGroupPartRelationship", "Part", rowId, "LineGroup");
  if (lineGroupId == null || lineGroupId.Count == 0) return;
  int lineGroupRowId = lineGroupId.First.Value;
 
  // Now select using this lineGroupRowId
  string sStatement = "PnPID=" + lineGroupRowId;
  PnPRow[] rows = tbl.Select(sStatement);
  if (rows.Length > 0) // should be just 1
  {
    foreach (PnPRow Row in rows)
    {
      // now do something here...
    }
  }
}

## 评论

**内容**: Pavel Lopata said...
Hi,
I'm beginner with programing and I have little problem with my small module.
I want reade parametr KKS from Support and write this parametr to SteelMember and Plate. I didn't get over strB. Didn't read this parametr.
Sub namePOK()
Dim strA As String
Dim strB As String
Dim objSS As AcadSelectionSet
Set objSS = ThisDrawing.SelectionSets.Add(Now)

objSS.SelectOnScreen
Dim dblTotal As Double
Dim objSupport As PnP3dCOMLib.AcPnP3dSupport
Dim objMember As PnP3dCOMLib.AcPnP3dStructureMember
Dim objPlate As PnP3dCOMLib.AcPnP3dStructurePlate
For Each objSupport In objSS
' strA = objSupport.KKS
strB = objSupport.KKS
objMember.BQ1 = strB
objPlate.BQ1 = strB
Next

objSS.Update
objSS.Delete

End Sub
Reply
10/26/2017 at 02:23 AM

---
**内容**: Gokul said...
Can you please tell me how do i get the “visible in object view” check box values which is in the P3dLineGroup UI window?
Reply
04/27/2023 at 02:47 AM

---
