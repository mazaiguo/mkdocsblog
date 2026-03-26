---
title: "Publishing model views to a multi-sheet DWF/PDF"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - PDF
  - Plot
description: "An approach to create a single multi-sheet PDF or DWF file that displays portions of your drawing as separate sheets is to create model views and g..."
author: Autodesk
---
# Publishing model views to a multi-sheet DWF/PDF

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/publishing-model-views-to-a-multi-sheet-dwfpdf.html

## 文章内容

By Balaji Ramamoorthy
An approach to create a single multi-sheet PDF or DWF file that displays portions of your drawing as separate sheets is to create model views and get them published.
Here is a sample code to publish two model views named "Test1" and "Test2" as separate sheets in a multi-sheet DWF file.
using Autodesk.AutoCAD.PlottingServices;
using Autodesk.AutoCAD.Publishing;
  [CommandMethod("PublishViews2MultiSheet")]
static public void PublishViews2MultiSheet()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      StringCollection viewsToPlot = new StringCollection();
    viewsToPlot.Add("Test1");
    viewsToPlot.Add("Test2");
      // Create page setup based on the views
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ObjectId layoutId = LayoutManager.Current.GetLayoutId
                        (LayoutManager.Current.CurrentLayout);
          Layout layout
            = Tx.GetObject(layoutId, OpenMode.ForWrite) as Layout;
          foreach (String viewName in viewsToPlot)
        {
            PlotSettings plotSettings
                           = new PlotSettings(layout.ModelType);
            plotSettings.CopyFrom(layout);
              PlotSettingsValidator psv
                                = PlotSettingsValidator.Current;
              psv.SetPlotConfigurationName
                (   plotSettings,
                    "DWF6 ePlot.pc3",
                    "ANSI_A_(8.50_x_11.00_Inches)"
                );
            psv.RefreshLists(plotSettings);
            psv.SetPlotViewName(plotSettings, viewName);
            psv.SetPlotType
                (
                    plotSettings,
                    PlotType.View
                );
            psv.SetUseStandardScale(plotSettings, true);
            psv.SetStdScaleType
                (
                    plotSettings,
                    StdScaleType.ScaleToFit
                );
            psv.SetPlotCentered(plotSettings, true);
            psv.SetPlotRotation
                (
                    plotSettings,
                    PlotRotation.Degrees000
                );
            psv.SetPlotPaperUnits
                (
                    plotSettings,
                    PlotPaperUnit.Inches
                );
              plotSettings.PlotSettingsName
                    = String.Format("{0}{1}", viewName, "PS");
            plotSettings.PrintLineweights = true;
            plotSettings.AddToPlotSettingsDictionary(db);
              Tx.AddNewlyCreatedDBObject(plotSettings, true);
            psv.RefreshLists(plotSettings);
              layout.CopyFrom(plotSettings);
        }
          Tx.Commit();
    }
      //put the plot in foreground
    short bgPlot = (short)Application.GetSystemVariable("BACKGROUNDPLOT");
    Application.SetSystemVariable("BACKGROUNDPLOT", 0);
      string dwgFileName
            = Application.GetSystemVariable("DWGNAME") as string;
    string dwgPath
        = Application.GetSystemVariable("DWGPREFIX") as string;
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DsdEntryCollection collection = new DsdEntryCollection();
        ObjectId activeLayoutId
            = LayoutManager.Current.GetLayoutId
                        (LayoutManager.Current.CurrentLayout);
          foreach (String viewName in viewsToPlot)
        {
            Layout layout = Tx.GetObject(
                                            activeLayoutId,
                                            OpenMode.ForRead
                                        ) as Layout;
              DsdEntry entry = new DsdEntry();
              entry.DwgName = dwgPath + dwgFileName;
            entry.Layout = layout.LayoutName;
            entry.Title = viewName;
            entry.NpsSourceDwg = entry.DwgName;
            entry.Nps = String.Format("{0}{1}", viewName, "PS");
              collection.Add(entry);
        }
          // remove the ".dwg" extension
        dwgFileName = dwgFileName.Substring(0, dwgFileName.Length - 4);
          DsdData dsdData = new DsdData();
          dsdData.SheetType = SheetType.MultiDwf;
        dsdData.ProjectPath = dwgPath;
        dsdData.DestinationName
                = dsdData.ProjectPath + dwgFileName + ".dwf";
          if (System.IO.File.Exists(dsdData.DestinationName))
            System.IO.File.Delete(dsdData.DestinationName);
          dsdData.SetDsdEntryCollection(collection);
          string dsdFile
                = dsdData.ProjectPath + dwgFileName + ".dsd";
          //Workaround to avoid promp for pdf file name
        //set PromptForDwfName=FALSE in dsdData using StreamReader/StreamWriter
          dsdData.WriteDsd(dsdFile);
          System.IO.StreamReader sr = new System.IO.StreamReader(dsdFile);
        string str = sr.ReadToEnd();
        sr.Close();
          // Replace PromptForDwfName
        str = str.Replace("PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
          // Workaround to have the page setup names included in the DSD file
        // Replace Setup names based on the created page setups
        // May not be required if Nps is output to the DSD
        int occ = 0;
        int index = str.IndexOf("Setup=");
        int startIndex = 0;
        StringBuilder dsdText = new StringBuilder();
        while(index != -1)
        {
            // 6 for length of "Setup="
            String str1 =
            str.Substring(startIndex, index + 6 - startIndex );
              dsdText.Append(str1);
            dsdText.Append(
                String.Format("{0}{1}", viewsToPlot[occ], "PS"));
              startIndex = index + 6;
            index = str.IndexOf("Setup=", index + 6);
              if (index == -1)
            {
                dsdText.Append(
               str.Substring(startIndex, str.Length-startIndex));
            }
            occ++;
        }
          // Write the DSD
        System.IO.StreamWriter sw
                        = new System.IO.StreamWriter(dsdFile);
        sw.Write( dsdText.ToString());
        sw.Close();
          // Read the updated DSD file
        dsdData.ReadDsd(dsdFile);
          // Erase DSD as it is no longer needed
        System.IO.File.Delete(dsdFile);
          PlotConfig plotConfig
            = PlotConfigManager.SetCurrentConfig("DWF6 ePlot.pc3");
          Publisher publisher = Application.Publisher;
          // Publish it
        publisher.PublishExecute(dsdData, plotConfig);
          Tx.Commit();
    }
      //reset the background plot value
    Application.SetSystemVariable("BACKGROUNDPLOT", bgPlot);
Here is a sample drawing to try the code :
Download Sample

