---
title: "Publish Layouts to PDF using COM"
date: 2015-11-01
categories:
  - AutoCAD COM
tags:
  - API
  - COM
  - PDF
description: "We don’t have a direct API to publish multiple layouts in to single PDF document, we may have to rely some hard code work"
author: Autodesk
---
# Publish Layouts to PDF using COM

发布日期: 2015-11-01

原始链接: https://adndevblog.typepad.com/autocad/2015/11/publish-layouts-to-pdf-using-com.html

## 文章内容

By Madhukar Moogala
We don’t have a direct API to publish multiple layouts in to single PDF document, we may have to rely some hard code work
In this blog I will show how to create a simple DSD, and use this DSD file to execute publish command.
  
  class DSDObject
  {

   public DSDObject()
   {

   }
   
   public string DWG { get; set; }
   public string Layout { get; set; }
   public string Setup { get; set; }
   public string dwgName { get; set; }
   public String createDSDEntry()
   {
   
    StringBuilder sb = new StringBuilder();
    sb.Append("[DWF6Sheet:" + this.dwgName + "-" + Layout + "]");
    sb.AppendLine();
    sb.Append("DWG=" + DWG);
    sb.AppendLine();
    sb.Append("Layout=" + Layout);
    sb.AppendLine();
    sb.Append("Setup=");
    return sb.ToString();
   }

  }

  public static void TP()
  {
   Autodesk.AutoCAD.Interop.AcadApplication acadCOMApp;
   acadCOMApp = (Autodesk.AutoCAD.Interop.AcadApplication)Application.AcadApplication;
   AcadDocument acadDoc = acadCOMApp.ActiveDocument;
   string drawingName = acadDoc.Name;
   string drawingPath = acadDoc.FullName;
   List entries = new List();


   foreach(AcadLayout alayout in acadDoc.Layouts)
   {
    DSDObject dsdObj = new DSDObject();
      
     dsdObj.DWG = drawingPath;
     dsdObj.dwgName = drawingName;
     dsdObj.Layout = alayout.Name;
     dsdObj.Setup = "";

     entries.Add(dsdObj.createDSDEntry());
   }
  
   StreamWriter writer = new StreamWriter("c:\\trash\\testDSD.dsd");
   writer.WriteLine("[DWF6Version]");
   writer.WriteLine("Ver=1");
   foreach(string entry in entries)
   {
      writer.WriteLine(entry);
   }

   writer.WriteLine("[Target]");
   writer.WriteLine("Type=6");

   writer.WriteLine("DWF=C:\\Users\\moogalm\\Desktop\\Kitchens.pdf");
   writer.WriteLine("OUT=C:\\Users\\moogalm\\Desktop\\");
   writer.WriteLine("PWD=");
   writer.Close();
   FileInfo fi = new FileInfo("C:\\Trash\\testDSD.dsd");
   if (fi.Length > 0)
   {
    acadDoc.SetVariable("FILEDIA", 0);
    acadDoc.SendCommand("-PUBLISH " + fi.FullName +"\n");
   }
    
   
   
  }

