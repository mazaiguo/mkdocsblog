---
title: "Identify Mechanical Desktop file(MDT) using .NET"
date: 2018-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - DWG
  - Database
description: "Recently, we had a customer query regarding distinguishing an AutoCAD Mechanical desktop file among a set of drawing files."
author: Autodesk
---
# Identify Mechanical Desktop file(MDT) using .NET

发布日期: 2018-07-01

原始链接: https://adndevblog.typepad.com/autocad/2018/07/identify-mechanical-desktop-filemdt-using-net.html

## 文章内容

By Deepak Nadig
Recently, we had a customer query regarding distinguishing an AutoCAD Mechanical desktop file among a set of drawing files.
Answer:
Mechanical desktop should have entry named AmdtFileType with a value of 84 in the Custom tab of DWGPROPS(image)
One of the ways to distinguish a Autodesk Mechanical desktop file could be to retrieve and check for the custom property as below.
Note : File to be checked is read as a side database in the code below. 
[CommandMethod("testMdtFile")]
public static void testMdtFile()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    try
    {
        using (Database db = new Database(false, true))
        {
            db.ReadDwgFile(@"c:\temp\testMDT.dwg", FileOpenMode.OpenForReadAndAllShare, false, null);
            db.CloseInput(true);
            string val = GetCustomProperty(db, "AmdtFileType");
            System.Windows.Forms.MessageBox.Show("Value of AmdtFileType is " + val);
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString());
    }
}
public static string GetCustomProperty(Database db, string key)
{
    DatabaseSummaryInfoBuilder sumInfo = new DatabaseSummaryInfoBuilder(db.SummaryInfo);
    IDictionary custProps = sumInfo.CustomPropertyTable;
    return (string)custProps[key];
}

