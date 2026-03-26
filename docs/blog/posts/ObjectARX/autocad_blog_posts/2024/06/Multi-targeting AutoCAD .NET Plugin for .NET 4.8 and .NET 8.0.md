---
title: "Multi-targeting AutoCAD .NET Plugin for .NET 4.8 and .NET 8.0"
date: 2024-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "Recently, we received a query from an ADN partner on how to organize code to target multiple frameworks, such as .NET 4.x and .NET 8.0."
author: Autodesk
---
# Multi-targeting AutoCAD .NET Plugin for .NET 4.8 and .NET 8.0

发布日期: 2024-06-01

原始链接: https://adndevblog.typepad.com/autocad/2024/06/multi-targeting-autocad-net-plugin-for-net-48-and-net-80.html

## 文章内容

By Madhukar Moogala
Recently, we received a query from an ADN partner on how to organize code to target multiple frameworks, such as .NET 4.x and .NET 8.0.
Let's take an ARX SDK sample project, EllipseJig.
EllipseJig is a simple .NET project that demonstrates the use of Jig APIs to create ellipses. The project is available in the ObjectARX SDK samples
Here is the project structure

```html
<Project Sdk="Microsoft.NET.Sdk">
<PropertyGroup>
    <AssemblyName>JigSample</AssemblyName>
    <OutputType>Library</OutputType>
    <RootNamespace>JigSample</RootNamespace>
    <TargetFramework>net8.0-windows</TargetFramework>
    <GenerateAssemblyInfo>False</GenerateAssemblyInfo>
    <Platforms>x64</Platforms>
    <Configurations>ACAD2024;ACAD2025</Configurations>
    <BaseOutputPath>bin</BaseOutputPath>
</PropertyGroup>
<PropertyGroup Condition="'$(Configuration)' == 'ACAD2025'">
    <TargetFramework>net8.0-windows</TargetFramework>
    <!-- uncomment to use Forms or WPF-->
    <!--<UseWindowsForms>true</UseWindowsForms>
  <UseWPF>true</UseWPF>-->
    <AssemblySearchPaths>D:\ArxSdks\Arx2025\inc\;$(AssemblySearchPaths)</AssemblySearchPaths>
</PropertyGroup>
<PropertyGroup Condition="'$(Configuration)' == 'ACAD2024'">
    <TargetFramework>net48</TargetFramework>
    <AssemblySearchPaths>D:\ArxSdks\Arx2024\inc\;$(AssemblySearchPaths)</AssemblySearchPaths>
</PropertyGroup>
<ItemGroup Condition="'$(Configuration)' == 'ACAD2025'">
    <FrameworkReference Include="Microsoft.WindowsDesktop.App"/>
</ItemGroup>
<ItemGroup>
    <Reference Include="AcDbMgd">
        <Private>False</Private>
    </Reference>
    <Reference Include="acmgd">
        <Private>False</Private>
    </Reference>
    <Reference Include="accoremgd">
        <Private>False</Private>
    </Reference>
</ItemGroup>
```
</Project>


Github Project : Ellipsejig
Note:
We encourage you to use Git branching to organize and maintain releases instead of organizing projects to target multiple frameworks. This is the same approach we adopt with the AutoCAD source code, which has billions of lines of code.
In the image below, our main branch is always the latest and newest state and content.
When it's time to switch to a new release, we branch "main" into "release2025." After that, "main" will become "2026," and so on.
So, if your main branch is currently supporting AutoCAD 2024, you would branch this off into "release2024" and then change "main" to support AutoCAD 2025.
For example, please find the Github project : ManagedCircle
There are two branches:
master - which is the current release 2025,
another branch for AutoCAD 2024 (.NET F4x)
If I have to roll out a fix to AutoCAD 2024, I will simply switch to that branch and work on it.

