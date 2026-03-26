---
title: "Get the group name of the main customization file (CUI/CUIx)"
date: 2012-07-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
  - COM Interop
  - CUI
description: "I would like to get the main customization file's group name so that I could unload it using the CUIUNLOAD command."
author: Autodesk
---
# Get the group name of the main customization file (CUI/CUIx)

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/get-the-group-name-of-the-main-customization-file-cuicuix.html

## 文章内容

By Adam Nagy
I would like to get the main customization file's group name so that I could unload it using the CUIUNLOAD command.
Solution
You could get it either using the ActiveX API:
using System;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.Interop;
using Autodesk.AutoCAD.Interop.Common;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Customization;
  [assembly: CommandClass(typeof(MyAddIn.Commands))]
  namespace MyAddIn
{
  public class Commands
  {
    // Needs reference to:
    // - Autodesk.AutoCAD.Interop.dll
    // - Autodesk.AutoCAD.Interop.Common.dll
    [CommandMethod("UseActiveX")]
    public static void MyCmdActiveX()
    {
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
      AcadApplication acadApp =
        (AcadApplication)acApp.AcadApplication;
      foreach (AcadMenuGroup group in acadApp.MenuGroups)
      {
        if (group.Type == AcMenuGroupType.acBaseMenuGroup)
          ed.WriteMessage(
            "The main menu group name is " + group.Name);
      }
    }
  }
}
... or using the CUI API (this is quite a bit slower):
// Needs a reference to:
// - AcCui.dll (Copy Local = False)
[CommandMethod("UseCuiApi")]
public static void UseCuiApi()
{
  Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
  string menuname = (string)acApp.GetSystemVariable("MENUNAME");
  // 2009 and before uses *.cui, 2010 and beyond uses *.cuix
  menuname += ".cuix";
  CustomizationSection cs = new CustomizationSection(menuname);
  ed.WriteMessage("The main menu group name is " + cs.MenuGroupName);
}
Since AutoCAD 2011 you could also use the Application.UnloadPartialMenu() to unload the customization file. This requires the file name and not the group name, so when using this the above 2 solutions would not be needed.
// Needs reference to the 2011+ version of
// AcMgd.dll (Copy Local = false)
[CommandMethod("UnloadMainCui")]
public static void UnloadMainCui()
{
  Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
  string menuname = (string)acApp.GetSystemVariable("MENUNAME");
  acApp.UnloadPartialMenu(menuname);
}

