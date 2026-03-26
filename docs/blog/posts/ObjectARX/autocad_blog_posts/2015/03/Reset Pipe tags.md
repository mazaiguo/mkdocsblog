---
title: "Reset Pipe tags"
date: 2015-03-01
categories:
  - Plant 3D
tags:
  - Database
  - Plant 3D
description: "On the UI it’s possible to select Pipes, erase the Tag (set as unassigned) and then set it back. In some cases, this is a workflow to fix tag probl..."
author: Autodesk
---
# Reset Pipe tags

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/reset-pipe-tags.html

## 文章内容

By Augusto Goncalves
On the UI it’s possible to select Pipes, erase the Tag (set as unassigned) and then set it back. In some cases, this is a workflow to fix tag problems on Pipes, that can reflect on ISO generation.
The idea of this code is: on the database level (DataLinksManager), get all the PipeRunComponents, Fasteners and P3dConnector, then finally Unrelate and Relate again. The purpose is to force Plant 3D to rebuild its structure and restore.
Thanks to Jorge Lopez (big) help on this!
Important: if you plan to use this, ensure you have a backup of your project.
[CommandMethod("tryFixPipeTag")]
public static void CmdTryFixLineTag()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
 
  PlantProject currentProj = 
    PlantApplication.CurrentProject;
  PipingProject pipeProj = 
    (PipingProject)currentProj.ProjectParts["Piping"];
  DataLinksManager dlm = 
    pipeProj.DataLinksManager;
 
  PnPDatabase db = dlm.GetPnPDatabase();
 
  db.StartTransaction();
 
  int dwgRowId = dlm.GetDrawingId(
    Application.DocumentManager.MdiActiveDocument.Database);
  PnPRowIdArray groupIds = dlm.GetRelatedRowIds(
    "P3dDrawingLineGroupRelationship", "Drawing",
    dwgRowId, "LineGroup");
 
  foreach (int groupId in groupIds)
  {
    List<PnPRow> rowsToFix = new List<PnPRow>();
    PnPRow rowLineGroup = db.GetRow(groupId);
 
    string tag = rowLineGroup["Tag"] as string;
    if (string.IsNullOrWhiteSpace(tag)) continue;
 
    ed.WriteMessage("\n{0}", tag);
    System.Diagnostics.Debug.WriteLine(
      string.Format("\n{0}", tag));
 
    // Get pipe run components
    //
    PnPTable tblPipes = db.Tables["PipeRunComponent"];
    PnPRow[] rowsPipes = tblPipes.Select(
      string.Format("LineNumberTag='{0}'", tag));
 
    AddRowsToUniqueList(rowsToFix, rowsPipes);
 
    // Get fasteners
    //
    PnPTable tblFastener = db.Tables["Fasteners"];
    PnPRow[] rowsFastener = tblFastener.Select(
      string.Format("LineNumberTag='{0}'", tag));
 
    AddRowsToUniqueList(rowsToFix, rowsFastener);
 
    // Get P3dConnectors
    //
    PnPTable tblConnector = db.Tables["P3dConnector"];
    // just in case, make sure all rows are loaded in
    tblConnector.Select();  
 
    foreach (PnPRow rowFastener in rowsFastener)
    {
      PpObjectIdArray arr = dlm.FindAcPpObjectIds(rowFastener.RowId);
      foreach (PpObjectId ppId in arr)
      {
        PpObjectId ppConnectorId = new PpObjectId(
          ppId.DwgId, ppId.dbHandle, 0);
        int rowIdConnector = dlm.FindAcPpRowId(ppConnectorId);
        PnPRow jointRow = db.GetRow(rowIdConnector);
 
        AddRowToUniqueList(rowsToFix, jointRow);
      }
    }
 
    // Fix: Catches the following situations:
    //
    // 1. where tag does not match actual group
    // 2. when there is more than one group per part
    // 3. when the relationship is missing
    //
    foreach (PnPRow row in rowsToFix)
    {
      PnPRowIdArray priorGroupIds = 
        dlm.GetRelatedRowIds(
        "P3dLineGroupPartRelationship",
        "Part", row.RowId, "LineGroup");
      if (priorGroupIds.Count == 1 &&
        priorGroupIds.First.Value == rowLineGroup.RowId)
      {
        continue;
      }
 
      foreach (int id in priorGroupIds)
      {
        dlm.Unrelate("P3dLineGroupPartRelationship",
          "LineGroup", id, "Part", row.RowId);
      }
 
      dlm.Relate("P3dLineGroupPartRelationship", 
        "LineGroup", rowLineGroup.RowId, "Part", row.RowId);
    }
  }
 
  db.CommitTransaction();
}
 
private static void AddRowToUniqueList(
  List<PnPRow> rowsToFix, PnPRow jointRow)
{
  AddRowsToUniqueList(rowsToFix, new PnPRow[] { jointRow });
}
 
private static void AddRowsToUniqueList(
  List<PnPRow> rowsToFix, PnPRow[] rowsPipes)
{
  rowsToFix.AddRange(rowsPipes);
}

