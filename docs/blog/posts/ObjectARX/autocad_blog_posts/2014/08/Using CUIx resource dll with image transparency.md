---
title: "Using CUIx resource dll with image transparency"
date: 2014-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
description: "This post and associated code samples is a courtesy from one of our ADN member: Michael Csikos. Thanks Michael!"
author: Autodesk
---
# Using CUIx resource dll with image transparency

发布日期: 2014-08-01

原始链接: https://adndevblog.typepad.com/autocad/2014/08/using-cuix-resource-dll-with-image-transparency.html

## 文章内容

By Philippe Leefsma
This post and associated code samples is a courtesy from one of our ADN member: Michael Csikos. Thanks Michael!
This illustrates how to use .ico files in a resource-only dll for your cuix files. By default the cuix file accepts resource dlls with .bmp files, however .bmp do not support transparency, which can make your button icons look much nicer in AutoCAD UI.
Unfortunately this approach isn’t documented anywhere in the AutoCAD programming help, so Michael was digging out this workaround: by manually editing the resource file (.rc) of your resource-only dll project, you can have the cuix support .ico files. Once you added a new ico resource through the Visual Studio editor, modify the “ICO” property of the resource to “RCDATA” as illustrated in the sample below:
//////////////////////////////////////////////////////////////////
// Icon with lowest ID value placed first to ensure application
// icon remains consistent on all systems.
IDI_TRIANGLE16     RCDATA           ".\\resources\\icon1.ico"
IDI_TRIANGLE32     RCDATA           ".\\resources\\icon2.ico"
#endif    // English (Australia) resources
//////////////////////////////////////////////////////////////////
You can then compile your dll and place it in the same folder than the cuix file using the resource. The same approach doesn’t work for .png unfortunately.
On top of that Michael also provided a C# sample that illustrates how to programmatically generate a cuix file using those resources. Generating the cuix file from the code is a very efficient approach, as it allows to quickly and easily modify and re-generate the cuix files as needed.
The sample creates extension methods (see CustomizationExtensions.cs) which makes it a lot easier to add new tabs, panels, rows and buttons.
An extract of his code looks like below:
var debugFolder          =
    Path.GetDirectoryName(
        Assembly.GetExecutingAssembly().Location);
-
var cs                   = new CustomizationSection();
var menuGroup            = cs.MenuGroup;
var tab                  = cs.AddNewTab("CuiTestTab");
var panel                = tab.AddNewPanel("Panel");
var row                  = panel.AddNewRibbonRow();
  menuGroup.Name           = "CuiTest";
  row.AddNewButton(
    "BMP",
    "BMP",
    "SayBMP",
    "BMP loaded from the resource DLL",
    "IDB_CIRCLE16",
    "IDB_CIRCLE32",
    RibbonButtonStyle.LargeWithText);
  row.AddNewButton(
    "ICO",
    "ICO",
    "SayICO",
    "ICO loaded from the resource DLL",
    "IDI_TRIANGLE16",
    "IDI_TRIANGLE32",
    RibbonButtonStyle.LargeWithText);
  var fileName = Path.Combine(debugFolder, "CuiTest.cuix");
  File.Delete(fileName);
  cs.SaveAs(fileName);
-
-
And here is a picture of the stunning result!
  See attachment for the whole project:
cui resonly ico.zip

## 评论

**内容**: Steve Hill said...
This is great! Thanks for sharing!
Reply
08/06/2014 at 11:27 AM

---
**内容**: Christian said...
This is to much for me. Can someone explain it easier?
Reply
11/21/2016 at 12:08 PM

---
**内容**: Akash Jain said...
I implemented this project but how to build it in OEM and verify if it is working, beacuse icons are still not displayed on the button when i run this attached project.
Reply
07/27/2017 at 01:50 AM

---
