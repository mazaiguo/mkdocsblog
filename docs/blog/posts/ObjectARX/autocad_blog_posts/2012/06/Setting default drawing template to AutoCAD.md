---
title: "Setting default drawing template to AutoCAD"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
description: "Below code shows the procedure to set the default drawing template to AutoCAD. So, once you set the template path, AutoCAD opens the template file ..."
author: Autodesk
---
# Setting default drawing template to AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/setting-default-drawing-template-to-autocad.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to set the default drawing template to AutoCAD. So, once you set the template path, AutoCAD opens the template file automatically, without asking the user for template selection during “New” command.
        <CommandMethod("setTempalatePath")> _
        Public Shared Sub setTempalatePath()
            Dim acadApp As Object = Application.AcadApplication
            Dim files As Object = acadApp.Preferences.Files
            Application.ShowAlertDialog("Old template file : " _
                                            + files.QNewTemplateFile)
              'Give full path...
            files.QNewTemplateFile = "c:\MyTemplates\acad.dwt"
            Application.ShowAlertDialog("new template file : " _
                                            + files.QNewTemplateFile)
        End Sub

