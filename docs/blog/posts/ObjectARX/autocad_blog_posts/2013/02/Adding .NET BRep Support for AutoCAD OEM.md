---
title: "Adding .NET BRep Support for AutoCAD OEM"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - OEM
  - Plugin
description: "The BRep modules are not included with any commands via the OEMMakeWizard, therefore if your .NET OEM application depends on the Brep API you will ..."
author: Autodesk
---
# Adding .NET BRep Support for AutoCAD OEM

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/adding-net-brep-support-for-autocad-oem.html

## 文章内容

by Fenton Webb
The BRep modules are not included with any commands via the OEMMakeWizard, therefore if your .NET OEM application depends on the Brep API you will have to add the acdbmgdbrep.dll to the OEMMakeWizard by hand.
Here’s how:
1) In the OemMakeWizard Your Modules Page, add acdbmgdbrep.dll as a BindMGDARX to be placed in the EXE folder, not required
2) In the Your Module Settings page, for acdbmgdbrep.dll, set the Logical Name to ACDBMGDBREP and set the Load Controls to the AcadApp::LoadReasons::LoadOnAutoCADStartup i.e. 2
3) Rebuild.

