---
title: "Unload partial CUIx when AutoCAD quits"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
description: "AutoCAD 2011 introduced new API functions to load/unload partial CUIx files. This is what I'm trying to use as well - see below code. It loads the ..."
author: Autodesk
---
# Unload partial CUIx when AutoCAD quits

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/unload-partial-cuix-when-autocad-quits.html

## 文章内容

By Adam Nagy
AutoCAD 2011 introduced new API functions to load/unload partial CUIx files. This is what I'm trying to use as well - see below code. It loads the CUIx fine, but the unloading does not seem to work as my CUIx is still loaded the next time I start up AutoCAD.
using System;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.Customization;
  namespace CuixUnloaderDll
{
  public class MyAddIn : IExtensionApplication
  {
    private string menuPath = @"C:\Temp\CuixUnloaderDll\MyCui.cuix";

    public void Initialize()
    {
      acApp.LoadPartialMenu(menuPath);
    }
      public void Terminate()
    {
      acApp.UnloadPartialMenu(menuPath);
    }
  }
}
Solution
If you check the return value of UnloadPartialMenu() then you'll see it's false, which means that the function did not succeed.
It is probably called too late and by that time the UI is unloaded.
Instead of using UnloadPartialMenu() you could use the CUI API to modify the acad.cuix file. This seemed to work fine:
using System;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.Customization;
  namespace CuixUnloaderDll
{
  public class MyAddIn : IExtensionApplication
  {
    private string menuPath = @"C:\Temp\CuixUnloaderDll\MyCui.cuix";
    private string menuGroupName = "MYCUI";
      public void Initialize()
    {
      bool ret = acApp.LoadPartialMenu(menuPath);
    }
      public void Terminate()
    {
      string mainCuiFile = string.Format("{0}.cuix",
        (string)acApp.GetSystemVariable("MENUNAME"));
      CustomizationSection cs =
        new CustomizationSection(mainCuiFile);
      cs.RemovePartialMenu(menuPath, menuGroupName);
      if (cs.IsModified == true)
      {
        cs.Save();
      }
    }
  }
}
Since AutoCAD 2012 you could also use the AutoLoader mechanism to take care of loading/unloading your user interface customisation files (*.cuix)

