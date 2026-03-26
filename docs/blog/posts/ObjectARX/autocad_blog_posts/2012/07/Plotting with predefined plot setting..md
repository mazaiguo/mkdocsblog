---
title: "Plotting with predefined plot setting."
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Database
  - Plot
description: "You can use the .NET API to plot with defined plot settings. Below code demonstrates the procedure for the same. Code, first ask for the plot setti..."
author: Autodesk
---
# Plotting with predefined plot setting.

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/plotting-with-predefined-plot-setting.html

## 文章内容

By Virupaksha Aithal
You can use the .NET API to plot with defined plot settings. Below code demonstrates the procedure for the same. Code, first ask for the plot setting name and make sure that the plot setting is suitable for current layout (model/paper space).
[CommandMethod("PlotPageSetup")]
static public void PlotPageSetup()
{
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptStringOptions opts =
                new PromptStringOptions("Enter plot setting name");
    opts.AllowSpaces = true;
    PromptResult settingName = ed.GetString(opts);
      if (settingName.Status != PromptStatus.OK)
        return;
      using (Transaction Tx =
                db.TransactionManager.StartTransaction())
    {
          LayoutManager layManager = LayoutManager.Current;
        ObjectId layoutId =
                   layManager.GetLayoutId(layManager.CurrentLayout);
          Layout layoutObj =
                   (Layout)Tx.GetObject(layoutId, OpenMode.ForRead);
          DBDictionary plotSettingsDic =
           (DBDictionary)Tx.GetObject(db.PlotSettingsDictionaryId,
                                                   OpenMode.ForRead);
          if (!plotSettingsDic.Contains(settingName.StringResult))
            return;
            ObjectId plotsetting =
                    plotSettingsDic.GetAt(settingName.StringResult);
        //layout type
        bool bModel = layoutObj.ModelType;
          PlotSettings plotSettings = Tx.GetObject(plotsetting,
                                  OpenMode.ForRead) as PlotSettings;
          if (plotSettings.ModelType != bModel)
        {
            return;
        }
        object backgroundPlot =
           Application.GetSystemVariable("BACKGROUNDPLOT");
          Application.SetSystemVariable("BACKGROUNDPLOT", 0);
          try
        {
            //now plot the setup...
            PlotInfo plotInfo = new PlotInfo();
            plotInfo.Layout = layoutObj.ObjectId;
            plotInfo.OverrideSettings = plotSettings;
              PlotInfoValidator piv = new PlotInfoValidator();
            piv.Validate(plotInfo);
                string outName = "c:\\temp\\"
                                + plotSettings.PlotSettingsName;
              using (var pe = PlotFactory.CreatePublishEngine())
            {
                // Begin plotting a document.
                pe.BeginPlot(null, null);
                pe.BeginDocument(plotInfo,
                        doc.Name, null, 1, true, outName);
                  // Begin plotting the page.
                PlotPageInfo ppi = new PlotPageInfo();
                pe.BeginPage(ppi, plotInfo, true, null);
                pe.BeginGenerateGraphics(null);
                pe.EndGenerateGraphics(null);
                  // Finish the sheet
                pe.EndPage(null);
                  // Finish the document
                pe.EndDocument(null);
                  //// And finish the plot
                pe.EndPlot(null);
            }
          }
        catch
        {
        }
          Tx.Commit();
          Application.SetSystemVariable("BACKGROUNDPLOT",
                         backgroundPlot);//
    }
}

