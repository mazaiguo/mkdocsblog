---
title: "Set or Get Lisp Symbol in .NET"
date: 2014-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
  - Database
description: "We are pretty much aware of pinvoke acedGetSym\acedPutSym in .NET to manipulate lisp symbols , we can avoid pinvoking with help of  SetLispSymbol a..."
author: Autodesk
---
# Set or Get Lisp Symbol in .NET

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/set-or-get-lisp-symbol-in-net.html

## 文章内容

By Madhukar Moogala
We are pretty much aware of pinvoke acedGetSym\acedPutSym in .NET to manipulate lisp symbols , we can avoid pinvoking with help of  SetLispSymbol and GetLispSymbol.
In the following example ,my attention is towards "how to store \retireve multiple fragements of information in lisp symbol " ,to achieve this we can use TypedValue object data type along with LispDataType enumerations as values.
  public static void PutSymbol()
{
  Document d = Application.DocumentManager.MdiActiveDocument;
Database db = d.Database;
// Create a list
TypedValue[] tValue = new TypedValue[7];
tValue.SetValue(new TypedValue((int)LispDataType.ListBegin), 0);
tValue.SetValue(new TypedValue((int)LispDataType.Text,
                                "Main List Item 1"), 1);
tValue.SetValue(new TypedValue((int)LispDataType.ListBegin), 2);
tValue.SetValue(new TypedValue((int)LispDataType.Text,
                                "Nested List Item 1"), 3);
tValue.SetValue(new TypedValue((int)LispDataType.Text,
                                "Nested List Item 2"), 4);
tValue.SetValue(new TypedValue((int)LispDataType.ListEnd), 5);
tValue.SetValue(new TypedValue((int)LispDataType.ListEnd), 6);
  d.SetLispSymbol("lst", tValue);
}
  public static void GetSymbol()
{
Document d = Application.DocumentManager.MdiActiveDocument;
Editor ed = d.Editor;
PromptResult res = ed.GetString("\nName of lisp-Symbol name: ");
if (res.Status == PromptStatus.OK)
{
    TypedValue[] tValue = (TypedValue[])d.GetLispSymbol(res.StringResult);
    if (tValue == null) return;
    foreach (TypedValue tV in tValue)
    {
        ed.WriteMessage("\n");
        ed.WriteMessage(tV.TypeCode + "," + tV.Value);
    }
  }
  }

## 评论

**内容**: sam1 said...
Hi Madhukar Moogala, I copied GetSymbol and built the solution but it's not working (Windows 7 and AutoCAD 2016):
System.InvalidCastException: Unable to cast object of type 'System.String' to type 'Autodesk.AutoCAD.DatabaseServices.TypedValue[]'.
the error occurs at this line:
TypedValue[] tValue = (TypedValue[])d.GetLispSymbol(res.StringResult);
(I was typing the name of a string var. A real number symbol leads to the same kind of error at the same line: System.InvalidCastException: Unable to cast object of type 'System.Double' to type 'Autodesk.AutoCAD.DatabaseServices.TypedValue[]'.)
What am I missing?
Reply
12/03/2015 at 06:21 AM

---
