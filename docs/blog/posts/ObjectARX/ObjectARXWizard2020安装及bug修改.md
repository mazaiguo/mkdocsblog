---
title: ObjectARXWizard2020安装及bug修改
date: 2024-08-10
categories:
  - CAD开发
  - ObjectARX
  - 开发工具
tags:
  - ObjectARX
  - Wizard
  - 安装配置
  - Bug修复
description: ObjectARX Wizard 2020安装步骤和常见bug的修改方法
author: JerryMa
---

# ObjectARX各版本免费下载

https://blog.csdn.net/lhxy24/article/details/101058720

[ObjectARX 2020 Wizard](https://github.com/ADN-DevTech/ObjectARX-Wizards/raw/ForAutoCAD2020/ObjectARXWizardsInstaller/ObjectARXWizard2020.zip)

[AutoCAD 2020 DotNet Wizard](https://github.com/ADN-DevTech/AutoCAD-Net-Wizards/raw/ForAutoCAD2020/AutoCADNetWizardsInstaller/AutoCAD_2020_dotnet_wizards.zip)

# ObjectARX2020 bug修改

1、C:\Program Files (x86)\Autodesk\ObjectARX 2020 Wizards\ArxAppWiz\Scripts\1033\default.js

从C:\Program Files (x86)\Autodesk\ObjectARX 2020 Wizards\ArxAppWiz\Templates\1033为新建项目的模板，拷贝这里面的文件，x64win32.vcxproj设置，要改变

```bash
<PropertyGroup Label="Globals">
    <ArxAppType>[!output PRJ_TYPE_APP]</ArxAppType>
    <RDS>[!output RDS_SYMB]</RDS>
    <TargetName Condition="'$(RDS)'!=''">$(RDS)$(ProjectName)</TargetName>
    <ProjectGuid>{F87873B0-2B5D-4D52-8FD5-BE1CDC50B2E3}</ProjectGuid>
    <WindowsTargetPlatformVersion>10.0.16299.0</WindowsTargetPlatformVersion>
  </PropertyGroup>
```


后面PropertyGroup 标签中的WindowsTargetPlatformVersion要考到前面来，否则找不到系统库。目标平台会被默认为win8.1，无法按win10SDK版本号导入目录。

2、C:\Program Files (x86)\Autodesk\ObjectARX 2020 Wizards\文件夹内外都有属性页设置，到底用的哪个还没整清楚。
应该是拷贝目录外面的，

```bash
CopyPropsFile ( 'Autodesk.arx-2020.props', strProjectName) ;
CopyPropsFile ( 'Autodesk.arx-2020-net.props', strProjectName) ;
CopyPropsFile ( 'crx.props', strProjectName) ;
```


因为crx.props在外面。

3、接2中，无论拷贝哪个属性页，目前是在项目中的vcxproj文件中，

合并上面这两个文件，之后
Autodesk.arx-2020.props文件会在合并下面6个文件
前三个

```bash
<Import Condition="'$(ArxAppType)'=='dbx' or '$(ArxAppType)'=='dbxnet'" Project="$(ArxSdkDir)\inc\dbx.props" />
<Import Condition="'$(ArxAppType)'=='crx' or '$(ArxAppType)'=='crxnet'" Project="$(ArxSdkDir)\inc\crx.props" />
<Import Condition="'$(ArxAppType)'=='arx' or '$(ArxAppType)'=='arxnet'" Project="$(ArxSdkDir)\inc\arx.props" />
```


后3个文件主要是不同项目类型的引用库的文件。

```bash
<Import Condition="'$(Configuration)'=='Release'" Project="$(ArxSdkDir)\inc\rxsdk_Releasecfg.props" />
<Import Condition="'$(Configuration)'=='Debug'" Project="$(ArxSdkDir)\inc\rxsdk_Debugcfg.props" />
<Import Condition="'$(ArxAppType)'=='dbxnet' or '$(ArxAppType)'=='crxnet' or '$(ArxAppType)'=='arxnet'" Project="Autodesk.arx-2020-net.props" />
```

这三个是调试和最终发布的一些设置，其中出bug那个地方是在<SmallerTypeCheck>true</SmallerTypeCheck>改为false。
原文链接：https://blog.csdn.net/ImummyI/article/details/103980572