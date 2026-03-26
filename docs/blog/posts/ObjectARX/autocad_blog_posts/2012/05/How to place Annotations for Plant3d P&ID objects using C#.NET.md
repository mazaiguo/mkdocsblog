---
title: "How to place Annotations for Plant3d P&ID objects using C#.NET"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - .NET
  - AutoCAD
  - C#
  - Plant 3D
description: "Leading on from this post How to list all of the Annotation Style names in Plant3d P&ID using C#.NET I thought I should try and use that code for s..."
author: Autodesk
---
# How to place Annotations for Plant3d P&ID objects using C#.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-place-annotations-for-plant3d-pid-objects-using-cnet.html

## 文章内容

by Fenton Webb
Leading on from this post How to list all of the Annotation Style names in Plant3d P&ID using C#.NET I thought I should try and use that code for something useful So I’ve basically implemented my own version of the PIDANNOTATE command…
  // Programmatically create Annotation by Fenton Webb, DevTech, Autodesk 1/5/2012
[CommandMethod("MyCreateAnnotation")]
public void myCreateAnnotation()
{
  // get the AutoCAD Editor object
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
  // select the pnid object to annotate
  PromptEntityResult pnidObjectRes = ed.GetEntity("Pick Object to annotate : ");
  // if something selected
  if (pnidObjectRes.Status == PromptStatus.OK)
  {
    PromptResult annoStyleRes;
    do
    {
      // enter the required annotation style
      PromptStringOptions opts = new PromptStringOptions("Enter Annotation Style or ? to list");
      opts.AllowSpaces = true;
      annoStyleRes = ed.GetString(opts);
      if (annoStyleRes.Status == PromptStatus.OK)
      {
        // check to see if a listing is required
        if (annoStyleRes.StringResult == "?")
        {
          // list the entries in the Autodesk_PNP dict
          using (DBDictionary annoStylesDict = DictionaryUtils.GetAnnotationStylesDictionaryId(ed.Document.Database, 0).Open(OpenMode.ForRead) as DBDictionary)
            foreach(DBDictionaryEntry entry in annoStylesDict)
              ed.WriteMessage("\n" + entry.Key);
        }
      }
    } while (annoStyleRes.Status == PromptStatus.OK && annoStyleRes.StringResult == "?");
      // if we have what we think is a valid annotation style
    if (annoStyleRes.Status == PromptStatus.OK)
    {
      // select the point for the annotation
      PromptPointResult pointRes = ed.GetPoint("Pick position of annotation");
      // if ok
      if (pointRes.Status == PromptStatus.OK)
      {
        // get the style id from the name input
        ObjectId styleId = PnIDStyleUtils.GetStyleIdFromName(annoStyleRes.StringResult, true);
          // now create the annotation object
        Annotation anno = new Annotation();
        // and place it
        anno.Create(pointRes.Value, styleId, pnidObjectRes.ObjectId);
      }
    }
  }    
}

