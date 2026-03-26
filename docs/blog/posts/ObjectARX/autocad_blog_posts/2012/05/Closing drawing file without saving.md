---
title: "Closing drawing file without saving"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM
  - COM Interop
description: "To close a drawing without saving it, you can use ether API  “CloseAndDiscard” as shown in below code or you can use the ActiveX interface in AutoC..."
author: Autodesk
---
# Closing drawing file without saving

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/closing-drawing-file-without-saving.html

## 文章内容

By Virupaksha Aithal
To close a drawing without saving it, you can use ether API  “CloseAndDiscard” as shown in below code or you can use the ActiveX interface in AutoCAD (refer Method 2).
The AcadDocument object has the Close method from where you can specify a flag if you want to save the changes.The following is a sample that demonstrates how to call the AcadDocument.Close method from .NET. The sample code uses late binding technique to avoid referencing the AutoCAD ActiveX interops.
//Method1
[CommandMethod("closeDoc_Method1", CommandFlags.Session)]
public static void closeDoc_Method1()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    doc.CloseAndDiscard();
}
  //Method2 - using ActiveX API
[CommandMethod("closeDoc_Method2", CommandFlags.Session)]
public static void closeDoc_Method2()
{
    Object acadObject = Application.AcadApplication;
    object ActiveDocument = acadObject.GetType().InvokeMember(
                                        "ActiveDocument",
                                 BindingFlags.GetProperty,
                                   null, acadObject, null);
      object[] dataArry = new object[2];
    dataArry[0] = false; //no save
    dataArry[1] = ""; //drawing file name.. if saving
    ActiveDocument.GetType().InvokeMember("close",
                                    BindingFlags.InvokeMethod,
                               null, ActiveDocument, dataArry);
}

## 评论

**内容**: Matus said...
is there a reason, not to use this?
Dim doc as Document=Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument
doc.CloseAndDiscard()
Reply
05/22/2012 at 09:12 AM

---
**内容**: Virupaksha Aithal said in reply to Matus...
Thanks. Yes we can use the API “CloseAndDiscard”. I will add this method too to the post.
Thanks again.
Viru
Reply
05/22/2012 at 09:31 PM

---
**内容**: Андрей Бушман said...
How I can close a drawing which was opened by the user right now, if I forbid his opening? If I try to close in an event handler, then I receive Fatal Error.
Reply
03/11/2013 at 07:52 AM

---
