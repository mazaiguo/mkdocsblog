---
title: "Opening a Project programmatically in Plant3d using .NET"
date: 2012-09-01
categories:
  - Plant 3D
tags:
  - .NET
  - Plant 3D
description: "Currently, for Plant3d 2012 and 2013 it’s not possible to use the PlantProject.LoadProject() function. The problem is that the Project Manager does..."
author: Autodesk
---
# Opening a Project programmatically in Plant3d using .NET

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/opening-a-project-programmatically-in-plant3d-using-net.html

## 文章内容

by Fenton Webb
Currently, for Plant3d 2012 and 2013 it’s not possible to use the PlantProject.LoadProject() function. The problem is that the Project Manager does not update.
The solution is to use the command line “-OPENPROJECT”, here’s how:
// open Plant3d project.xml by Fenton Webb, DevTech, 17/9/12
[CommandMethod("OpenMyProject")]
public void OpenMyProject()
{
 // select project.xml
 System.Windows.Forms.OpenFileDialog dlg = new System.Windows.Forms.OpenFileDialog();
 DirectoryInfo defaultPathDI = new DirectoryInfo(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments));
   dlg.InitialDirectory = defaultPathDI.FullName;
 dlg.FileName = "project.xml";
 dlg.Multiselect = false;
   System.Windows.Forms.DialogResult dlgResult = dlg.ShowDialog();
 // if ok
 if (dlgResult == System.Windows.Forms.DialogResult.OK)
{
  AcadApp.DocumentManager.MdiActiveDocument.SendStringToExecute("-_.OPENPROJECT \"" + dlg.FileName + "\"\n", true, false, true);       
}
}
If the LoadProject() was working you would use it like this…
[CommandMethod("loadMyProject")]
public void loadProject()
{
 // select project.xml
 System.Windows.Forms.OpenFileDialog dlg = new System.Windows.Forms.OpenFileDialog();
 DirectoryInfo defaultPathDI = new DirectoryInfo(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments));
   dlg.InitialDirectory = defaultPathDI.FullName;
 dlg.FileName = "project.xml";
 dlg.Multiselect = false;
   System.Windows.Forms.DialogResult dlgResult = dlg.ShowDialog();
 // if ok
 if (dlgResult == System.Windows.Forms.DialogResult.OK)
{
  PlantProject pp = PlantProject.LoadProject(dlg.FileName, true, "", "");
  PlantApplication.SetCurrentProject(pp, true);
}
}

## 评论

**内容**: _davewolfe said...
This doesn't seem to work in Plant 3d 2015.
Reply
01/14/2015 at 11:12 AM

---
**内容**: Augusto Goncalves said in reply to _davewolfe...
Dave,
To use this on 2015 you'll need the Extension 1 available on subscription. Note that SP2 does not include it (tested here), also you need to install Extension 1 *before* SP2
Regards,
Augusto Goncalves
Reply
04/14/2015 at 11:11 AM

---
**内容**: _davewolfe said...
Better way OpenProjectFileNoPrompt(string projectFile) from the PnPProjectManagerUI.dll
Reply
06/22/2016 at 07:57 PM

---
