---
title: "Folder structure for Autoloader Bundles using Revit as an Example"
date: 2013-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "If you are posting an App to the Exchange store, posting your files as an unorganized zip will delay posting of your App."
author: Autodesk
---
# Folder structure for Autoloader Bundles using Revit as an Example

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/folder-structure-for-autoloader-bundles-using-revit-as-an-example.html

## 文章内容

by Fenton Webb
If you are posting an App to the Exchange store, posting your files as an unorganized zip will delay posting of your App. 
Here’s a quick tutorial on how to lay your app bundle out before posting to the Exchange store.
First of all, you need to understand what the bundle folder structure is all about.
The bundle App folder structure is a Windows and Mac solution for deploying Autodesk plugins. AutoCAD also comes as a Mac product, we also have various cloud an mobile products like AutoCAD WS that are/will be using the bundle format.
The bundle App folder structure supports multiple versions in the same bundle, this is intended for ease of deployment and for a clean user experience. It’s true that all versions of your App will be installed, even if the user doesn’t have the supporting version on his system so there is some waste; because of this you have to make sure you carefully lay out your bundle to share resources.
The bundle App folder structure allows for multiple Autodesk product support in the same bundle. This is particularly useful if you have a main application plugin that has extensions. For instance, say you have a Revit room designer main app with export/import functions that link to AutoCAD.
Here are some bundle folder layout recommendations for creating various App bundles… You can add as many folders as you like, but your App must be self contained.
Revit App Bundle Folder Example
The Resources folder is intended to to store your application help files, icons, any shared resources that your application has.
Win32 is intended to house all of your Windows 32bit specific runtime. If your application is platform independent, then there’s no need to have a Win32 folder, simply use the Windows folder.
Win64 is intended to house all of your Windows 64bit specific runtime. If your application is platform independent, then there’s no need to have a Win64 folder, simply use the Windows folder.
The Windows folder is intended to house all platform independent runtime. If you have platform specific runtime, then use either the Win32 or Win64 folders.
The R2013 and R2014 folders are Revit specific version folders. These folders are intended to house version specific runtime, for example Revit 2013 runtime for Win32 goes in the Win32\R2013 folder. If you have shared DLL components for both 2013 and 2014, say a licensing.dll then you can simply suffix the Revit version on your DLL name e.g. MyRevitApp2013.dll and MyRevitApp2014.dll then just house all 3 DLLs in the specific platform folder (Win32/Win64 or Windows)
Revit App Bundle Example with AutoCAD Extensions
AutoCAD uses a different series versioning system than Revit. AutoCAD generally has binary compatibility between series, however it does normally break every 3 releases. If you want to include AutoCAD extensions to your Revit product, here’s how you would lay out your bundle. (Notice I have omitted R19.1 AutoCAD 2014, that’s because R19.1 is binary compatible with R19.0)
Submit your Apps to Exchange using this format, and your Apps with be processed quicker.

## 评论

**内容**: Catherine Mbinya said...
Thank you for sharing.
Reply
06/29/2019 at 03:25 AM

---
