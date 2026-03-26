---
title: "How to pass COM optional parameter in C#"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - COM
description: "Here is a problem you may encounter when invoking the AutoCAD ActiveX API from C#:"
author: Autodesk
---
# How to pass COM optional parameter in C#

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-pass-com-optional-parameter-in-c.html

## 文章内容

By Philippe Leefsma
Here is a problem you may encounter when invoking the AutoCAD ActiveX API from C#:
I'm trying to use AcadSelectionSet.SelectOnScreen in C# with similar approaches I've been using in VB. But I can't omit the optional parameters in C# which I can in VB.
I tried to create some empty arrays and pass them to SelectOnScreen but I get invalid argument errors.
Could you offer a solution?
Solution
Note: this workaround only applies to .Net 3.5 and prior versions of the framework, as C# 4.0 provides missing parameters functionality. 
In VB, you can ignore the optional parameters when you call AcadSelectionSet.SelectOnScreen but you can't do that in C#. This is because C# doesn't support optional parameters. Also, if you really want to pass NULL values as an indication that you don't want any values in the object array (no variant in C#), you can't create arrays with values, the zeros will be trades as values in the DXF code not 'nothing'. That's where the problem is.
Fortunately, there is a solution in .NET which is using object reflection to specific a missing value that is NULL.
   object o = System.Reflection.Missing.Value;
This will be the equivalent of NULL values passed into VB functions call. The following code snippet demonstrates how it works.
  //
// error checking code omitted for code brevity
//
private void TestMissing(AcadApplication oAcad)
{
    AcadDocument oDoc = oAcad.ActiveDocument;
    AcadSelectionSet ss = oDoc.SelectionSets.Add("ss01");
    object oMissing01 = System.Reflection.Missing.Value;
    object oMissing02 = System.Reflection.Missing.Value;
    ss.SelectOnScreen(oMissing01, oMissing02);
    System.Windows.Forms.MessageBox.Show(
        "Number of objects in the selection: " + ss.Count + ".");
    ss.Delete();
}

