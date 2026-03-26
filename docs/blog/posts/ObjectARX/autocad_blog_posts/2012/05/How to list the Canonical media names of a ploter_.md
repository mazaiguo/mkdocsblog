---
title: "How to list the Canonical media names of a ploter?"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Plot
description: "The following sample code can retrieve the correct paper size defined in page setup dialog. In order to test the code, it assumes the page “PlotSet..."
author: Autodesk
---
# How to list the Canonical media names of a ploter?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-list-the-canonical-media-names-of-a-ploter.html

## 文章内容

By Xiaodong Liang
The following sample code can retrieve the correct paper size defined in page setup dialog. In order to test the code, it assumes the page “PlotSetName_HP” based on plotter HP LaserJet 8150 PCL 5 e. is available.
[CommandMethod("getCanName")]
public void getCanName()
{
    // assume a plot setting exists
    string strPlotSetName = "PlotSetName_HP";
    bool PlotSettingExists = false;
      StringCollection strMediaNameList = null;
      Editor editor =
        Autodesk.AutoCAD.ApplicationServices.
        Application.DocumentManager.MdiActiveDocument.Editor;
    Database db = editor.Document.Database;
      using (Transaction t = 
                db.TransactionManager.StartTransaction())
    {
        try
        {
            // get PlotSettings Dictionary
            DBDictionary psDicts =
                (DBDictionary)t.GetObject(
                db.PlotSettingsDictionaryId,
                OpenMode.ForRead);
            foreach (
                System.Collections.DictionaryEntry psDict
                in psDicts)
            {
                object o = psDict.Value;
                string key = (string)psDict.Key;
                if (key == strPlotSetName)
                {
                    // find the plot setting
                    PlotSettingExists = true;
                }
            }
              if (PlotSettingExists)
            {
                // open the plot setting dictionary
                DBDictionary plotsettingdic =
                    (DBDictionary)t.GetObject(
                    db.PlotSettingsDictionaryId,
                    OpenMode.ForRead);
                  // open the setting
                PlotSettings setting =
                    (PlotSettings)t.GetObject(
                    plotsettingdic.GetAt(strPlotSetName),
                    OpenMode.ForWrite);
                  // get PlotSettingsValidator
                PlotSettingsValidator psv =
                    Autodesk.AutoCAD.DatabaseServices.
                    PlotSettingsValidator.Current;
                  psv.RefreshLists(setting);
                  // get the media name list
                strMediaNameList =
                    psv.GetCanonicalMediaNameList(setting);
                editor.WriteMessage("Media Name List:\n");
                foreach (String str in strMediaNameList)
                {
                    editor.WriteMessage(str + "\n");
                }
              }
            t.Commit();
          }
        catch (System.Exception ex)
        {
            editor.WriteMessage(ex.Message);
        }
        ///////------------------------------
    }
  }

## 评论

**内容**: Account Deleted said...
Hi, Xiaodong!
I have a question why it was necessary to open db.PlotSettingsDictionaryId with OpenMode.ForWrite. Can be enough OpenMode.ForRead?
Reply
05/16/2012 at 03:36 AM

---
**内容**: Xiaodong Liang said...
Hi Alex,
you are right. Opening for read is enough. Thanks for spotting this.
Cheers,
Xiaodong
Reply
05/16/2012 at 11:03 PM

---
**内容**: Jason Booth said...
Hello,
I tried to use this code as reference, but I am still having the same issue.
I have a pc3 file with a filtered list of paper sizes, but the GetCanonicalMediaNameList() returns all possible paper sizes.
Is there a way to use this API to return only the filtered paper sizes (filtered in the same way as in the plot dialog)?
Regards,
Jason Booth
Reply
02/19/2013 at 07:25 AM

---
**内容**: Xiaodong Liang said in reply to Jason Booth...
Unfortunately, there is no API to return the filtering CanonicalMediaNames of a provided PC3 file.
Reply
03/01/2013 at 02:25 AM

---
**内容**: اِحسان بَحرانی said...
hi
its not work!
theres nothing in psDicts, the count of items is zero!
Reply
03/31/2019 at 04:56 AM

---
**内容**: EhsanBahrani said in reply to اِحسان بَحرانی...
to change plotter in SetPlotConfigurationName we need plotter and canonicalmedianame, is there a way to change plotter without knowing this?!
i want to set plotter first, and then get list of canonicalmedianames, so the user can select one of them.
can you help me via this?!
i want to get canonicalmedianames of specific plotter device, so how to get it?
Reply
03/31/2019 at 04:58 AM

---
