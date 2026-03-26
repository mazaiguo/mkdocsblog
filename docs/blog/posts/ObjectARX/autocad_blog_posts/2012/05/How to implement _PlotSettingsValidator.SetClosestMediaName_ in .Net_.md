---
title: "How to implement "PlotSettingsValidator.SetClosestMediaName" in .Net?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C#
  - Plot
description: "The comments in the Help Files about "PlotSettingsValidator.SetClosestMediaName" method mention:"
author: Autodesk
---
# How to implement "PlotSettingsValidator.SetClosestMediaName" in .Net?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-implement-plotsettingsvalidatorsetclosestmedianame-in-net.html

## 文章内容

By Philippe Leefsma
  The comments in the Help Files about "PlotSettingsValidator.SetClosestMediaName" method mention:
"This function is not implemented."
Below is a suggestion to implement this functionality in C# with the .Net API:
  [CommandMethod("SetClosestMediaNameCmd")]
public void SetClosestMediaNameCmd()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PlotSettingsValidator psv = PlotSettingsValidator.Current;
      // Let's first select the device
    StringCollection devlist = psv.GetPlotDeviceList();
      ed.WriteMessage("\n--- Plotting Devices ---");
      for (int i = 0; i < devlist.Count; ++i)
    {
        ed.WriteMessage("\n{0} - {1}", i+1, devlist[i]);
    }
      PromptIntegerOptions opts = new PromptIntegerOptions(
        "\nEnter device number: ");
      opts.LowerLimit = 1;
    opts.UpperLimit = devlist.Count;
    PromptIntegerResult pir = ed.GetInteger(opts);
      if(pir.Status != PromptStatus.OK)
        return;
      string device = devlist[pir.Value - 1];
      PromptDoubleOptions pdo1 = new PromptDoubleOptions(
        "\nEnter Media Height(mm): ");
        PromptDoubleResult pdr1 = ed.GetDouble(pdo1);
      if (pdr1.Status != PromptStatus.OK)
        return;
      PromptDoubleOptions pdo2 = new PromptDoubleOptions(
        "\nEnter Media Width(mm): ");
        PromptDoubleResult pdr2 = ed.GetDouble(pdo2);
      if (pdr2.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        LayoutManager layoutMgr = LayoutManager.Current;
          Layout layout = Tx.GetObject(
            layoutMgr.GetLayoutId(layoutMgr.CurrentLayout),
            OpenMode.ForWrite)
                 as Layout;
          setClosestMediaName(
            psv, device, layout,
            pdr1.Value, pdr2.Value,
            PlotPaperUnit.Millimeters, true);
          Tx.Commit();
    }
}
  void setClosestMediaName(PlotSettingsValidator psv,
    string device,
    Layout layout,
    double pageWidth,
    double pageHeight,
    PlotPaperUnit units,
    bool matchPrintableArea)   
{
    psv.SetPlotType(
        layout,
        Autodesk.AutoCAD.DatabaseServices.PlotType.Extents);
      psv.SetPlotPaperUnits(layout, units);
    psv.SetUseStandardScale(layout, false);
    psv.SetStdScaleType(layout, StdScaleType.ScaleToFit);
    psv.SetPlotConfigurationName(layout, device, null);
    psv.RefreshLists(layout);
      StringCollection mediaList =
        psv.GetCanonicalMediaNameList(layout);
      double smallestOffset = 0.0;
    string selectedMedia = string.Empty;
    PlotRotation selectedRot = PlotRotation.Degrees000;
      foreach(string media in mediaList)
    {
        psv.SetCanonicalMediaName(layout, media);
        psv.SetPlotPaperUnits(layout, units);
          double mediaPageWidth = layout.PlotPaperSize.X;
        double mediaPageHeight = layout.PlotPaperSize.Y;
          if(matchPrintableArea)
        {
              mediaPageWidth  -=
                  (layout.PlotPaperMargins.MinPoint.X +
                   layout.PlotPaperMargins.MaxPoint.X);
                mediaPageHeight -=
                  (layout.PlotPaperMargins.MinPoint.Y +
                   layout.PlotPaperMargins.MaxPoint.Y);
        }
          PlotRotation rotationType = PlotRotation.Degrees090;
          //Check that we are not outside the media print area
        if(mediaPageWidth < pageWidth ||
           mediaPageHeight < pageHeight)
        {
              //Check if 90°Rot will fit, otherwise check next media
              if(mediaPageHeight < pageWidth ||
                 mediaPageWidth >= pageHeight)
              {
                    //Too small, let's check next media
                    continue;
              }
                //That's ok 90°Rot will fit
              rotationType = PlotRotation.Degrees090;
        }
          double offset = Math.Abs(
            mediaPageWidth * mediaPageHeight -
            pageWidth * pageHeight);
          if (selectedMedia == string.Empty || offset < smallestOffset)
        {
            selectedMedia = media;
            smallestOffset = offset;
            selectedRot = rotationType;
              //Found perfect match so we can quit early
            if (smallestOffset == 0)
                break;
        }
    }
      psv.SetCanonicalMediaName(layout, selectedMedia);
    psv.SetPlotRotation(layout, selectedRot);
      string localMedia = psv.GetLocaleMediaName(
        layout,
        selectedMedia);
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      ed.WriteMessage("\n - Closest Media: " + localMedia);
    ed.WriteMessage("\n - Offset: " + smallestOffset.ToString());
    ed.WriteMessage("\n - Rotation: " + selectedRot.ToString());
}

## 评论

**内容**: Oleg said...
Thanks for the good work, Philippe!
This code is working like a sharm for me,
Regards,
Oleg
Reply
08/01/2012 at 07:16 AM

---
**内容**: Philippe Leefsma said...
No problem, you're welcome;)
Reply
09/20/2012 at 08:47 AM

---
**内容**: Carl said...
hmm. everywhere you have Layout, intellisense asks for PlotSettings in my studio...
Reply
03/12/2014 at 06:01 PM

---
**内容**: Oscar T said...
May be I'm wrong but I think there could be a typo. Shouldn't be the comparer ">=" be replaced with "<" in the previous code? In the section:
//Check if 90°Rot will fit, otherwise check next media
if(mediaPageHeight < pageWidth ||
mediaPageWidth >= pageHeight)
Reply
03/25/2017 at 01:11 PM

---
