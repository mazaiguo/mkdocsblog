---
title: "How to get the ‘Joint Type’ information for a P&ID Asset from Plant3d using C#.NET"
date: 2012-04-01
categories:
  - Plant 3D
tags:
  - .NET
  - C#
  - Plant 3D
description: "Recently an interesting question came in about obtaining the ‘Joint Type’ information from a P&ID Asset from Plant3d. Basically, the concept of a J..."
author: Autodesk
---
# How to get the ‘Joint Type’ information for a P&ID Asset from Plant3d using C#.NET

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-get-the-joint-type-information-for-a-pid-asset-from-plant3d-using-cnet.html

## 文章内容

By Fenton Webb
Recently an interesting question came in about obtaining the ‘Joint Type’ information from a P&ID Asset from Plant3d. Basically, the concept of a Joint Type between P&ID and Plant3d is quite different. The Joint Type is a property of the style that affects placement behavior. For P&ID, it only specifies if the asset should be inline, endline, break an sline, etc. These concepts don’t translate to Plant 3D very well. However, in P&ID there is a per object property that does translate over albeit not directly. This property is the EndConnections property found in the DataManager->P&ID->Engineering Items->Inline Assets->Hand Valves. So, from the API, once we have a PnPDatabase, you can get a row for an Inline Asset, get the EndConnections column in the row, then when we have that, we match the inline asset on the Plant3d side with a matching Tag. If the Tag properties match, then is the same logical inline asset. Once we have that match, then we check to see how it's connected.
Now for the code…
// determining the Join Type for Assets
[CommandMethod("GetJointType")]
public void GetJointType()
{
  // get the AutoCAD Editor object so we can print to the command line
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    // get the current project object
  PlantProject currentProj = PlantApplication.CurrentProject;
    // get the PnID project part
  PnIdProject PnIdProj = (PnIdProject)currentProj.ProjectParts["PnID"];
  // get the datalinks manager
  DataLinksManager datalinksManager = PnIdProj.DataLinksManager;
  // get the PnpDatabase
  PnPDatabase pnpDatabase = datalinksManager.GetPnPDatabase();
    // get the Piping project part
  PipingProject pipingProj = (PipingProject)currentProj.ProjectParts["Piping"];
  // get the datalinks manager
  DataLinksManager pipingDatalinksManager = pipingProj.DataLinksManager;
  // get the PnpDatabase
  PnPDatabase pipingPnpDatabase = pipingDatalinksManager.GetPnPDatabase();
  // now from the piping.pcf, get the PipeRunComponent from PnpBase->EngineeringItems
  var pipeRunComps = pipingPnpDatabase.Tables["PipeRunComponent"];
    // get the handvalves from PnpBase->EngineeringItems->InLineAssets
  var pnid_table = pnpDatabase.Tables["HandValves"];
  PnPRow[] pnid_handvalves = pnid_table.Select();
  // loop through each hand value type and examine the EndConnections
  foreach (PnPRow pnid_valve in pnid_handvalves)
  {
    // extract the EndConnections type string, remember that this may not match up with the "JointType" later on
    var strEndConnections = pnid_valve["EndConnections"] as string;
    // and the tag string
    var strTag = pnid_valve["Tag"] as string;
    // make sure we have a tag
    if (String.IsNullOrEmpty(strTag) == true || strTag == "?-?")
    {
      ed.WriteMessage("\nSkipping EndConnections->" + strEndConnections.ToString() + " because the Tag value is not set");
      continue;
    }
      // and select all of the tags that match the HandValves row
    var pipingRows = pipeRunComps.Select("Tag='" + strTag + "'");
    // check that we have some
    if (pipingRows.Length == 0)
    {
      ed.WriteMessage("\nFailed to find Tag " + strTag + " in the Piping.dcf. The tags must be labeled the same in order to match up.");
      continue;
    }
      ed.WriteMessage("\nFound " + pipingRows.Length.ToString() + " matching tags called " + strTag);
      // loop the matching tags, for Part1
    foreach (PnPRow piping_row in pipingRows)
    {
      int id = piping_row.RowId;
      // get the connection types from P3dPartConnection
      PnPRelationshipType relType = pipingPnpDatabase.RelationshipTypes["P3dPartConnection"];
      // find the JointTypes for the tag
      findAndPrintJointTypes("Part1", "Part2", strTag, id, relType, strEndConnections, pipingPnpDatabase);
      // and reverse because they may be connected in a different order
      findAndPrintJointTypes("Part2", "Part1", strTag, id, relType, strEndConnections, pipingPnpDatabase);
    }
  }
}
  void findAndPrintJointTypes(string part1, string part2, string strTag, int id, PnPRelationshipType relType, string endConnection, PnPDatabase pnpDatabase)
{
  // get the AutoCAD Editor object so we can print to the command line
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
  // now find the 'Part1" relationships from the table
  var rels1 = relType.GetRelationships(new KeyValuePair<string, int>(part1, id));
  // loop all of them
  foreach (var rel in rels1)
  {
    // find the Part2 relation
    int relatedId = rel[part2];
    var relatedRow = pnpDatabase.GetRow(relatedId);
    // extract the JointType
    var jointType = relatedRow["JointType"];
      // now if we have a match
    if (jointType.ToString() == endConnection)
    {
      ed.WriteMessage("\nFound JointType " + jointType + " from PnId in Piping for Tag " + strTag);
    }
  }
}

