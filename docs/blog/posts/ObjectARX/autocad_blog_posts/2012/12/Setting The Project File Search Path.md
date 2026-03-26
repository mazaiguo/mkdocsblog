---
title: "Setting The Project File Search Path"
date: 2012-12-01
categories:
  - AutoCAD VBA
tags:
  - API
  - AutoCAD
  - COM
  - VBA
description: "If you use the Drawing projects feature of AutoCAD regularly, you might wonder how to get/set the project file search path programmatically?"
author: Autodesk
---
# Setting The Project File Search Path

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/setting-the-project-file-search-path.html

## 文章内容

By Gopinath Taget
If you use the Drawing projects feature of AutoCAD regularly, you might wonder how to get/set the project file search path programmatically?
To get the project file path name, use the GetProjectFilePath method of AcadPreferencesFiles object accessible using the ActiveX API. You can also set the project file path name using SetProjectFilePath method of AcadPreferencesFiles object. And the current project name is stored in the system variable "PROJECTNAME".
There are however no ActiveX methods available to obtain the list of project names that you can access through Options dialog in the UI. One work around would be to directly read the information from the registry. The project names will be available under the following key.
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\RXX.X\ACAD-XXXX:XXX\Profiles\<<Unnamed Profile>>\Project Settings\
The following sample VBA code gets the path information for the Project called "TestProject". Remember to add a project by name TestProject before testing this sample.
Sub f_test()
  Dim po_pref As AcadPreferences
  Set po_pref = ThisDrawing.Application.Preferences
    MsgBox po_pref.Files.GetProjectFilePath("TestProject")
  Call po_pref.Files.SetProjectFilePath("TestProject",
                                      "c:\my documents")
End Sub

