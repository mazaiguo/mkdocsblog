---
title: "Setting plot configuration to "none""
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Database
  - Plot
description: "Below code shows the procedure to set the plot configuration to "none". Code sets the model space plot configuration to “none”."
author: Autodesk
---
# Setting plot configuration to "none"

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/setting-plot-configuration-to-none.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to set the plot configuration to "none". Code sets the model space plot configuration to “none”.
[CommandMethod("setNonePlotConfig")]
static public void setNonePlotConfig()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      PlotSettingsValidator psv = PlotSettingsValidator.Current;
    LayoutManager layoutMgr = LayoutManager.Current;
      ObjectId layoutId = layoutMgr.GetLayoutId("Model");
      using (Transaction Tx =
                        db.TransactionManager.StartTransaction())
    {
        Layout layout =
            Tx.GetObject(layoutId, OpenMode.ForWrite) as Layout;
        psv.SetPlotConfigurationName(layout,
                                     "None", "none_user_media");
        Tx.Commit();
    }
}

## 评论

**内容**: Maxence DELANNOY said...
PlotConfigManager.get_StdConfigNames(StdConfiguration.NoneDevice) should be used instead of litteral "None"
Reply
11/15/2012 at 05:34 AM

---
