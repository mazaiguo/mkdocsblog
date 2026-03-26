---
title: "Assigining programatically the PLOTSTYLE"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plot
description: "PlotStyleNames are just entries in the plotStyleName Dictionary (ACADPLOTSTYLENAME). The plotStyleName is used as a lookup name when AutoCAD looks ..."
author: Autodesk
---
# Assigining programatically the PLOTSTYLE

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/assigining-programatically-the-plotstyle.html

## 文章内容

By Virupaksha Aithal
PlotStyleNames are just entries in the plotStyleName Dictionary (ACAD_PLOTSTYLENAME). The plotStyleName is used as a lookup name when AutoCAD looks for a plotStyle. You can create new PlaceHolder object and add it to the plotStyleName dictionary using your desired plotStyleName as the entry's key placeholder.
Note that the plotStyleName dictionary has a default entry "Normal" of AcDbPlaceHolder class. And the setPlotStyleName function returns an error status if the plot style cannot be found in the current plot style table (as this case), or if the drawing's PlotStyleMode is set to use color-based plot styles
[CommandMethod("PlotStyleName")]
static public void PlotStyleName()
{
    DictionaryWithDefaultDictionary dict = null;
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId psDictId = db.PlotStyleNameDictionaryId;
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        string newStyleName = "Test";
        dict = (DictionaryWithDefaultDictionary)tr.GetObject(
                                        psDictId, OpenMode.ForRead);
          if (!dict.Contains(newStyleName))
        {
            dict.UpgradeOpen();
              PlaceHolder newHolder = new PlaceHolder();
            dict.SetAt(newStyleName, newHolder);
            tr.AddNewlyCreatedDBObject(newHolder, true);
        }
          LayerTableRecord lyrRcd;
        using (lyrRcd = (LayerTableRecord)tr.GetObject(db.Clayer,
                                                  OpenMode.ForWrite))
        {
            lyrRcd.PlotStyleName = newStyleName;
        }
        tr.Commit();
    }
}

