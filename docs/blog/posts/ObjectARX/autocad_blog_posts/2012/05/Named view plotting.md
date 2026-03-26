---
title: "Named view plotting"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Plot
description: "Below code shows the procedure of plotting of named view to a PNG image using plotting API. Note, the code assumes that there is a named view with ..."
author: Autodesk
---
# Named view plotting

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/named-view-plotting.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure of plotting of named view to a PNG image using plotting API. Note, the code assumes that there is a named view with name “Test” in the model space.
[CommandMethod("NamedViewPlot")]
static public void NamedViewPlot()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tx =
                        db.TransactionManager.StartTransaction())
    {
         string deviceName = "PublishToWeb PNG.pc3";
         string mediaName = "VGA (640.00 x 480.00 Pixels)";
           BlockTable blockTable = tx.GetObject(db.BlockTableId,
                                  OpenMode.ForRead) as BlockTable;
         BlockTableRecord blockTableRecord = tx.GetObject(
                            blockTable[BlockTableRecord.ModelSpace],
                              OpenMode.ForRead) as BlockTableRecord;
           Layout plotPage = tx.GetObject(blockTableRecord.LayoutId,
                                       OpenMode.ForRead) as Layout;
           PlotInfo plotInfo = new PlotInfo();
         plotInfo.Layout = plotPage.Id;
           PlotSettings ps = new PlotSettings(plotPage.ModelType);
         ps.CopyFrom(plotPage);
           PlotSettingsValidator psv = PlotSettingsValidator.Current;
         psv.SetPlotViewName(ps, "Test");
         psv.SetPlotType(ps,
                   Autodesk.AutoCAD.DatabaseServices.PlotType.View);
         psv.SetUseStandardScale(ps, true);
         psv.SetPlotConfigurationName(ps,
                           deviceName, mediaName.Replace(" ", "_"));
         psv.SetPlotCentered(ps, true);
           psv.SetStdScaleType(ps, StdScaleType.ScaleToFit);
         psv.RefreshLists(ps);
           plotInfo.OverrideSettings = ps;
         PlotInfoValidator piv = new PlotInfoValidator();
         piv.Validate(plotInfo);
           object backgroundPlot =
                    Application.GetSystemVariable("BACKGROUNDPLOT");
         Application.SetSystemVariable("BACKGROUNDPLOT", 0);
           using (var pe = PlotFactory.CreatePublishEngine())
         {
             // Begin plotting a document.
             pe.BeginPlot(null, null);
             pe.BeginDocument(plotInfo,
                     doc.Name, null, 1, true, "c:\\temp\\test.png");
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
         Application.SetSystemVariable("BACKGROUNDPLOT",
                                backgroundPlot);//
           tx.Commit();
    }
}

## 评论

**内容**: Matus Brlit said...
Hi,
is it possible to plot from side-loaded database in 2012, or in 2013?
Reply
05/15/2012 at 04:36 AM

---
**内容**: Virupaksha aithal said...
No, you cannot plot the side or in memory database
Thanks
Viru
Reply
05/15/2012 at 05:05 AM

---
