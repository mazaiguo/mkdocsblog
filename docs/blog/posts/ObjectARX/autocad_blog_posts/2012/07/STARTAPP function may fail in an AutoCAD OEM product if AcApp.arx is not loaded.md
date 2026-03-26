---
title: "STARTAPP function may fail in an AutoCAD OEM product if AcApp.arx is not loaded"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
description: "An error occurs when the (startapp) function is used in an AutoCAD OEM product: "Error: no function definition: STARTAPP". When I load the .fas fil..."
author: Autodesk
---
# STARTAPP function may fail in an AutoCAD OEM product if AcApp.arx is not loaded

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/startapp-function-may-fail-in-an-autocad-oem-product-if-acapparx-is-not-loaded.html

## 文章内容

by Fenton Webb
Issue
An error occurs when the (startapp) function is used in an AutoCAD OEM product: "Error: no function definition: STARTAPP". When I load the .fas file in Standard AutoCAD, the function works correctly and no error occurs. What is the cause of this problem in the OEM version?
Solution
The (startapp) function depends on AcApp.arx, so it needs it loaded to work correctly. This module may not be loaded automatically when the project is run from the OEM Make wizard. If an installer is made for the project and the product is installed, then AcApp.arx is always loaded automatically.
The arxload function could be used to avoid this problem as in this example.
(defun c:test ()
  (arxload "AcApp.arx")
  (startapp "hh.exe" (findfile "c:/ARXSDK/docs/arxdoc.chm"))
)
NOTE: You should always test your OEM application as an installed application, not just as a build from the OEMMakeWizard – that way you ensure that the product is fully installed and registered correctly.

