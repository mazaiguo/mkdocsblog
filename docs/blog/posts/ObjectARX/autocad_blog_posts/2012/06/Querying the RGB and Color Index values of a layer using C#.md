---
title: "Querying the RGB and Color Index values of a layer using C#"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Database
  - Layer
  - Plot
description: "Here’s a simple C# code snippet showing how to access the RGB color and color index values for a layer. The code iterates all LayerTableRecords in ..."
author: Autodesk
---
# Querying the RGB and Color Index values of a layer using C#

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/querying-the-rgb-and-color-index-values-of-a-layer-using-c.html

## 文章内容

By Stephen Preston
Here’s a simple C# code snippet showing how to access the RGB color and color index values for a layer. The code iterates all LayerTableRecords in the drawing and prints the values we’re querying to the command line.
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Colors;
  namespace LayerColor
{
  public class GetRGBValuesClass
  {
    public GetRGBValuesClass()
    {
    }
      [CommandMethod("GetRGB")]
    public void GetRGB()
    {
      Database dBase =
               Application.DocumentManager.MdiActiveDocument.Database;
      Autodesk.AutoCAD.DatabaseServices.TransactionManager tm =
                                  dBase.TransactionManager;
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction myT = tm.StartTransaction())
      {
        try
        {
            LayerTable lt = (LayerTable)tm.GetObject(dBase.LayerTableId,
                                                  OpenMode.ForRead);
          //Iterate all records in table
          foreach (ObjectId ltrId in lt)
          {
            LayerTableRecord ltr = (LayerTableRecord)tm.GetObject(ltrId, OpenMode.ForRead);
            Color colour = ltr.Color;
            ed.WriteMessage("\nThe name of the layer is: " +
                                                ltr.Name.ToString());
            ed.WriteMessage("\nRed: " + colour.ColorValue.R.ToString());
            ed.WriteMessage("\nGreen: " + colour.ColorValue.G.ToString());
            ed.WriteMessage("\nBlue: " + colour.ColorValue.B.ToString());
            ed.WriteMessage("\nColor Index value of the layer is:" +
                                colour.ColorIndex.ToString() + "\n");
          }
          myT.Commit();
        }
        catch (Autodesk.AutoCAD.Runtime.Exception e1)
        {
          //Handle errors
        }
      }
    }
  }
}

