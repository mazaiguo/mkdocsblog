---
title: "How to load GraphicsInterface.TextStyle from a TextStyleTableRecord in .Net"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Unicode
description: "Here is a question asked by one of the ADN developer:"
author: Autodesk
---
# How to load GraphicsInterface.TextStyle from a TextStyleTableRecord in .Net

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-load-graphicsinterfacetextstyle-from-a-textstyletablerecord-in-net.html

## 文章内容

By Philippe Leefsma
  Here is a question asked by one of the ADN developer:
How can I load a GraphicsInterface.TextStyle with the properties of TextStyleTableRecord, without manually copying every property individually?
Solution
There is a built-in function provided by the API that allows to copy all properties of a TextStyleTableRecord into a GraphicsInterface.TextStyle. This method isn’t exposed to the .Net API, but you can easily P/Invoke it. Below are two examples that illustrate the two flavors of “fromAcDbTextStyle”: one takes a TextStyleTableRecord name as entry and the other a TextStyleTableRecord Id.
The command methods show how to retrieve the height and width of the input text, but in that case I just wanted to illustrate how to use “fromAcDbTextStyle” method.
  [DllImport("acdb18.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint =
    "?fromAcDbTextStyle@@YA?AW4ErrorStatus@Acad@@AAVAcGiTextStyle@@PB_W@Z")]
private static extern ErrorStatus fromAcDbTextStyle(
    System.IntPtr style, string styleName);
  [CommandMethod("getTextStrWidth")]
public void getTextStrWidth()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptResult pr = ed.GetString("\nEnter a string: ");
      if (pr.Status != PromptStatus.OK) return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        TextStyleTable TxtStlTbl = Tx.GetObject(
            db.TextStyleTableId,
            OpenMode.ForRead)
                as TextStyleTable;
          string styleName = "STANDARD";
          if (!TxtStlTbl.Has(styleName))
        {
            ed.WriteMessage("\nStyle "
                + styleName + " doesn't exist :(");
              return;
        }
          Autodesk.AutoCAD.GraphicsInterface.TextStyle iStyle =
            new Autodesk.AutoCAD.GraphicsInterface.TextStyle();
          if (fromAcDbTextStyle(iStyle.UnmanagedObject, styleName)
            == ErrorStatus.OK)
        {
            Extents2d ex = iStyle.ExtentsBox(
                pr.StringResult, true, true, null);
              double width = ex.MaxPoint.X - ex.MinPoint.X;
            double height = ex.MaxPoint.Y - ex.MinPoint.Y;
              ed.WriteMessage(
                "\n-Width = " +
                width.ToString() +
                "\n-Height = " +
                height.ToString());
        }
    }
}
  [DllImport("acdb18.dll",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?fromAcDbTextStyle@@YA?AW4ErrorStatus@Acad@@AAVAcGiTextStyle@@ABVAcDbObjectId@@@Z")]
private static extern ErrorStatus fromAcDbTextStyle(
    System.IntPtr style, ref ObjectId id);
  [CommandMethod("getTextStrWidthId")]
public void getTextStrWidthId()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptResult pr = ed.GetString("\nEnter a string: ");
      if (pr.Status != PromptStatus.OK) return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        TextStyleTable TxtStlTbl = Tx.GetObject(
            db.TextStyleTableId,
            OpenMode.ForRead)
                as TextStyleTable;
          string styleName = "STANDARD";
          if (!TxtStlTbl.Has(styleName))
        {
            ed.WriteMessage("\nStyle " +
                styleName + " doesn't exist :(");
              return;
        }
          Autodesk.AutoCAD.GraphicsInterface.TextStyle iStyle =
            new Autodesk.AutoCAD.GraphicsInterface.TextStyle();
          ObjectId styleId = TxtStlTbl[styleName];
          if (fromAcDbTextStyle(iStyle.UnmanagedObject, ref styleId)
            == ErrorStatus.OK)
        {
            Extents2d ex = iStyle.ExtentsBox(
                pr.StringResult, true, true, null);
              double width = ex.MaxPoint.X - ex.MinPoint.X;
            double height = ex.MaxPoint.Y - ex.MinPoint.Y;
              ed.WriteMessage(
                "\n-Width = " +
                width.ToString() +
                "\n-Height = " +
                height.ToString());
        }
    }
}

## 评论

**内容**: Mehmet said...
gives DLL error at Autocad 2019
Reply
02/25/2020 at 05:46 AM

---
