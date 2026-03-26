---
title: "AutoCAD Performance Gauges App"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I wrote this App to demonstrate some basic AutoCAD Messaging and Threading concepts at Autodesk University last year, I thought you might like to s..."
author: Autodesk
---
# AutoCAD Performance Gauges App

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/autocad-performance-gauges-app.html

## 文章内容

by Fenton Webb
I wrote this App to demonstrate some basic AutoCAD Messaging and Threading concepts at Autodesk University last year, I thought you might like to see the App and the code behind it.
Here’s a snap shot of the installed App…
As you can see, there are seven WPF gauges, all hosted in a RibbonCompositeItem, described left to right…
Total number of objects being opened for read, per second
Total number of objects being closed, per second
Total number of objects being opened for write, per second
Total number of objects being erased, per second
Total number of objects being deepCloned, per second
Total number of view updates occurring, per second
Total number of DWG files being found on your hard drive, using a .NET Background worker thread.
What you might find interesting about this App is the nice smooth interactive feel of the whole thing; the purpose of this demo App is to show how to keep dynamic UI working, whilst keeping the AutoCAD UI responsive. After you have seen it work, I recommend that you take a look at the source code that I have attached to see how it works (the source is also included inside of the .bundle Contents/Resource folder) - I hope you like it.
Some topics to note inside the code…
Check out the way I post updates to the gauges using Dispatcher.BeginInvoke.
Check out the RelativeSource.Self Databinding style I’m using
Look at the power of our Overrule API!
Do not use worker threads with AutoCAD directly, AutoCAD is not multithread aware.
Some things that the App doesn’t do at this time…
The gauges only work for the start-up document, I have not coded any document switching.
Finally, this App also shows how to “Autoload” CUI Custom Ribbon controls, for both AutoCAD 2012 and 2013... One of the features of the Autoloader is the ability for it to load WPF Dll’s away from the acad.exe directory; it does this by implementing an AssemblyResolve event handler. In addition, the Autoloader does the full CUI Custom Ribbon control registration for you – niiiice.
Here’s the PackageContents.xml for reference, it shows how the CUI utilizes and references the CUI Custom Ribbon Control via the Autoloader...
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" ProductType="Application" Name="Fentons AutoCAD Performance Monitor" AppVersion="1.0.0" Description="Displays Featured Apps for Autodesk products" Author="Fenton Webb" OnlineDocumentation="www.autodesk.com/joinadn" HelpFile="./Contents/Resources/Source Code/AcadPerfMon/AcadPerfMon.sln" ProductCode="{D2D4BA3C-2B46-4285-80C8-546548181331}" UpgradeCode="{DD1DE7DC-D831-4AFB-891D-5A987987987C}" SupportedLocales="Enu" AppNameSpace="appstore.exchange.autodesk.com">
  <CompanyDetails Name="Autodesk" Phone=" " Url="www.autodesk.com/joinadn" Email="fenton.webb@autodesk.com" />
  <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD*|AutoCAD" SeriesMin="R18.2" SeriesMax="R19.0" />
  <Components Description="AutoCAD 2012">
    <RuntimeRequirements OS="Win64|Win32" Platform="AutoCAD|AutoCAD*" SeriesMin="R18.2" SeriesMax="R18.2" />
    <ComponentEntry AppName="AcadPerfMon" Version="1.0.0" ModuleName="./Contents/Resources/AcadPerfMon.cuix" AppDescription="Performance Gauges Ribbon control">
      <RibbonControls>
        <RibbonControl Name="au" Path="pack://application:,,,/AcadPerfMon;component/MyControls/ResourceDictionary.xaml" />
      </RibbonControls>
      <AssemblyMappings>
        <AssemblyMapping Name="AcadPerfMon" Path="./Contents/Windows/2012/AcadPerfMon.dll" />
      </AssemblyMappings>
    </ComponentEntry>
    <ComponentEntry AppName="AcadPerfMon" Version="1.0.0" ModuleName="./Contents/Windows/2012/CircularGauge.dll" AppDescription="WPF Gauge" />
  </Components>
  <Components Description="AutoCAD 2013">
    <RuntimeRequirements OS="Win64|Win32" Platform="AutoCAD|AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="AcadPerfMon" Version="1.0.0" ModuleName="./Contents/Resources/AcadPerfMon.cuix" AppDescription="Performance Gauges Ribbon control">
      <RibbonControls>
        <RibbonControl Name="au" Path="pack://application:,,,/AcadPerfMon;component/MyControls/ResourceDictionary.xaml" />
      </RibbonControls>
      <AssemblyMappings>
        <AssemblyMapping Name="AcadPerfMon" Path="./Contents/Windows/2013/AcadPerfMon.dll" />
      </AssemblyMappings>
    </ComponentEntry>
    <ComponentEntry AppName="AcadPerfMon" Version="1.0.0" ModuleName="./Contents/Windows/2013/CircularGauge.dll" AppDescription="WPF Gauge" />
  </Components>
</ApplicationPackage>
Please find the App bundle and the whole source code attached to this post. To see it run, simply copy the .bundle to your %APPDATA%\Autodesk\ApplicationPlugins folder.

## 评论

**内容**: Autocad Training said...
Thanks for sharing such an amazing information.
Keep posting more information about autocad.
Reply
04/30/2015 at 10:15 AM

---
**内容**: Peter2 said...
Hi Fenton
where to find the plugin for current versions 2014 - 2016? At the App-store there seem to be nothinh ...
Peter
Reply
06/29/2015 at 02:54 AM

---
**内容**: Alexander said...
Hello.I am trying to understand how to make Custom Control in ribbon.
It's almost what i want, but I do not use bundle.
How can I add RibbonCompositeItem to Ribbon in code (C#)?

Sorry for poor english - use online translator
Reply
12/08/2015 at 10:42 AM

---
