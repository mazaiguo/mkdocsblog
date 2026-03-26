---
title: "Register Autoloader on Mac"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Plugin
description: "I know that Autoloader is available both on Mac and Windows but on Mac the AutoCAD installer does not seem to register it. How could I register it ..."
author: Autodesk
---
# Register Autoloader on Mac

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/register-autoloader-on-mac.html

## 文章内容

By Adam Nagy
I know that Autoloader is available both on Mac and Windows but on Mac the AutoCAD installer does not seem to register it. How could I register it programmatically so that it would load my AddIn's automatically?
Solution
If you look into the contents of the *.bundle files in the AutoCAD.app folder, then you can see that they contain an arx.plist file and this file contains the autoload settings that you would find in the registry in case of the Windows version of AutoCAD.
When you install AutoCAD for Mac 2011, then autoloader.bundle does not contain this arx.plist file by default, and so it is not autoloaded into AutoCAD. Once you APPLOAD'ed autoloader.bundle for the first time then arx.plist file will be created and added to the autoloader.bundle folder and so you could copy it from there and distribute it with your AddIn's installer, which in turn would copy it into the autoloader.bundle folder.

