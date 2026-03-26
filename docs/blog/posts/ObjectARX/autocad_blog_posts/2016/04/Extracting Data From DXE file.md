---
title: "Extracting Data From DXE file"
date: 2016-04-01
categories:
  - AutoCAD
tags:
  - API
  - Unicode
description: "If you have an existing DXE file on your disk, it is possible to extract data to .csv file, and also retrieve information about the drawing file an..."
author: Autodesk
---
# Extracting Data From DXE file

发布日期: 2016-04-01

原始链接: https://adndevblog.typepad.com/autocad/2016/04/extracting-data-from-dxe-file.html

## 文章内容

By Madhukar Moogala
If you have an existing DXE file on your disk, it is possible to extract data to .csv file, and also retrieve information about the drawing file and external files if any source drawing referring to it.
Additionally you can refer to this blog which talks about imitating EATTEXT programmatically which uses Dataextraction API.
    public void extractSettingsFromDXE()
        {
        // Add the AcDx.dll reference from the inc folder
             Document doc = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            StringBuilder fileContent = new StringBuilder();
            const string dxePath = @"C:\Mechanical_Multileaders.dxe";
            if (System.IO.File.Exists(dxePath))
            {
              /*Load DxE from disk*/
           IDxExtractionSettings extractionSettings = DxExtractionSettings.FromFile(dxePath);
                /*Retrieve Information about File Structure*/
           DxFileList files = extractionSettings.DrawingDataExtractor.Settings.DrawingList as DxFileList;
           IDxFileReference[] fileRefereces = files.Files;
           foreach (DxFileReference dwgFile in fileRefereces)
               {
               ed.WriteMessage("\nDrawingFile :{0}", dwgFile);
               }
             IDxFileReference[] xrefFiles = files.XrefFiles;
           foreach (DxFileReference xref in xrefFiles)
               {
               ed.WriteMessage("\nXref DrawingFile :{0}", xref);
              }
            /*Write data to CSV*/
           if (extractionSettings.DrawingDataExtractor.ExtractData(dxePath))
               {
               System.Data.DataTable dt = extractionSettings.DrawingDataExtractor.ExtractedData;
                 foreach (var col in dt.Columns)
                   {
                   fileContent.Append(col.ToString() + ",");
                   }
                 fileContent.Replace(",", System.Environment.NewLine, fileContent.Length - 1, 1);
                foreach (DataRow dr in dt.Rows)
                   {
                    foreach (var column in dr.ItemArray)
                       {
                       fileContent.Append("\"" + column.ToString() + "\",");
                       }
                     fileContent.Replace(",", System.Environment.NewLine, fileContent.Length - 1, 1);
                   }
               if(File.Exists(@"C:\MLeaders.csv"))
                   File.Delete(@"C:\MLeaders.csv");
               System.IO.File.WriteAllText(@"C:\MLeaders.csv", fileContent.ToString());
               }
              /*Some Other Information*/
           //IDxOutputSettings outPutSettings = extractionSettings.OutputSettings;
           //AdoOutput.OutputType outPutType =  outPutSettings.FileOutputType;
             //DxOuputFlags oFlags = outPutSettings.OuputFlags;
           //IDxReport report  =  extractionSettings.Report;
              }
        }
  Sample screen of excel sheet with data written to it

## 评论

**内容**: Erphan Wadood said...
Hello Madhukar Moogala,
Can we write .dxe file from .dwg file programmatically using .NET API without starting AutoCAD.
Thanks,
Reply
07/21/2020 at 03:48 AM

---
