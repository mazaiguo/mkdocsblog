---
title: "Autoloader Example for invoking a Startup Command in AutoCAD"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - Migration
  - Palette
description: "Initializing AutoCAD UI from within your .NET Initialize() is not advised. The reason is that your .NET DDL may be loaded on AutoCAD startup, and a..."
author: Autodesk
---
# Autoloader Example for invoking a Startup Command in AutoCAD

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/autoloader-example-for-invoking-a-startup-command-in-autocad.html

## 文章内容

by Fenton Webb
  Initializing AutoCAD UI from within your .NET Initialize() is not advised. The reason is that your .NET DDL may be loaded on AutoCAD startup, and at the point Initialize for your App is called certain subsystems inside of AutoCAD have not properly initialized – e.g. Ribbon, COM, Palettes, etc.
The normal solution is to create a document event reactor inside of your Initialize() and watch for a new document created, then from within there create another event reactor which watches for AutoCAD entering Quiescent state, then, from within that function callback do your initialize.
Using the Autoloader, all of this is handled for your automatically, simply use the Commands::Command.StartupCommand attribute to indicate your startup/initialize command. e.g.
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" Name="MyTestApp" Description="FentyCAD demo app" AppVersion="1.0.0" FriendlyVersion="1.0.0" ProductType="Application" SupportedLocales="Enu" AppNameSpace="appstore.exchange.autodesk.com" Author="Fenton Webb" ProductCode="{17FFEEB3-D653-491D-97D3-40FC069FB967}" UpgradeCode="{1F07C18D-E5D9-4775-9A80-3E240CB4D1C3}">
  <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD|AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.1" />
  <CompanyDetails Name="FentyCAD" Url="www.FentyCAD.com" Email="info@FentyCAD.com" />
  <Components Description="Any CPU DLLs">
    <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD|AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.1" />
    <ComponentEntry AppName="FentiCADMain" Version="1.0.0" ModuleName="./Contents/Windows/MyApp.dll" AppDescription="Main App .NET DLL" LoadOnCommandInvocation="True">
      <Commands GroupName="FentyCAD_MAIN">
        <Command Local="_FCStartup" Global="FCStartup" Description="Startup command used to initialize my app" StartupCommand="True" />
      </Commands>
    </ComponentEntry>
  </Components>
</ApplicationPackage>

## 评论

**内容**: Alexander Rivilis said...
Typo: not ".NET DDL" but ".NET DLL"
Reply
04/22/2013 at 01:37 PM

---
**内容**: Narayanan Devarajan said...
Thanks Fenton, does this work with AutoCAD OEM? Based on my (limited) observation, I could not find folders %APPDATA%/Autodesk/ApplicationPlugins and
%ProgramFiles%/Autodesk/ApplicationPlugins where my OEM product is installed.
Are there any other special folder where the AOEM.Exe will look for the bundle during its load?
Many thanks.
Reply
08/08/2014 at 04:15 AM

---
