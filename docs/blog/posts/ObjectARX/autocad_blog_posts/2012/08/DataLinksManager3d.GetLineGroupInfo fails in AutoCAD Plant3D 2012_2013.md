---
title: "DataLinksManager3d.GetLineGroupInfo fails in AutoCAD Plant3D 2012/2013"
date: 2012-08-01
categories:
  - Plant 3D
tags:
  - API
  - AutoCAD
  - Plant 3D
  - Plot
description: "It seems that I found a slight problem with the Plant3d API in terms of obtaining the PipeLineGroupData from the DataLinksManager3d.GetLineGroupInf..."
author: Autodesk
---
# DataLinksManager3d.GetLineGroupInfo fails in AutoCAD Plant3D 2012/2013

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/datalinksmanager3dgetlinegroupinfo-fails-in-autocad-plant3d-20122013.html

## 文章内容

by Fenton Webb
It seems that I found a slight problem with the Plant3d API in terms of obtaining the PipeLineGroupData from the DataLinksManager3d.GetLineGroupInfo().
If you are running into this issue, then try this code below…
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
    PlantProject currentProj = Autodesk.ProcessPower.PlantInstance.PlantApplication.CurrentProject;
    // get the Piping project part
    Autodesk.ProcessPower.P3dProjectParts.PipingProject pipeProj = (Autodesk.ProcessPower.P3dProjectParts.PipingProject)currentProj.ProjectParts["Piping"];
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
      // there is a slignt issue in the Plant that prevents getting lginfo by
      // part rowid. Sorry about that. We can achieve the same thing using the
      //  following workaround (see below)
    }
      // Parts are related to pipe line group via P3dLineGroupPartRelationship.
    // So we need to traverse this relationship to get line group row id
    PnPRowIdArray lgid = dlm.GetRelatedRowIds("P3dLineGroupPartRelationship", "Part", rowId, "LineGroup");
    if (lgid == null || lgid.Count == 0)
    {
      // line group was not found - for example, if Equipment is picked.
      return;
    } 
    // this is line group row in the data. (PnPRowIdArray is in fact list
    int lgRowId = lgid.First.Value;
      // using lgRowId you can get all line group properties using the following
    // last parameter doesn't matter
    List<KeyValuePair<string, string>> vals = dlm.GetAllProperties(lgRowId, false);
      // or get the same thing from PnPDatabase via row
    PnPRow lgRow = dlm.GetPnPDatabase().GetRow(lgRowId);
      // the following code will only work if linegroup has a valid (not empty)
    // tag. Expect an exception here if LineGroup is not assigned a tag
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

