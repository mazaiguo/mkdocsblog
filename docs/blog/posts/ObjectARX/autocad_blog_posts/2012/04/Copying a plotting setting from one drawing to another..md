---
title: "Copying a plotting setting from one drawing to another."
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - Database
  - Plot
description: "Below code shows the procedure to copy the plot setting from one drawing to the current drawing file."
author: Autodesk
---
# Copying a plotting setting from one drawing to another.

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/copying-a-plotting-setting-from-one-drawing-to-another.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to copy the plot setting from one drawing to the current drawing file.
[CommandMethod("CopyPlotSetting")]
static public void CopyPlotSetting()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database _db = doc.Database;
      using (Database _srDb = new Database(false, true))
    {
        _srDb.ReadDwgFile("c:\\temp\\testPlot.dwg",
            System.IO.FileShare.Read,
            true, null);
          using (Transaction _templateTr =
           _srDb.TransactionManager.StartTransaction())
        {
            using (Transaction _tr =
             _db.TransactionManager.StartTransaction())
            {
                DBDictionary dbDict = _templateTr.GetObject(
                                    _srDb.PlotSettingsDictionaryId,
                                    OpenMode.ForRead) as DBDictionary;
                if (dbDict != null)
                {
                    ObjectId settingsId = ObjectId.Null;
                    settingsId = dbDict.GetAt("TestPlotSetting");
                    PlotSettings settings = null;
                    settings =
                           _templateTr.GetObject(settingsId,
                                 OpenMode.ForRead) as PlotSettings;
                      PlotSettings newSettings =
                                new PlotSettings(true);
                      newSettings.CopyFrom(settings);
                    newSettings.AddToPlotSettingsDictionary(_db);
                    _tr.AddNewlyCreatedDBObject(newSettings, true);
                }
                _tr.Commit();
            }
            _templateTr.Commit();
        }
    }
}

## 评论

**内容**: Jonathan Clark said...
This is great code. I realized that it only works for plot settings that reside in model space. Can I get some direction on how to do the same thing with plot settings that are for layouts also.
Thanks.
Jonathan
Reply
07/01/2012 at 11:53 PM

---
**内容**: Virupaksha Aithal said...
Please try replacing
PlotSettings newSettings = new PlotSettings(true);
With
PlotSettings newSettings = new PlotSettings(settings.ModelType);
Thanks
Viru
Reply
07/03/2012 at 06:14 AM

---
**内容**: Achu said...
Can i get a code for copying model and layouts space of a current drawing and paste the same into a new drawing..
Reply
05/27/2015 at 04:18 AM

---
