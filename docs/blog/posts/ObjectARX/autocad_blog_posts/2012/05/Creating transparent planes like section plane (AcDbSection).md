---
title: "Creating transparent planes like section plane (AcDbSection)"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "I would like to create a transparent plane similar to section plane [command SECTIONPLANE]. How could I do it?"
author: Autodesk
---
# Creating transparent planes like section plane (AcDbSection)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-transparent-planes-like-section-plane-acdbsection.html

## 文章内容

By Adam Nagy
I would like to create a transparent plane similar to section plane [command SECTIONPLANE]. How could I do it?
Solution
The way section plane (AcDbSection) achieves this is drawing a simple line in 2D views and using a transparent material in 3D views and then setting the graphics system to use this even in Conceptual Visual Style, where materials are not used by default.
You could create a custom entity which does the same, or since AutoCAD 2010 you could simply take advantage of the Overrule API. In this case you can define an entity's behaviour and look in .NET as well.
This is what the following sample project code shows you how to do. This code can turn an existing regular region into a transparent one.
using System;
using System.Collections.Generic;
  using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.GraphicsInterface;
using Autodesk.AutoCAD.GraphicsSystem;
using Autodesk.AutoCAD.Geometry;
  namespace TransparentRegion
{
  public class RegionDrawOverrule : DrawableOverrule
  {
    // This could have any unique name
    // Best thing is to start it with your registered developer
    // symbol: mine is AEN1
    const string kTransparentRegionVisualStyle =
      "AEN1_REGION_VISUAL_STYLE_TRANSPARENT";
      // Function makes sure that the transparent style we want to
    // use exists
    public static ObjectId getVisualStyle()
    {
      Database db = HostApplicationServices.WorkingDatabase;
      ObjectId id = ObjectId.Null;
        using (Transaction tr =
        db.TransactionManager.StartTransaction())
      {
        DBDictionary dict = (DBDictionary)tr.GetObject(
          db.VisualStyleDictionaryId, OpenMode.ForRead);
          if (dict.Contains(kTransparentRegionVisualStyle))
        {
          id = dict.GetAt(kTransparentRegionVisualStyle);
        }
        else
        {
          // Create a new visual style and make sure it is using
          // tranparency
          DBVisualStyle style = new DBVisualStyle();
            style.Type = VisualStyleType.Custom;
          style.InternalUseOnly = true;
          style.SetTrait(VisualStyleProperty.FaceOpacity, .5,
            VisualStyleOperation.Set);
          style.SetTraitFlag(VisualStyleProperty.FaceModifier,
            (uint)VSFaceModifiers.FaceOpacityFlag, true);
            dict.UpgradeOpen();
          id = dict.SetAt(kTransparentRegionVisualStyle, style);
            tr.AddNewlyCreatedDBObject(style, true);
        }
          tr.Commit();
      }
        return id;
    }
      // This will override the regions look in 3D views
    public override bool WorldDraw(Drawable drawable, WorldDraw wd)
    {
      // Make sure the graphics system is using the transparent style
      // to draw our region
      wd.SubEntityTraits.VisualStyle = getVisualStyle();
        return base.WorldDraw(drawable, wd);
    }
  }
    public class Commands
  {
    static RegionDrawOverrule rdo = null;
    static List<ObjectId> regions = new List<ObjectId>();
      [CommandMethod("RegionMakeTransparent")]
    public void regionMakeTransparent()
    {
      Document doc = Application.DocumentManager.MdiActiveDocument;
      Editor ed = doc.Editor;
        // Ask the user to select a region he wants to make transparent
      PromptEntityResult per = ed.GetEntity("\nSelect a Region");
        if (per.Status != PromptStatus.OK)
        return;
        if (regions.Contains(per.ObjectId))
        return;
        regions.Add(per.ObjectId);
        if (rdo == null)
      {
        rdo = new RegionDrawOverrule();
          // Start using the overrule
        Overrule.AddOverrule(
          RXObject.GetClass(typeof(Region)), rdo, true);
        // Use id filter so that our overrule class will only be used
        // in case of the regions whose ids are in the regions list
        rdo.SetIdFilter(regions.ToArray());
        Overrule.Overruling = true;
      }
      else
      {
        rdo.SetIdFilter(regions.ToArray());
      }
        // Set the region modified, so that the graphics system will
      // redraw it and our overrule class will be called
      using (Transaction tr =
        doc.Database.TransactionManager.StartTransaction())
      {
        Entity reg =
          (Entity)tr.GetObject(per.ObjectId, OpenMode.ForWrite);
        reg.RecordGraphicsModified(true);
          tr.TransactionManager.QueueForGraphicsFlush();
          tr.Commit();
      }
    }
  }
}

