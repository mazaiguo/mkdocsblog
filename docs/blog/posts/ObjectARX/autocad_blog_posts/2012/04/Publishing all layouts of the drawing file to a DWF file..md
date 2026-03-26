---
title: "Publishing all layouts of the drawing file to a DWF file."
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "Below code shows the procedure to publish all the layouts to single DWF file. This procedure uses PublishExecute API passing the layout information..."
author: Autodesk
---
# Publishing all layouts of the drawing file to a DWF file.

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/publishing-all-layouts-of-the-drawing-file-to-a-dwf-file.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to publish all the layouts to single DWF file. This procedure uses PublishExecute API passing the layout information through the DSD file.
[CommandMethod("PublishDWF")]
static public void PublishDWF()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      string dwgFileName =
        Application.GetSystemVariable("DWGNAME") as string;
    string dwgPath =
        Application.GetSystemVariable("DWGPREFIX") as string;
      string name =
        System.IO.Path.GetFileNameWithoutExtension(dwgFileName);
      //find a temp location.
    string strTemp = System.IO.Path.GetTempPath();
      PromptStringOptions options =
        new PromptStringOptions("Specific the DWF file name");
    options.DefaultValue = "c:\\temp\\" + name + ".dwf";
    PromptResult result = ed.GetString(options);
      if (result.Status != PromptStatus.OK)
        return;
      //get the layout ObjectId List
    System.Collections.ArrayList layoutList = null;
    try
    {
        layoutList = GetLayoutIdList(db);
    }
    catch
    {
        Application.ShowAlertDialog("Unable to get layouts name");
        return;
    }
      Publisher publisher = Application.Publisher;
      //put the plot in foreground
    short bgPlot =
        (short)Application.GetSystemVariable("BACKGROUNDPLOT");
    Application.SetSystemVariable("BACKGROUNDPLOT", 0);
      using (Transaction tr =
                db.TransactionManager.StartTransaction())
    {
        DsdEntryCollection collection =
                        new DsdEntryCollection();
          foreach (ObjectId layoutId in layoutList)
        {
            Layout layout =
                tr.GetObject(layoutId,
                        OpenMode.ForRead) as Layout;
              DsdEntry entry = new DsdEntry();
              entry.DwgName = dwgPath + dwgFileName;
            entry.Layout = layout.LayoutName;
            entry.Title = layout.LayoutName;
            entry.Nps = "AA";
              collection.Add(entry);
        }
          DsdData dsdData = new DsdData();
          dsdData.SheetType = SheetType.MultiDwf;
        dsdData.ProjectPath = "c:\\Temp";
        dsdData.DestinationName = result.StringResult;
            string dsdFile = strTemp + name + ".dsd";
          if (System.IO.File.Exists(dsdFile))
            System.IO.File.Delete(dsdFile);
          dsdData.SetDsdEntryCollection(collection);
          //Workaround to avoid promp for dwf file name
        //set PromptForDwfName=FALSE in
        //dsdData using StreamReader/StreamWriter
        dsdData.WriteDsd(dsdFile);
          StreamReader sr = new StreamReader(dsdFile);
        string str = sr.ReadToEnd();
        sr.Close();
          str =
            str.Replace("PromptForDwfName=TRUE",
                            "PromptForDwfName=FALSE");
        str =
            str.Replace("IncludeLayer=FALSE",
                                   "IncludeLayer=TRUE");
          StreamWriter sw = new StreamWriter(dsdFile);
        sw.Write(str);
        sw.Close();
          dsdData.ReadDsd(dsdFile);
          using (PlotConfig pc =
            PlotConfigManager.SetCurrentConfig("DWF6 ePlot.pc3"))
        {
            publisher.PublishExecute(dsdData, pc);
        }
          System.IO.File.Delete(dsdFile);
          tr.Commit();
    }
      //reset the background plot value
    Application.SetSystemVariable("BACKGROUNDPLOT", bgPlot);
}
  public static ArrayList GetLayoutIdList(Database db)
{
    ArrayList layoutList = new ArrayList();
      Autodesk.AutoCAD.DatabaseServices.TransactionManager tm =
        db.TransactionManager;
      using (Transaction myT = tm.StartTransaction())
    {
        DBDictionary dic =
            (DBDictionary)tm.GetObject(db.LayoutDictionaryId,
                                OpenMode.ForRead, false);
        DbDictionaryEnumerator index = dic.GetEnumerator();
          while (index.MoveNext())
            layoutList.Add(index.Current.Value);
          myT.Commit();
    }
      return layoutList;
}

## 评论

**内容**: Maxence DELANNOY said...
When you read and write the DSD file, you have to specify Encoding.Default because otherwise UTF-8 will be used and the non-ascii characters in file paths will be replaced by other characters.
You can also use File.ReadAllText and File.WriteAllText to simplify the code.
Reply
08/20/2012 at 03:53 AM

---
