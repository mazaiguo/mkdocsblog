---
title: "Mimic Line Number > New feature on Plant 3D – 2.0"
date: 2015-07-01
categories:
  - Plant 3D
tags:
  - Plant 3D
  - Selection
description: "This is an expanded version of what as previously posted here, hence the 2.0"
author: Autodesk
---
# Mimic Line Number > New feature on Plant 3D – 2.0

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/mimic-line-number-new-feature-on-plant-3d-20.html

## 文章内容

By Augusto Goncalves
This is an expanded version of what as previously posted here, hence the 2.0
But what was missing on version 1.0?
Actually it considered just one element at a time. Also, it ignored the related elements, like connectors, for instance. Now the sample below get a selection of entities, then find related elements (like P3dConnector and Universal) and add them all to the newly create group.
Thanks to Jens Dorstewitz (ADN Partner) for helping improve it.
[CommandMethod("customNewTag")]
public static void CmdCustomNewTag()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
 
  PromptSelectionResult  per = ed.GetSelection();
  if (per.Status != PromptStatus.OK) return;
 
  PromptResult pr = ed.GetString("\nEnter new tag: ");
  if (pr.Status != PromptStatus.OK) return;
 
  ObjectIdCollection ids = new ObjectIdCollection();
  foreach (SelectedObject selObj in per.Value)
    ids.Add(selObj.ObjectId);
 
  CreateNewTag(ids, pr.StringResult);
}
 
private static void CreateNewTag(ObjectIdCollection itemIds, string newTagValue)
{
  PlantProject currentProj = PlantApplication.CurrentProject;
  PipingProject pipeProj = (PipingProject)currentProj.ProjectParts["Piping"];
  DataLinksManager dlm = pipeProj.DataLinksManager;
  PnPDatabase db = dlm.GetPnPDatabase();
 
  // create new line group
  PnPTable p3dLineGroupTable = db.Tables["P3dLineGroup"];
  PnPRow lgRow = p3dLineGroupTable.NewRow();
  lgRow["Tag"] = newTagValue;
  p3dLineGroupTable.Rows.Add(lgRow);
  int newLineGroupId = lgRow.RowId;
 
  // rowIds of the selected items
  List<int> rowIds = new List<int>();
  foreach (ObjectId itemId in itemIds)
    rowIds.Add(dlm.FindAcPpRowId(itemId));
 
  // now the rowIds list contain only the 
  // items selected on screen, but we need more
  // elements related to those
  List<int> relateRowIds = new List<int>();
  foreach (int itemRowId in rowIds)
  {
    // only Olet, skip others.
    if (db.GetRowTableName(itemRowId) != "Olet") continue;
 
    // get the P3dConnectors
    List<int> p3dConnectorIds = new List<int>();
    p3dConnectorIds.AddRange(
      dlm.GetRelatedRowIds("P3dPartConnection",
      "Part1", itemRowId, "Part2"));
    p3dConnectorIds.AddRange(
      dlm.GetRelatedRowIds("P3dPartConnection",
      "Part2", itemRowId, "Part1"));
 
    List<int> universals = new List<int>();
    foreach (int connectorId in p3dConnectorIds)
    {
      // now the Universal:
      // the PnPDataLinks table should contain both
      // P3dConnector and Universal, and both share the 
      // same DwgHandleLow value, so find the first and
      // use this value to find the second
      PnPTable datalinksTable = db.Tables["PnPDataLinks"];
      PnPRow[] rows = datalinksTable.Select(
        string.Format("\"RowId\"={0}", connectorId));
      foreach(PnPRow row in rows)
      {
        PnPRow[] universalRow = datalinksTable.Select(
          string.Format("\"DwgHandleLow\"={0} AND \"DwgSubIndex\"=1",
          row["DwgHandleLow"]));
        universals.Add(int.Parse(universalRow[0]["RowId"].ToString()));
      }
    }
 
    // add what we found to the main list
    relateRowIds.AddRange(p3dConnectorIds);
    relateRowIds.AddRange(universals);
  }
 
  // finally a list with the selected elements
  // plus all related elements
  // now the rowIds should contain everything
  // that needs to be added to the new line group
  rowIds.AddRange(relateRowIds);
 
  // .Distinct avoid duplicated
  foreach (int itemRowId in rowIds.Distinct<int>().ToList<int>()) 
  {
    // get all line groups related to the items we found
    PnPRowIdArray priorGroupIds = dlm.GetRelatedRowIds(
      "P3dLineGroupPartRelationship", "Part", itemRowId, "LineGroup");
 
    // remove them from any previous group
    if (priorGroupIds.Count != 1)
    {
      foreach (int id in priorGroupIds)
      {
        dlm.Unrelate("P3dLineGroupPartRelationship",
          "LineGroup", id, "Part", itemRowId);
      }
    }
 
    // make the new relation
    if (newLineGroupId != -1 && itemRowId != -1)
    {
      dlm.Relate("P3dLineGroupPartRelationship",
        "LineGroup", newLineGroupId, "Part", itemRowId);
    }
  }
 
  // relate the drawing to the line group
  int dwgId = dlm.GetDrawingId(
    Application.DocumentManager.MdiActiveDocument.Database);
  if (dwgId != -1)
  {
    dlm.Relate("P3dDrawingLineGroupRelationship",
                "Drawing", dwgId,
                "LineGroup", newLineGroupId);
  }
}

