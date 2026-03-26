---
title: "AcadStartup and AutoCAD OEM"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
  - Unicode
  - VBA
description: "I am having problems launching my VBA app in AutoCAD OEM.  The problem is that VBA is not getting automatically loaded.  If I manually load my VBA ..."
author: Autodesk
---
# AcadStartup and AutoCAD OEM

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/acadstartup-and-autocad-oem.html

## 文章内容

By Fenton Webb
Issue
I am having problems launching my VBA app in AutoCAD OEM.  The problem is that VBA is not getting automatically loaded.  If I manually load my VBA app, then VBA gets initialized.  Since my product runs as a silent, unattended app, how can I force VBA to be initialized? 
Solution
First, you will need to name your DVB to <prog4>.dvb, where <prog4> represents the first four letters of your AutoCAD OEM program's name.  If you have a macro named ‘AcadStartup’, this macro will run when the VBA initialization is complete.  However, the VBA initialization is not complete until AcVba.arx is done loading, so AcVba.arx needs to be loaded at startup.  You can set your AcVba.arx module to demand load using the MakeWizard (by just selecting ‘Build Resources’ and NOT ‘Bind ARX’), but probably it is easier for you to use an RX file to load AcVba.arx at startup.
For an RX file, you will have to name it <prog4>.rx (to match the first four letters of your AutoCAD OEM program's name).  This RX file is just a text file with a single line of ‘AcVba.arx’.  Make the text file, place it in your project file location (\OEMInstall\Projects\<prog4>\...), and add it as a module in Your Modules, specifying ‘CopyFile’ for Build With and ‘Exe’ as Build Destination. This will also ensure that the file is created in your installer, if you use the OEMInstallerWizard.

