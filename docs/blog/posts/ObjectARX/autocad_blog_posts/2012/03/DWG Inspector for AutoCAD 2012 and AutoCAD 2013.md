---
title: "DWG Inspector for AutoCAD 2012 and AutoCAD 2013"
date: 2012-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
description: "I just updated the C++ Inspector App to run on AutoCAD 2012/2013 and figured that, you know what, I may as well wrap this up as my very own Exchang..."
author: Autodesk
---
# DWG Inspector for AutoCAD 2012 and AutoCAD 2013

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/dwg-inspector-for-autocad-2012-and-autocad-2013.html

## 文章内容

By Fenton Webb
I just updated the C++ Inspector App to run on AutoCAD 2012/2013 and figured that, you know what, I may as well wrap this up as my very own Exchange Store App! That way you can install and use it as a ready built App, and/or install it and check out the code - so I did it. Of course, posting how I did it should help you work out how to create your own Apps for the Exchange Store too…
Here’s how I did it:
First of all, I created a folder structure that looks like this, notice the parent folder is suffixed with .bundle “Autodesk DWG Inspector.bundle”
Inside the Contents folder I have a Resources folder, and a Win32 and Win64 folder.
The Resources folder contains the Inspector Html readme with accompanying support files, check out that HTML file because if you create your own Autodesk Exchange App then you will want to derive your help from it as a template.
The Resources folder also contains a folder called DWGInspectorSource which houses the Inspector Visual Studio 2010 project. I made this project compile Debug versions of the ARX module in 32bit 2012/2013 and 64bit 2012/2013, in turn, these ARX modules are written to the Contents\Win32\Debug2008 which contains the 32bit VS 2008 AutoCAD 2012 ARX, Contents\Win32\Debug2010 which contains the 32bit VS 2010 AutoCAD 2013 ARX. Obviously, the Win64 folders contain the mirror of the 32bit except the ARX’s contained in there run for 64bit AutoCAD only.
Next, I created a PackageContents.xml file in the Autodesk DWG Inspector.bundle folder. This XML describes to the AutoCAD AppAutoloader what to load and how to load it…. This is what it looks like (I’ve commented the lines in the XML to explain what they do):
<?xml version="1.0" encoding="utf-8"?>
<!-- The ApplicationPackage element contains the Application properties -->
<!-- You need to generate your own ProductCode and UpgradeCode guids -->
<!-- If you update the product, the ProductCode needs to be regenerated, the UpgradeCode stays the same -->
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" ProductType="Application" 
          Name="DWG Inspector" AppVersion="1.0.0" Description="Debugging tools for AutoCAD - Inspector" 
          Author="Fenton Webb" 
          Icon="./Contents/Resources/resource/Inspector.jpg" 
          AppNameSpace="adn.exchange.autodesk.com" 
          OnlineDocumentation=" www.autodesk.com/developautocad" 
          HelpFile="./Contents/Resources/helpfile.html" 
          ProductCode="{56A544B1-A092-480D-8DEA-B07051DDBFAF}" UpgradeCode="{A36C0A9E-9970-400A-B598-8880ECD50875}">
    <!-- Information about your Company -->          
  <CompanyDetails Name="Autodesk" Phone=" " Url=" www.autodesk.com/developautocad" Email="devtech@autodesk.com" />
    <!-- Overview specification describing what OS, Autodesk product, version this entire set of components describes  -->          
  <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD*|AutoCAD" SeriesMin="R18.2" SeriesMax="R19.0" />
    <!-- A logical set of components, this Components section describes the 32bit AutoCAD 2012 version -->
  <Components Description="AutoCAD 2012/VS2008">
    <RuntimeRequirements OS="Win32" SeriesMin="R18.2" SeriesMax="R18.2" />
    <ComponentEntry AppName="DWGInspector" Version="1.0.0" 
                    ModuleName="./Contents/Resources/DWGInspectorSource/Win32/Debug2008/AdskInspector.arx" 
                    AppDescription="AutoCAD 2012/VS2008" 
                    LoadOnAutoCADStartup="True" />
  </Components>
    <!-- A logical set of components, this Components section describes the 32bit AutoCAD 2013 version -->
  <Components Description="AutoCAD 2013/VS2010">
    <RuntimeRequirements OS="Win32" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="DWGInspector" Version="1.0.0" 
                    ModuleName="./Contents/Resources/DWGInspectorSource/Win32/Debug2010/AdskInspector.arx" 
                    AppDescription="AutoCAD 2013/VS2010" 
                    LoadOnAutoCADStartup="True" />
  </Components>
    <!-- A logical set of components, this Components section describes the 64bit AutoCAD 2012 version -->
  <Components Description="AutoCAD 2012/VS2008">
    <RuntimeRequirements OS="Win64" SeriesMin="R18.2" SeriesMax="R18.2" />
    <ComponentEntry AppName="DWGInspector" Version="1.0.0" 
                    ModuleName="./Contents/Resources/DWGInspectorSource/x64/Debug2008/AdskInspector.arx" 
                    AppDescription="AutoCAD 2012/VS2008" 
                    LoadOnAutoCADStartup="True" />
  </Components>
    <!-- A logical set of components, this Components section describes the 64bit AutoCAD 2013 version -->
  <Components Description="AutoCAD 2013/VS2010">
    <RuntimeRequirements OS="Win64" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="DWGInspector" Version="1.0.0" 
                    ModuleName="./Contents/Resources/DWGInspectorSource/x64/Debug2010/AdskInspector.arx" 
                    AppDescription="AutoCAD 2013/VS2010" 
                    LoadOnAutoCADStartup="True" />
  </Components>
</ApplicationPackage>
Finally, I sent the bundle to the Autodesk AppStore team and they sent me back my very own installer – super cool. Here’s the zip file containing the App installer.
Autodesk DWG Inspector App

## 评论

**内容**: badziewiak said...

This has been successfully installed but not working on AC2012 x64 win7 x64. I do not see the window.
Reply
07/26/2012 at 02:16 PM

---
**内容**: badziewiak said in reply to badziewiak...
It works fine. It should load the c:\Users\...\AppData\Roaming\Autodesk\ApplicationPlugins\Autodesk DWG Inspector.bundle\Contents\Win64\Debug2008\AdskInspector.arx
Reply
07/27/2012 at 12:06 AM

---
