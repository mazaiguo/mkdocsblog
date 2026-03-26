---
title: "How to reload the line type in AutoCAD using AutoCAD.NET API"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "Below AutoCAD.NET command shows the procedure to reload the line type in AutoCAD using .NET API. The command runs in “Session” mode so that “SendCo..."
author: Autodesk
---
# How to reload the line type in AutoCAD using AutoCAD.NET API

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/how-to-reload-the-line-type-in-autocad-using-autocadnet-api.html

## 文章内容

By Virupaksha Aithal
Below AutoCAD.NET command shows the procedure to reload the line type in AutoCAD using .NET API. The command runs in “Session” mode so that “SendCommand” can work synchronously. Also, code uses AutoCAD ActiveX API using late binding technique to avoid adding reference to AutoCAD ActiveX interops.
[CommandMethod("relaodLinetype", CommandFlags.Session)]
public void relaodLinetype()
{
    DocumentCollection docManager =
            Application.DocumentManager;
    Database db =
        docManager.MdiActiveDocument.Database;
    Transaction trans =
        db.TransactionManager.StartTransaction();
    bool bReload = false;
      using (trans)
    {
        LinetypeTable table =
            trans.GetObject(
            db.LinetypeTableId,
            OpenMode.ForRead) as LinetypeTable;
          if (table.Has("CENTER"))
            bReload = true;
    }
      System.Int16 fileDia = (System.Int16)
        Application.GetSystemVariable("FILEDIA");
    Application.SetSystemVariable("FILEDIA", 0);
      //reload using linetype command...
    Object acadObject = Application.AcadApplication;
    object ActiveDocument =
        acadObject.GetType().InvokeMember(
            "ActiveDocument",
            System.Reflection.BindingFlags.GetProperty,
            null,
            acadObject,
            null);
      object[] dataArry = new object[1];
      if (bReload)
    {
        dataArry[0] =
            "-linetype Load CENTER\nacad.lin\nYes\n ";
    }
    else
    {
        dataArry[0] =
            "-linetype Load CENTER\nacad.lin\n ";
    }
      ActiveDocument.GetType().InvokeMember(
                "SendCommand",
                System.Reflection.BindingFlags.InvokeMethod,
                null,
                ActiveDocument,
                dataArry);
      Application.SetSystemVariable("FILEDIA", fileDia);
}

## 评论

**内容**: FFlix said...
hi virupaksha, thanks for sharing this example to which my question relates: how does the document manage the linetype table records and its .lin file, i.e. how are differences handled if say a linetype is created in the .lin file and a linetype of the same name exists in the linetype table? does a linetype persist in the database if a linetype table record is created but the .lin file is not accessed? thanks
Reply
05/28/2012 at 12:33 PM

---
**内容**: Virupaksha Aithal said...
Hi
Line type file used only to create line type. AutoCAD does not maintain any link between line type file and the line type created. If user loads a line type name which is already present in drawing, the line type in drawing is updated to reflect the line type in the newly loaded file
Thanks
Viru
Reply
05/29/2012 at 04:56 AM

---
