---
title: "Upgrading C++/CLI Wrappers for Custom Entities to .NET 8.0"
date: 2024-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - Migration
description: "AutoCAD 2025 started supporting .NET 8.0 platform, if you have managed wrapper or interop API for custom entities, you need to upgrade them from NE..."
author: Autodesk
---
# Upgrading C++/CLI Wrappers for Custom Entities to .NET 8.0

发布日期: 2024-06-01

原始链接: https://adndevblog.typepad.com/autocad/2024/06/upgrading-ccli-wrappers-for-custom-entities-to-net-80.html

## 文章内容

By Madhukar Moogala
AutoCAD 2025 started supporting .NET 8.0 platform, if you have managed wrapper or interop API for custom entities, you need to upgrade them from NET 4.x to NET 8.0
Upgrading managed wrappers is three fold process
First, you need to upgrade arx or dbx project (*.vcxproj) to target new SDK version
Second, you need to upgrade the wrapper project (C++\CLI) to NET 8.0
Third, you need to upgrade the client side plugin project from NET 4x to NET 8.0
Here is the step by step guide to upgrade the managed wrapper project from NET 4.x to NET 8.0
Update the .vcxproj File:
Replace <CLRSupport>true</CLRSupport> properties with <CLRSupport>NetCore</CLRSupport>.
Replace <TargetFrameworkVersion> properties with <TargetFramework>net8.0</TargetFramework>.
Remove .NET Framework References:
Remove any references to System, System.Core,System.Data, System.Windows.Forms, and System.Xml from your project.
Update API Usage:
Review your .cpp files and update any APIs that are unavailable in .NET.
WPF and Windows Forms Usage:
C++/CLI projects can use Windows Forms and WPF APIs.
Add explicit framework references to the UI libraries.
To use Windows Forms APIs, add this reference to the .vcxproj file:
<!-- Reference all of Windows Forms -->
    <FrameworkReference Include="Microsoft.WindowsDesktop.App.WindowsForms" />
    
To use WPF APIs, add this reference to the .vcxproj file:
<!-- Reference all of WPF -->
    <FrameworkReference Include="Microsoft.WindowsDesktop.App.WPF" />
    
To use both Windows Forms and WPF APIs, add this reference to the .vcxproj file:
<!-- Reference the entirety of the Windows desktop framework:     Windows Forms, WPF, and the types that provide integration between them -->
    <FrameworkReference Include="Microsoft.WindowsDesktop.App" />
    
Remember that there are some limitations when migrating C++/CLI projects to .NET Core, such as not being able to compile to an executable directly and Windows-only support for C++/CLI. Make sure to check the documentation for more details
Upgrading a .NET 4.x Project to .NET 8.0
Open the Project File:
In Visual Studio, navigate to Solution Explorer.
Right-click on the ManagedTest project and select "Upgrade"
Refer: How to use upgrade assistant)
Update the Project Configuration:
Locate the <TargetFramework> property and change its value to net8.0-windows. This specifies that the project targets the latest .NET 8.0 framework for Windows.
Find the <Platforms> property and set it to x64. This indicates that the project is built for the 64-bit architecture.
Configure Assembly Search Paths:
Locate the <AssemblySearchPaths> property (it might not exist yet).
Add the path to your ObjectARX SDK directory within the property's value. This ensures that .NET references from the SDK are found during compilation. Here's an example structure:
XML
            <AssemblySearchPaths>$(OutDir);$(ReferencePath);C:\Path\To\Your\ObjectARX\SDK</AssemblySearchPaths>
            
          
Replace C:\Path\To\Your\ObjectARX\SDK with the actual path to your ObjectARX SDK installation.
Optional: Update Root Namespace (if necessary):
If your project uses a specific root namespace to organize its files, locate the <RootNamespace> property and ensure it matches your project directory name.
Save the Project File:
Save the changes made to the project file (ManagedTest.csproj).
Here is the sample project file for your reference
    <?xml version="1.0" encoding="utf-8"?>
    <Project Sdk="Microsoft.NET.Sdk">
    <PropertyGroup>
    <OutputType>Library</OutputType>
    <RootNamespace>ManagedTest</RootNamespace>
    <TargetFramework>net8.0-windows</TargetFramework>
    <GenerateAssemblyInfo>false</GenerateAssemblyInfo>
    <ObjectARXPATH Condition="'$(ObjectARXPATH)' == ''">D:\ArxSdks\arx2025</ObjectARXPATH>
    <AssemblySearchPaths>$(ObjectARXPATH)\inc\;$(AssemblySearchPaths)</AssemblySearchPaths>
    <Platforms>x64</Platforms>
    </PropertyGroup>
    <ItemGroup>
    <FrameworkReference Include="Microsoft.WindowsDesktop.App"/>
    </ItemGroup>
    <ItemGroup>
    <ProjectReference Include="..\ManagedWrapper\ManagedWrapper.vcxproj" />
    </ItemGroup>
    <ItemGroup>
    <Reference Include="AcDbMgd">
    <Private>False</Private>
    </Reference>
    <Reference Include="AcMgd">
    <Private>False</Private>
    </Reference>
    <Reference Include="AcCoreMgd">
    <Private>False</Private>
    </Reference>
    </ItemGroup>
    </Project>   
  
The Github project is available at ManagedCircle

