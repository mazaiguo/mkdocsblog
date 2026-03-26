---
title: "DWG file type association"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "Here is some information on .dwg file type association that you may find helpful especially if you multiple softwares that can open .dwg files inst..."
author: Autodesk
---
# DWG file type association

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/dwg-file-type-association.html

## 文章内容

By Balaji Ramamoorthy
Here is some information on .dwg file type association that you may find helpful especially if you multiple softwares that can open .dwg files installed in your system.
The applications that can open .dwg files in a system are listed under the following registry key :
HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps
For example, AutoCAD could be listed under :
HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps\{F29F85E0-4FF9-1068-AB91-08002B27B3D9}:AutoCAD
The default application that will be used for opening .dwg file is under 
HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps -> (Default) key
AutoCAD reads the following registry key at startup to know if .dwg file type is associated with AutoCAD.
HKEY_CURRENT_USER\Software\Classes\.dwg
If this key is not found as would be expected when running AutoCAD for the very first time, AutoCAD would display the DWG Association dialog as shown in this screenshot.
In case you want AutoCAD to show this dialog in any of its subsequent invocations, simply try renaming the ".dwg" registry key under "HKEY_CURRENT_USER\Software\Classes"
To always automatically reassociate the .dwg without prompting the user, the following registry key was required is to be set :
HKCU\Software\Autodesk\AutoCAD\R20.0\ACAD-E001:409\Profiles\<<Unnamed Profile>>\General
DwgAlwaysAssociate : 1
To never associate .dwg automatically and also prevent the reassociate dialog from appearing, the following  registry key is to be set :
HKCU\Software\Autodesk\AutoCAD\R20.0\ACAD-E001:409\Profiles\<<Unnamed Profile>>\General
DwgAlwaysAssociate : 0
If you do not find the DwgAlwaysAssociate key in the registry, you can create it as a DWORD.
Please ensure that you make the registry changes with care and keep a backup of the registry keys that you are changing by first exporting them as .reg files. This is important to undo the changes if you face any problems later.

