---
title: "Listing user defined page setup using .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Database
  - Plot
description: "User defined page setups are basically plotsetting objects that are stored in the dictionary "ACADPLOTSETTINGS". Below code shows the procedure to ..."
author: Autodesk
---
# Listing user defined page setup using .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/listing-user-defined-page-setup-using-net.html

## 文章内容

By Virupaksha Aithal
User defined page setups are basically plotsetting objects that are stored in the dictionary "ACAD_PLOTSETTINGS". Below code shows the procedure to list the user defined page setups.
[CommandMethod("ListPageSetup")]
static public void ListPageSetup()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx =
                db.TransactionManager.StartTransaction())
    {
        DBDictionary NOD =
                        Tx.GetObject(db.NamedObjectsDictionaryId,
                               OpenMode.ForRead) as DBDictionary;
            DBDictionary plotSettingsDic =
                    Tx.GetObject(db.PlotSettingsDictionaryId,
                               OpenMode.ForRead) as DBDictionary;
          foreach (DictionaryEntry dicoEntry in plotSettingsDic)
        {
            PlotSettings plotSettings =
                        Tx.GetObject((ObjectId)(dicoEntry.Value),
                                OpenMode.ForRead) as PlotSettings;
            ed.WriteMessage("\n - Page Setup: "
                    + dicoEntry.Key.ToString() + " PlotConfig: <" +
                         plotSettings.PlotConfigurationName + ">");
        }
          Tx.Commit();
    }
}

## 评论

**内容**: Tgr Br said...
How can I list only the Model Space plot setups? The code in the post lists the plot setups from the Model Space and from Layout Space.
Reply
04/28/2023 at 11:15 AM

---
**内容**: Keith Brown said...
Not sure if the previous poster ever found an answer but once you open the PlotSettings is has a value called ModelType which is a boolean to determine if it is modelSpace or not.
Reply
05/15/2023 at 01:40 PM

---
