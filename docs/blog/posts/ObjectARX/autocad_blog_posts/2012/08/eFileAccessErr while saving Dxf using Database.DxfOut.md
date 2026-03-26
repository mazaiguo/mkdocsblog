---
title: "eFileAccessErr while saving Dxf using Database.DxfOut"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DXF
  - Database
description: "Attempting to save a DXF file opened in AutoCAD using the Database.DxfOut method throws the "eFileAccessErr". This is a known behavior and the work..."
author: Autodesk
---
# eFileAccessErr while saving Dxf using Database.DxfOut

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/efileaccesserr-while-saving-dxf-using-databasedxfout.html

## 文章内容

By Balaji Ramamoorthy
Attempting to save a DXF file opened in AutoCAD using the Database.DxfOut method throws the "eFileAccessErr". This is a known behavior and the workaround for it is to use the "SendCommand" method to send the "dxfout" command to the AutoCAD command line.
Here is a sample code to save all the documents opened in AutoCAD as Dxf and close them.
There is a change in the way the AcadDocument is retrieved in 2013 SDK and also in the way the "SendCommand" can be invoked as compared the earlier versions. So, I have provided two versions of the code snippet.
// Prior to 2013
[CommandMethod("SaveAndCloseAll", CommandFlags.Session)]
public static void SaveAndCloseAll()
{
    object filediaVariable = Application.GetSystemVariable("FILEDIA");
    Application.SetSystemVariable("FILEDIA", 0);
      DocumentCollection acDocMgr = Application.DocumentManager;
    foreach (Document doc in acDocMgr)
    {
        AcadDocument acadDoc = doc.AcadDocument as AcadDocument;
          using (DocumentLock doclock = doc.LockDocument())
        {
            object[] dataArry = new object[1];
            dataArry[0] = "dxfout\n\nV\n2010\n\ny\n";
            acadDoc.GetType().InvokeMember
                (
                    "SendCommand",
                    System.Reflection.BindingFlags.InvokeMethod,
                    null,
                    acadDoc,
                    dataArry
                );
        }
    }
    Application.SetSystemVariable("FILEDIA", filediaVariable);
      // Close all the documents
    acDocMgr.CloseAll();
}
  // 2013 onwards
[CommandMethod("SaveAndCloseAll", CommandFlags.Session)]
public static void SaveAndCloseAll()
{
    object filediaVariable = Application.GetSystemVariable("FILEDIA");
    Application.SetSystemVariable("FILEDIA", 0);
      DocumentCollection acDocMgr = Application.DocumentManager;
    foreach (Document doc in acDocMgr)
    {
        dynamic acadDoc = doc.GetAcadDocument();
        using (DocumentLock doclock = doc.LockDocument())
        {
            object[] dataArry = new object[1];
            dataArry[0] = "dxfout\n\nV\n2010\n\ny\n";
            acadDoc.SendCommand("dxfout\n\nV\nR12\n\ny\n");
        }
    }
    Application.SetSystemVariable("FILEDIA", filediaVariable);
      // Close all the documents
    acDocMgr.CloseAll();
}

