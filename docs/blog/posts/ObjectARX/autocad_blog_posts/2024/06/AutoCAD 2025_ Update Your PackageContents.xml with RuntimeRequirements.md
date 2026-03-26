---
title: "AutoCAD 2025: Update Your PackageContents.xml with RuntimeRequirements"
date: 2024-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "If you are using PlugIn-Autoloader mechanism to install custom applications, this important update is for you"
author: Autodesk
---
# AutoCAD 2025: Update Your PackageContents.xml with RuntimeRequirements

发布日期: 2024-06-01

原始链接: https://adndevblog.typepad.com/autocad/2024/06/autocad-2025-update-your-packagecontentsxml-with-runtimerequirements.html

## 文章内容

By Madhukar Moogala
If you are using PlugIn-Autoloader mechanism to install custom applications, this important update is for you
With the release of AutoCAD 2025, Autoloader engine checks for RuntimeRequirements for applications. In other words, you need to specify the series bounds for your application if the ComponentEntry \ AppType is .NET to load in AutoCAD 2025.
RuntimeRequirements has two attributes which defines supportablity of your application component on AutoCAD
The following description holds true for any other application but not for .NET plugins.
RuntimeRequirements Attributes
Attribute Description
SeriesMin Defines the minimum product release number that the set of components supports.The value can be a major version number (R24) or a specific version (R24.1). The version number can be found in the Windows Registry or obtained with the ACADVER system variable in AutoCAD-based products.If this attribute and SeriesMaxare not specified, it is assumed all components are compatible with all product releases. If you omit this value, any version before that specified by the SeriesMaxattribute is allowed.
SeriesMax Defines the maximum product release number that the set of components supports.If you omit this value, any version after that specified by the SeriesMin attribute is allowed.
What Changed?
If the SeriesMax is not set for a particular component in the bundle PackageContents.xml (via the RuntimeRequirements element) the Autoloader assumes it is a compatible component and loads it. However, since the API breaks because of the .NET upgrade, the app may crash while loading.
So, it is important to specify the SeriesMax attribute in the RuntimeRequirements element.
Here is the sample code PackageContents.xml to specify the series bounds for your .NET based applications targeting AutoCAD 2025
EDIT:
Thanks to Nedeljko Sovljanski it was plain oversight to place RuntimeRequirements at incorrect scope.
      
```html
<?xml version="1.0" encoding="UTF-8"?>
<ApplicationPackage SchemaVersion="1.0" Name="HelloWorld" 
AppVersion="2024.1.0" Description="A basic HelloWorld application"
 Author="Madhukar Moogala" ProductCode="90bcc406-78d2-4667-bef8-12c02e1ab25b">
   <CompanyDetails Name="APS" Url="" Email="" />
   <Components>
      <ComponentEntry AppName="HelloWorld" 
      ModuleName="HelloWorld.dll" 
      AppDescription="A simple hello" 
      AppType=".Net" 
      LoadOnAutoCADStartup="True">
         <RuntimeRequirements OS="Win64" SeriesMin="R20.0" SeriesMax="R24.3" />
         <Commands GroupName="HelloMGD">
            <Command Local="HELLO" Global="HELLO" />
         </Commands>
      </ComponentEntry>
      <ComponentEntry AppName="HelloWorld" 
      ModuleName="HelloWorld_NET8.0.dll" 
      AppDescription="A simple hello" 
      AppType=".Net" 
      LoadOnAutoCADStartup="True">
         <RuntimeRequirements OS="Win64" SeriesMin="R25.0" SeriesMax="R25.0" />
         <Commands GroupName="HelloMGD">
            <Command Local="HELLO" Global="HELLO" />
         </Commands>
      </ComponentEntry>
   </Components>
</ApplicationPackage>
```

