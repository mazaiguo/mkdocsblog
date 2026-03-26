---
title: "Setting the Line Number Tag in AutoCAD Plant3d"
date: 2012-08-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - DWG
  - Plant 3D
description: "Leading on from this post I had a question on how to use that same code to set the Line Number Tag; I have to admit, for a newbie, it’s not that ob..."
author: Autodesk
---
# Setting the Line Number Tag in AutoCAD Plant3d

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/setting-the-line-number-tag-in-autocad-plant3d.html

## 文章内容

by Fenton Webb
Leading on from this post I had a question on how to use that same code to set the Line Number Tag; I have to admit, for a newbie, it’s not that obvious...
Selecting the PPG-PIPING-01.dwg from the Plant3d 2012 “Sample Project” project, and then viewing the Properties of the first Pipe I see, I get this view in Plant…
So how to set the Line Number Tag?
Using the code from the previous post I mentioned above, you would think this code would work, but it doesn’t…
[CommandMethod("GetLineGroupInfo")]
public void GetLineGroupInfo()
{
 // get the AutoCAD Editor object so we can print to the command line
 Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor; 
 // select the object
 PromptEntityResult res = ed.GetEntity("Pick Object obtain properties : ");
 // if something selected
 if (res.Status == PromptStatus.OK)
{
  // get the current project object
  PlantProject currentProj = PlantApplication.CurrentProject;
  // get the Piping project part
  PipingProject pipeProj = (PipingProject)currentProj.ProjectParts["Piping"];
  // get the data links manager
  DataLinksManager dlm = pipeProj.DataLinksManager;
  // get the 3d data links manager
  DataLinksManager3d dlm3d = pipeProj.DataLinksManager3d;
  // and then get the row id for the selected object
  int rowId = dlm.FindAcPpRowId(res.ObjectId);
    // Parts are related to pipe line group via P3dLineGroupPartRelationship.
  // So we need to traverse this relationship to get line group row id
  PnPRowIdArray lgid = dlm.GetRelatedRowIds("P3dLineGroupPartRelationship", "Part", rowId, "LineGroup");
  if (lgid == null || lgid.Count == 0)
  {
   // line group was not found. May happen, for example, if Equipment is picked.
   return;
  }
    // this is line group row in the data. (PnPRowIdArray is in fact list
  int lgRowId = lgid.First.Value;
    // using lgRowId you may get all line group properties using the following code
  // last parameter doesn't matter
  List<KeyValuePair<string, string>> vals = dlm.GetAllProperties(lgRowId, false);
    try
  {
    // or get the same thing from PnPDatabase via row
    PnPRow lgRow = dlm.GetPnPDatabase().GetRow(lgRowId);
    String Tag = lgRow["Tag"].ToString();
    lgRow.BeginEdit();
    lgRow["Tag"] = "98765";
    lgRow.EndEdit();
    Tag = lgRow["Tag"].ToString();
   }
  catch (System.Exception ex)
  {
    }
 }
The reason that it doesn’t is because the Tag value is actually defined via the Project Manager->Project Settings to be set via the P3d Line Group ‘Number’ property…
First let’s see how I found worked out that it was using the P3d Line Group…
  Now let’s see how I worked out that the ‘Number’ property is the one we need…
  So, finally, to change the Tag, the code should look something like this…
[CommandMethod("GetLineGroupInfo")]
public void GetLineGroupInfo()
{
 // get the AutoCAD Editor object so we can print to the command line
 Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
   // select the object
 PromptEntityResult res = ed.GetEntity("Pick Object obtain properties : ");
 // if something selected
 if (res.Status == PromptStatus.OK)
{
  // get the current project object
  PlantProject currentProj = PlantApplication.CurrentProject;
  // get the Piping project part
  PipingProject pipeProj = (PipingProject)currentProj.ProjectParts["Piping"];
  // get the data links manager
  DataLinksManager dlm = pipeProj.DataLinksManager;
  // get the 3d data links manager
  DataLinksManager3d dlm3d = pipeProj.DataLinksManager3d;
  // and then get the row id for the selected object
  int rowId = dlm.FindAcPpRowId(res.ObjectId);
    try
  {
   PipeLineGroupData lginfo = dlm3d.GetLineGroupInfo(rowId);
  }
  catch
  {
   // there is bug in the Plant that prevents getting lginfo by part rowid. Sorry.
   // but we may achieve the same thing using the following workaround
  }
    // Parts are related to pipe line group via P3dLineGroupPartRelationship.
      // So we need to traverse this
  // relationship to get line group row id
  PnPRowIdArray lgid = dlm.GetRelatedRowIds("P3dLineGroupPartRelationship", "Part", rowId, "LineGroup");
  if (lgid == null || lgid.Count == 0)
  {
   // line group was not found. May happen, for example, if Equipment is picked.
   return;
  }
    // this is line group row in the data. (PnPRowIdArray is in fact list
  int lgRowId = lgid.First.Value;
    // using lgRowId you may get all line group properties using the following code
  // last parameter doesn't matter
  List<KeyValuePair<string, string>> vals = dlm.GetAllProperties(lgRowId, false);
        try
      {
        // get the pnp row
        PnPRow lgRow = dlm.GetPnPDatabase().GetRow(lgRowId);
        // find out what the original tag was set to
        String Tag = lgRow["Tag"].ToString();
          // start an edit transaction
        lgRow.BeginEdit();
        // set the P3d Line Group 'Number'
        lgRow["Number"] = "98765";
        // finish the edit transaction
        lgRow.EndEdit();
          // see if it worked
        Tag = lgRow["Tag"].ToString();
        // yes it did!
        // all done
      }
      catch (System.Exception ex)
      {
        }
    // the following code will only work if linegroup has a valid (not empty) tag. So you may expect
  // exception here if LineGroup is not assigned a tag (not sure why it is done this way)
  try
  {
   PipeLineGroupData lginfoAtLast = dlm3d.GetLineGroupInfo(lgRowId);         
  }
  catch
  {
   // get here if line group doesn't have assigned tag
  }
}
}

## 评论

**内容**: Andrew Root said...
Can you compile this into a DLL such that it can be loaded into Plant 3D and allow creating or setting new linenumbers?
Thanks!
Reply
01/19/2024 at 08:08 PM

---
