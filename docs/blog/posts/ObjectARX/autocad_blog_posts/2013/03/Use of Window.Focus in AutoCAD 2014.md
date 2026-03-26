---
title: "Use of Window.Focus in AutoCAD 2014"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - DWG
  - Palette
description: "The new API in AutoCAD 2014 includes the Window.Focus method. This method is very useful if you were using palette to call a command that requires ..."
author: Autodesk
---
# Use of Window.Focus in AutoCAD 2014

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/use-of-windowfocus-in-autocad-2014.html

## 文章内容

By Balaji Ramamoorthy
The new API in AutoCAD 2014 includes the Window.Focus method. This method is very useful if you were using palette to call a command that requires AutoCAD to prompt for user input. In earlier versions of AutoCAD, the AutoCAD editor did not receive focus until the editor was clicked. This was a bit troublesome as it required an additional mouse click. The way to overcome it was to either call the "SetFocus" Win32 API through a dllimport or to use an internal undocumented method : "Internal.Utils.SetFocusToDwgView".
With AutoCAD 2014, the "Window.Focus" method can be used instead. As an example, if you had a button in the palette to insert a block named "Autodesk", then you can use the Window.Focus method from the button click callback method as :
using Autodesk.AutoCAD.ApplicationServices;
using AAA = Autodesk.AutoCAD.ApplicationServices;
  private void InsertBlockBtn_Click(object sender, EventArgs e)
{
    AAA.Document activeDoc
            = AAA.Application.DocumentManager.MdiActiveDocument;
      dynamic acadDocObj = activeDoc.GetAcadDocument();
    activeDoc.Window.Focus();
    acadDocObj.SendCommand(String.Format("-Insert\nAutodesk\n"));
      //            or
      //object acadDocObj = activeDoc.GetAcadDocument();
    //activeDoc.Window.Focus();
    //object[] OnedataArry = new object[1];
    //OnedataArry[0] = String.Format("-Insert\nAutodesk\n");
    //acadDocObj.GetType().InvokeMember(
    //  "SendCommand",
    //  System.Reflection.BindingFlags.InvokeMethod,
    //  null, acadDocObj, OnedataArry
    //);
}

## 评论

**内容**: joantopo said...
I have a paletteset in my addin and I have tried that command but is the same result as:
"Autodesk.AutoCAD.Internal.Utils.SetFocusToDwgView();"
I would like that pointer appears in command line and with both methods I can do this.
Reply
12/04/2013 at 07:47 AM

---
