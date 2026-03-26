---
title: "How to use Autodesk.AutoCAD. Publishing.Publisher.PublishExecute?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoCAD
  - C#
description: "The following C# sample shows you how to publish to DWF all layouts in a drawing. It illustrates the use of Autodesk.AutoCAD.Publishing.Publisher.P..."
author: Autodesk
---
# How to use Autodesk.AutoCAD. Publishing.Publisher.PublishExecute?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-use-autodeskautocadpublishingpublisherpublishexecute.html

## 文章内容

By Philippe Leefsma 
The following C# sample shows you how to publish to DWF all layouts in a drawing. It illustrates the use of Autodesk.AutoCAD.Publishing.Publisher.PublishExecute API.
//////////////////////////////////////////////////////////////////////////
//Use: This command will publish all the layouts in the current
//      drawing to a multi sheet dwf.
//////////////////////////////////////////////////////////////////////////
[CommandMethod("PublishAllLayouts")]
static public void PublishAllLayouts()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      //put the plot in foreground
    short bgPlot =
        (short)Application.GetSystemVariable("BACKGROUNDPLOT");
      Application.SetSystemVariable("BACKGROUNDPLOT", 0);
      //get the layout ObjectId List
    System.Collections.Generic.List<ObjectId> layoutIds =
        GetLayoutIds(db);
      string dwgFileName =
        (string)Application.GetSystemVariable("DWGNAME");
      string dwgPath = ¨
        (string)Application.GetSystemVariable("DWGPREFIX");
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DsdEntryCollection collection = new DsdEntryCollection();
          foreach (ObjectId layoutId in layoutIds)
        {
            Layout layout = Tx.GetObject(layoutId, OpenMode.ForRead)
                as Layout;
              DsdEntry entry = new DsdEntry();
                        entry.DwgName = dwgPath + dwgFileName;
            entry.Layout = layout.LayoutName;
            entry.Title = "Layout_" + layout.LayoutName;
            entry.NpsSourceDwg = entry.DwgName;
            entry.Nps = "Setup1";
              collection.Add(entry);
        }
          dwgFileName = dwgFileName.Substring(
            0, dwgFileName.Length - 4);
          DsdData dsdData = new DsdData();
          dsdData.SheetType = SheetType.MultiDwf; //SheetType.MultiPdf
        dsdData.ProjectPath = dwgPath;
        dsdData.DestinationName =
            dsdData.ProjectPath + dwgFileName + ".dwf";
          if (System.IO.File.Exists(dsdData.DestinationName))
            System.IO.File.Delete(dsdData.DestinationName);
          dsdData.SetDsdEntryCollection(collection);
          string dsdFile = dsdData.ProjectPath + dwgFileName + ".dsd";
          //Workaround to avoid promp for dwf file name
        //set PromptForDwfName=FALSE in dsdData using
        //StreamReader/StreamWriter
                dsdData.WriteDsd(dsdFile);
          System.IO.StreamReader sr =
            new System.IO.StreamReader(dsdFile);
          string str = sr.ReadToEnd();
        sr.Close();
          str = str.Replace(
            "PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
          System.IO.StreamWriter sw =
            new System.IO.StreamWriter(dsdFile);
          sw.Write(str);
        sw.Close();
          dsdData.ReadDsd(dsdFile);
        System.IO.File.Delete(dsdFile);
          PlotConfig plotConfig = Autodesk.AutoCAD.PlottingServices.
            PlotConfigManager.SetCurrentConfig("DWF6 ePlot.pc3");
          //PlotConfig pc = Autodesk.AutoCAD.PlottingServices.
        //  PlotConfigManager.SetCurrentConfig("DWG To PDF.pc3");
          Autodesk.AutoCAD.Publishing.Publisher publisher = 
            Autodesk.AutoCAD.ApplicationServices.
            Application.Publisher;
          publisher.AboutToBeginPublishing +=
            new Autodesk.AutoCAD.Publishing.
                AboutToBeginPublishingEventHandler(
                    Publisher_AboutToBeginPublishing);
          publisher.PublishExecute(dsdData, plotConfig);
          Tx.Commit();
    }
      //reset the background plot value
    Application.SetSystemVariable("BACKGROUNDPLOT", bgPlot);
}
  private static System.Collections.Generic.List<ObjectId>
    GetLayoutIds(Database db)
{
    System.Collections.Generic.List<ObjectId> layoutIds =
        new System.Collections.Generic.List<ObjectId>();
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DBDictionary layoutDic = Tx.GetObject(
            db.LayoutDictionaryId,
            OpenMode.ForRead, false)
                as DBDictionary;
          foreach (DBDictionaryEntry entry in layoutDic)
        {
            layoutIds.Add(entry.Value);
        }
    }
      return layoutIds;
}
  static void Publisher_AboutToBeginPublishing(
    object sender,
    Autodesk.AutoCAD.Publishing.AboutToBeginPublishingEventArgs e)
{
    Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
        "\nAboutToBeginPublishing!!");
}
      The following sample uses a similar approach but illustrates how to use "PublishExecute" API to batch plot layouts from several different drawings without need to worry about synchronization issues linked to opening/closing the files:
//////////////////////////////////////////////////////////////////////////
//Use: Will batch publish to single dwf every layout of
//      each document provided as input
//     Make sure each of your drawing contains a page setup
//      named Setup1 before running.
//          
//////////////////////////////////////////////////////////////////////////
[CommandMethod("BatchPublishCmd", CommandFlags.Session)]
static public void BatchPublishCmd()
{
    short bgPlot =
        (short)Application.GetSystemVariable("BACKGROUNDPLOT");
      Application.SetSystemVariable("BACKGROUNDPLOT", 0);
      System.Collections.Generic.List<string> docsToPlot =
        new System.Collections.Generic.List<string>();
      docsToPlot.Add("C:\\Temp\\Drawing1.dwg");
    docsToPlot.Add("C:\\Temp\\Drawing2.dwg");
    docsToPlot.Add("C:\\Temp\\Drawing3.dwg");
      BatchPublish(docsToPlot);
}
  static public void BatchPublish(
    System.Collections.Generic.List<string> docsToPlot)
{
    DsdEntryCollection collection = new DsdEntryCollection();
      Document doc = Application.DocumentManager.MdiActiveDocument;
      foreach (string filename in docsToPlot)
    {
        using (DocumentLock doclock = doc.LockDocument())
        {
            Database db = new Database(false, true);
              db.ReadDwgFile(
                filename, System.IO.FileShare.Read, true, "");
              System.IO.FileInfo fi = new System.IO.FileInfo(filename);
              string docName =
                fi.Name.Substring(0, fi.Name.Length - 4);
              using (Transaction Tx =
                db.TransactionManager.StartTransaction())
            {
                foreach (ObjectId layoutId in getLayoutIds(db))
                {
                    Layout layout = Tx.GetObject(
                        layoutId,
                        OpenMode.ForRead)
                            as Layout;
                      DsdEntry entry = new DsdEntry();
                      entry.DwgName = filename;
                    entry.Layout = layout.LayoutName;
                    entry.Title = docName + "_" + layout.LayoutName;
                    entry.NpsSourceDwg = entry.DwgName;
                    entry.Nps = "Setup1";
                      collection.Add(entry);
                }
                  Tx.Commit();
            }
        }
    }
      DsdData dsdData = new DsdData();
      dsdData.SheetType = SheetType.SingleDwf;
    dsdData.ProjectPath = "C:\\Temp";
      //Not used for "SheetType.SingleDwf"
    //dsdData.DestinationName = dsdData.ProjectPath + "\\output.dwf";
      dsdData.SetDsdEntryCollection(collection);
      string dsdFile = dsdData.ProjectPath + "\\dsdData.dsd";
      //Workaround to avoid promp for dwf file name
    //set PromptForDwfName=FALSE in dsdData
    //using StreamReader/StreamWriter
      if (System.IO.File.Exists(dsdFile))
        System.IO.File.Delete(dsdFile);
      dsdData.WriteDsd(dsdFile);
      System.IO.StreamReader sr = new System.IO.StreamReader(dsdFile);
    string str = sr.ReadToEnd();
    sr.Close();
      str = str.Replace(
        "PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
      System.IO.StreamWriter sw = new System.IO.StreamWriter(dsdFile);
    sw.Write(str);
    sw.Close();
      dsdData.ReadDsd(dsdFile);
    System.IO.File.Delete(dsdFile);
      PlotConfig plotConfig =
        Autodesk.AutoCAD.PlottingServices.
            PlotConfigManager.SetCurrentConfig("DWF6 ePlot.pc3");
      Autodesk.AutoCAD.Publishing.Publisher publisher =
        Autodesk.AutoCAD.ApplicationServices.Application.Publisher;
      publisher.PublishExecute(dsdData, plotConfig);
}
  private static System.Collections.Generic.List<ObjectId>
    getLayoutIds(Database db)
{
    System.Collections.Generic.List<ObjectId> layoutIds =
        new System.Collections.Generic.List<ObjectId>();
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DBDictionary layoutDic = Tx.GetObject(
            db.LayoutDictionaryId,
            OpenMode.ForRead, false)
                as DBDictionary;
          foreach (DBDictionaryEntry entry in layoutDic)
        {
            layoutIds.Add(entry.Value);
        }
    }
      return layoutIds;
}

## 评论

**内容**: Peter said...
Hello Philippe
I run your code (Autocad Mechanical 2012). But the event
"AboutToBeginPublishing" does not fire. Do you know why this could happen?
Best regards Peter
Reply
07/05/2012 at 04:25 AM

---
**内容**: Philippe Leefsma said in reply to Peter ...
Yes this is a known issue unfortunately. Those events do not work in 2012/2013.
Give a try at PlotEvents, those should work:
[CommandMethod("PlotEvents")]
static public void PlotEvents()
{
PlotReactorManager plotReactorMng = new PlotReactorManager();
plotReactorMng.BeginDocument += new BeginDocumentEventHandler(plotReactorMng_BeginDocument);
plotReactorMng.BeginPage += new BeginPageEventHandler(plotReactorMng_BeginPage);
plotReactorMng.BeginPlot += new BeginPlotEventHandler(plotReactorMng_BeginPlot);
plotReactorMng.EndDocument += new EndDocumentEventHandler(plotReactorMng_EndDocument);
plotReactorMng.EndPage += new EndPageEventHandler(plotReactorMng_EndPage);
plotReactorMng.EndPlot += new EndPlotEventHandler(plotReactorMng_EndPlot);
}
static void plotReactorMng_BeginDocument(object sender, BeginDocumentEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::BeginDocument " + e.FileName);
}
static void plotReactorMng_BeginPage(object sender, BeginPageEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::BeginPage");
}
static void plotReactorMng_BeginPlot(object sender, BeginPlotEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::BeginPlot");
}
static void plotReactorMng_EndPlot(object sender, EndPlotEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::EndPlot");
}
static void plotReactorMng_EndPage(object sender, EndPageEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::EndPage");
}
static void plotReactorMng_EndDocument(object sender, EndDocumentEventArgs e)
{
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
ed.WriteMessage("\nPlotReactor::EndDocument");
}
Reply
07/16/2012 at 05:48 AM

---
**内容**: Sanjay Kulkarni said...
It seems that this code works only in A2012 and above. Am I right?
What if we have A2011.
Reply
07/16/2012 at 12:54 AM

---
**内容**: Philippe Leefsma said in reply to Sanjay Kulkarni...
Sorry what do you mean exactly by it only works in 2012 and above? What behavior do you experience under 2011? it doesn't publish anything or the events are not fired...? Can you be more specific? Thank you.
Reply
07/16/2012 at 05:50 AM

---
**内容**: Maxence said...
Don't you have to call Dispose on the databases at the end ? And why do you have to lock the active document ?
If I understand well, all the drawings need to be loaded in memory. If I want to publish 1000 drawings in a single DWF, I've to open the 1000 files.
Reply
08/30/2012 at 02:46 AM

---
**内容**: Philippe said...
Hi Maxence,
Since no modification is done to the document, you are right, it shouldn't be required to lock it.
The database doesn't have to be disposed, it should be garbage collected by the .Net framework as it goes out of scope. As it is created in a loop, I would not expect having 1000 drawing loaded in memory at the same time.
Reply
08/30/2012 at 02:57 AM

---
**内容**: Nikus said...
I know it's an old post but for people who are using this code with special char, don't forget to add encoding in the work around :
//Workaround to avoid promp for dwf file name set PromptForDwfName=FALSE in dsdData using StreamReader/StreamWriter
dsdData.WriteDsd(dsdFile);
System.IO.StreamReader sr = new System.IO.StreamReader(dsdFile, Encoding.Default);
string str = sr.ReadToEnd();
sr.Close();
str = str.Replace("PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
System.IO.StreamWriter sw = new System.IO.StreamWriter(dsdFile, false, Encoding.Default);
Reply
01/27/2021 at 09:40 AM

---
**内容**: dba said in reply to Nikus...
Hello, could someone even manage Eventhandling here? I'd like to cleanup after publishing, but apparently the eventhandling is still an issue (Autocad 2022).
Any hints are highly appreciated!
Reply
10/24/2022 at 12:44 AM

---
