---
title: "Restricting selection to strictly single only"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
  - Selection
description: "Setting “PromptSelectionOptions.SingleOnly” as true, will still permit the use of the window selection while selecting the entity."
author: Autodesk
---
# Restricting selection to strictly single only

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/restricting-selection-to-strictly-single-only.html

## 文章内容

By Balaji Ramamoorthy
Setting “PromptSelectionOptions.SingleOnly” as true, will still permit the use of the window selection while selecting the entity.
As mentioned in the Managed API documentation, setting "PromptSelectionOptions.SingleOnly" to true is only equivalent of providing “:S” to the acedSSGet method. So it does not prevent the use of Window selection while selecting entities.
To prevent the window and crossing polygon selection options, you will need to use the acedSSGet in your .Net plugin by using the P/Invoke and provide "-W-F-A-C-CP:S" to remove the window and fence options.
The keywords "-W-F-A-C-CP:S" stands for "Window", "Fence", "All", "Crossing", "Crossing Polygon" and "Single". For the code snippet to work on other language versions of AutoCAD, the equivalent of these need to be used.
Here is the sample code :
struct ads_name
{
    IntPtr a;
    IntPtr b;
};
  // Replace "accore.dll" by "acad.exe" for AutoCAD versions prior to 2013
[DllImport
    (
        "accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true
    )
]
private static extern PromptStatus acedSSGet
    (
        string str,
        IntPtr pt1,
        IntPtr pt2,
        IntPtr filter,
        out ads_name ss
    );
  // Replace "accore.dll" by "acad.exe" for AutoCAD versions prior to 2013
[DllImport
    (
        "accore.dll",
        CallingConvention = CallingConvention.Cdecl,
        CharSet = CharSet.Unicode,
        ExactSpelling = true
    )
]
private static extern PromptStatus acedSSLength
    (
        ref ads_name ss,
        out int len
    );
  [CommandMethod("TestSS")]
public void commandMethodTest()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      ads_name sset;
    string str = "-W-F-A-C-CP:S";
      PromptStatus ps = acedSSGet (
                                    str,
                                    IntPtr.Zero,
                                    IntPtr.Zero,
                                    IntPtr.Zero,
                                    out sset
                                );
    if (ps == PromptStatus.OK)
    {
        int selections = 0;
        if (acedSSLength(ref sset, out selections) == PromptStatus.OK)
        {
            ed.WriteMessage(string.Format("{0} selected", selections));
        }
    }
}

