---
title: "How to obtain a list of all Pipe Specs and Sizes in Plant3d using .NET C#"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - .NET
  - C#
  - Plant 3D
description: "If you are looking for an easy way to list all Pipe Specs available in Plant3d, then you may run into problem. That is, of course, until you find o..."
author: Autodesk
---
# How to obtain a list of all Pipe Specs and Sizes in Plant3d using .NET C#

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-obtain-a-list-of-all-pipe-specs-and-sizes-in-plant3d-using-net-c.html

## 文章内容

by Fenton Webb
If you are looking for an easy way to list all Pipe Specs available in Plant3d, then you may run into problem. That is, of course, until you find out that there is a special reference DLL that is not included in the posted SDK which contains everything you need…
That reference DLL is called PnP3dMain.dll.
Once you add this reference included in your Visual Studio project (from the Program Files folder of your Plant3d with Copy Local=False) you will gain access to:
Autodesk.ProcessPower.P3dUI.UISettings
and everything becomes much easier to achieve, as you can see by the code below…
// get all pipe spec names by Fenton Webb, DevTech, Autodesk 23/05/2012
[CommandMethod("GetPipeSpecs")]
public void GetPipeSpecs()
{
  // get the AutoCAD Editor object so we can print to the command line
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
  // get the UISettings object (found in Pnp3dMain.dll)
  Autodesk.ProcessPower.P3dUI.UISettings settings =
                new Autodesk.ProcessPower.P3dUI.UISettings();
  StringCollection specs = settings.AllSpecs();
  foreach (string spec in specs)
  {
    ed.WriteMessage("\nSpec " + spec);
  }
}
  // get sizes available from a spec
// by Fenton Webb, DevTech, Autodesk 23/05/2012
[CommandMethod("GetPipeSizes")]
public void GetPipeSizes()
{
  // get the AutoCAD Editor object so we can print to the command line
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
  PromptResult res = ed.GetString("\nEnter Pipe Spec");
  if (res.Status == PromptStatus.OK)
  {
    // get the UISettings object (found in Pnp3dMain.dll)
    Autodesk.ProcessPower.P3dUI.UISettings settings =
                new Autodesk.ProcessPower.P3dUI.UISettings();
    // now get all the sizes that are available for that spec
    StringCollection sizes = settings.GetAllSizesFromSpecName(res.StringResult);
    foreach (string size in sizes)
    {
      ed.WriteMessage("\nSize " + size);
    }
  }
}

## 评论

**内容**: Reza said...
Dear Fenton Webb,
I want to create equipment in plant 3d from predefined shape.
I want to implement it in C# program.
Best Regards
Reply
02/23/2016 at 12:06 AM

---
