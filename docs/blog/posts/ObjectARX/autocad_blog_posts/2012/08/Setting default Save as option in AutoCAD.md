---
title: "Setting default Save as option in AutoCAD"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM
  - COM Interop
description: "You can use ActiveX API “IAcadPreferencesOpenSave.SaveAsType” to set the default save option. “AcSaveAsType” enum provides various options which yo..."
author: Autodesk
---
# Setting default Save as option in AutoCAD

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/setting-default-save-as-option-in-autocad.html

## 文章内容

By Virupaksha Aithal
You can use ActiveX API “IAcadPreferencesOpenSave.SaveAsType” to set the default save option. “AcSaveAsType” enum provides various options which you can set to IAcadPreferencesOpenSave.SaveAsType. Below code shows the procedure to use the “SaveAsType” API in VB.NET
        <CommandMethod("Setsaveastype")> _
        Public Shared Sub Setsaveastype()
            'with Reference to acad interops
            Dim acadApp As AcadApplication = _
                                        Application.AcadApplication
            'set the 2007 DWG as default
            acadApp.Preferences.OpenSave.SaveAsType = _
                                    Common.AcSaveAsType.ac2007_dwg
              'late binding (without Reference to acad interops)
            'Dim acadApp As Object = Application.AcadApplication
            '36 is the enum value of ac2007_dwg
            'acadApp.Preferences.OpenSave.SaveAsType = 36
        End Sub

## 评论

**内容**: MX said...
Can AcSaveAsType also be set to AutoCAD Mechanical files?
Reply
02/14/2019 at 04:43 AM

---
