---
title: "Use LayerFilterTree to add a new Layer Filter"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Layer
description: "Here is a C# example that creates a new layer filter. If a layer filter named "MyFilter" already exists, the code makes it the active Layer Filter ..."
author: Autodesk
---
# Use LayerFilterTree to add a new Layer Filter

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/use-layerfiltertree-to-add-a-new-layer-filter.html

## 文章内容

By Wayne Brill
Here is a C# example that creates a new layer filter. If a layer filter named "MyFilter" already exists, the code makes it the active Layer Filter instead of creating a new one.
[CommandMethod("addFilt")]
public void addLayerFilter()
{
    Editor ed = Application.DocumentManager.
                    MdiActiveDocument.Editor;
      try
    {
        // Access tree of layer filters.
        LayerFilterTree lyrTree =
            HostApplicationServices.
                 WorkingDatabase.LayerFilters;
          int fltCount = lyrTree.Root.
                          NestedFilters.Count;
          for (int i = 0; i <= fltCount - 1; i++)
        {
            LayerFilter lyrFilt = lyrTree.Root.
                               NestedFilters[i];
            if (lyrFilt.Name == "MyFilter")
            {
                ed.WriteMessage
("\nMyFilter already exists, making it current");
                // This is the way I found to
                // make a Layer Filter current
                //use LayerFilterTree constructor
                LayerFilterTree lyrTree2 =
                     new LayerFilterTree
                           (lyrTree.Root, lyrFilt);
                HostApplicationServices.
                    WorkingDatabase.LayerFilters =
                                          lyrTree2;
                return;
              }
        }
          // If we get here then Layer
        // Filter named MyFilter does not exist
        // create it
        LayerFilter lyrFilt2 = new LayerFilter();
        lyrFilt2 = new LayerFilter();
        lyrFilt2.Name = "MyFilter";
        lyrFilt2.FilterExpression =
                            "NAME==\"WBLayer*\"";
        // Add the Layer Filter to the
        // NestedFilters of the LayerFilters
        lyrTree.Root.NestedFilters.Add(lyrFilt2);
        // Use the constructor to make the Layer
        // Filter current
        // and update the Layer Palette. Without
        // this you can run the
        // LAYER command and see the new
        // layer filter
        lyrTree = new LayerFilterTree
                         (lyrTree.Root, lyrFilt2);
        HostApplicationServices.WorkingDatabase.
                           LayerFilters = lyrTree;
    }
    catch (System.Exception ex)
    {
        // Do something here
        ed.WriteMessage("Oops!" + ex.ToString());
    }
}

