---
title: "Track value change on Plant 3D Database"
date: 2015-05-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Database
  - Plant 3D
description: "On AutoCAD entities we cannot track changes, although we can simulate some sort of tracking mechanism, see this blog post. So if you need to track ..."
author: Autodesk
---
# Track value change on Plant 3D Database

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/track-value-change-on-plant-3d-database.html

## 文章内容

By Augusto Goncalves
On AutoCAD entities we cannot track changes, although we can simulate some sort of tracking mechanism, see this blog post. So if you need to track geometric properties, like position, you’ll probably need something as described.
Now on Plant 3D there is a actual database storing information: the PnPDatabase, which includes a list of tables (PnPTable), that represent the classes. And there are some interesting events, such as ColumnChanged event.
Below is a sample that uses this event to track changes on database values (in this case, the Manufacturer) of EngineeringItems.
[CommandMethod("trackTableChanges")]
public static void CmdTrackChanges()
{
  TrackDBTableChanges(
    "EngineeringItems",
    new string[] { "Manufacturer" });
}
 
private static void TrackDBTableChanges(
  string tableName, string[] columns)
{
  PlantProject currentProj =
    PlantApplication.CurrentProject;
  PipingProject pipeProj =
    (PipingProject)currentProj.ProjectParts["Piping"];
  DataLinksManager dlm = pipeProj.DataLinksManager;
  PnPDatabase db = dlm.GetPnPDatabase();
 
  // the table we want to track
  PnPTable engItemsTable = db.Tables[tableName];
 
  // just the columns we want to track
  _collunsToTrack = new List<string>(columns);
 
  // start tracking
  engItemsTable.ColumnChanged +=
    engItemsTable_ColumnChanged;
}
 
private static List<string> _collunsToTrack = null;
 
static void engItemsTable_ColumnChanged
  (object sender, PnPColumnChangeEventArgs e)
{
  // filter by column name
  if (!(_collunsToTrack.Contains(e.Column.Name))) return;
 
  // simple output
  Application.DocumentManager.MdiActiveDocument.
    Editor.WriteMessage(
    "{0} of item {1} changed from {2} to {3}",
    e.Column.Name, e.Row.RowId,
    e.CurrentValue, e.ProposedValue);
}

