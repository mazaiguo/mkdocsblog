---
title: "Gets and sets the current plot style for a layout"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Plot
description: "This example adds a command named "SetPlotSheet". When this command is run all of the available plot sheets are listed on the command line. Also if..."
author: Autodesk
---
# Gets and sets the current plot style for a layout

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/gets-and-sets-the-current-plot-style-for-a-layout.html

## 文章内容

By Virupaksha Aithal
This example adds a command named "SetPlotSheet". When this command is run all of the available plot sheets are listed on the command line. Also if the drawing is using .ctb files the stylesheet for the layout is set to "acad.ctb" if it is one of the available style sheets.
[CommandMethod("SetPlotSheet")]
public void SetPlotSheet()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        LayoutManager layManager = LayoutManager.Current;
        ObjectId layoutId =
                   layManager.GetLayoutId(layManager.CurrentLayout);
          Layout layoutObj =
                   (Layout)tr.GetObject(layoutId, OpenMode.ForWrite);
          ed.WriteMessage("Style sheet of current layout: "
                                + layoutObj.CurrentStyleSheet + "\n");
          PlotSettingsValidator plotSetVal =
                                       PlotSettingsValidator.Current;
        plotSetVal.RefreshLists(layoutObj);
          System.Collections.Specialized.StringCollection sheetList
                                = plotSetVal.GetPlotStyleSheetList();
        ed.WriteMessage("The list of available plot style sheets\n");
        foreach (String str in sheetList)
        {
            ed.WriteMessage(str + "\n");
            if (str.ToLower().Equals("acad.ctb"))
            {
                //find out if drawing is using ctb
                System.Object test =
                    Application.GetSystemVariable("PSTYLEMODE");
                if (test.ToString().Equals("1"))
                {
                    // drawing is using ctb so go ahead and
                    //assign acad.ctb to the layout
                    ed.WriteMessage("\nThe plot style sheet is" +
                                       " being set to acad.ctb\n\n");
                    plotSetVal.SetCurrentStyleSheet(layoutObj, str);
                }
                else
                {
                    ed.WriteMessage("\nUnable to set plot style in" +
                            " this example, drawing using stb\n\n");
                }
            }
        }
        tr.Commit();
    }
}

## 评论

**内容**: phg said...
Is this code run without exception?I try to run,but at the line :plotSetVal.SetCurrentStyleSheet(layoutObj, str);threw an exception,says eInvalid input...,and I check the help file,is says the first parameter should be PlotSettings instead of Layout.
Actually,my problem is no matter what style sheet I set,the line in the ploted file(pdf) always has it's color,but I want them all black.
Any suggestions?thank you.
Reply
05/13/2013 at 02:32 AM

---
**内容**: Johan B said in reply to phg...
Just found out that one needs to say "Use the Stylesetting".
Thus in VB this line:
acPlotSetValidator.SetCurrentStyleSheet (acPlotSettings, StyleSheet)
is followed by:
acPlotSettings.PlotPlotStyles = True
That works for me. (after few months of pulling my hear out)
Reply
10/31/2013 at 02:55 AM

---
