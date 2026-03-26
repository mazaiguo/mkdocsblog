---
title: "About Exchange App Installer automatic Localization"
date: 2013-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When you submit your apps to Autodesk Exchange you get back an MSI which installs you app, super cool!"
author: Autodesk
---
# About Exchange App Installer automatic Localization

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/about-exchange-app-installer-automatic-localization.html

## 文章内容

by Fenton Webb
When you submit your apps to Autodesk Exchange you get back an MSI which installs you app, super cool!
But how does the installer deal with localization…
There are a three parts to Exchange App localization:
The Autoloader PackageContents.xml localization
The Exchange App installer localization
Your App localization
The Autoloader PackageContents.xml Localization  
The installer that you get from us here at Autodesk is automatically localized by an internal tool. This tool uses the localized settings found in the PackageContents.xml to understand the localization requirements needed for the installer.
Each localizable attribute in the PackageContents.xml can have a localized value simply by suffixing the locale id onto the end of the attribute name. e.g.  
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" ProductType="Application" Name="DWG MgdDBG" AppVersion="1.0.0" Author="Fenton Webb" Icon="./Contents/Resources/resource/Inspector.jpg" AppNameSpace="adn.exchange.autodesk.com" OnlineDocumentation=" www.autodesk.com" HelpFile="./Contents/Resources/helpfile.html" ProductCode="{DB35F952-289A-4453-A46D-B424A6FCFDFB}" UpgradeCode="{E5B78003-2D7B-490F-B947-65D804392151}" SupportedLocales="Enu|Ptb|Deu|Esp|Fra|Ita" FriendlyVersion="1.0.0" Description="Debugging tools for AutoCAD - MgdDBG" DescriptionDeu="Das Desription" DescriptionEsp="El Descriptiano" DescriptionFra="La Description">
  This mechanism is described in the Autoloader White paper found here http://adndevblog.typepad.com/autocad/2013/01/autodesk-autoloader-white-paper.html
  The Exchange App Installer Localization  
As mentioned before, the installer that you get from us here at Autodesk is automatically localized by an internal tool. Currently, the Exchange App installer MSI’s supports 15 languages automatically. When the internal tool reads the PackageContents.xml, it recognises each and every localized attribute name and processes the localization automatically into the installer. When the locale of the machine is, say, German, when the App installer runs, it automatically transforms itself swapping out the default English words to the German localized words so that the German version is displayed.
Obviously, this will save you many hours or time and money, and also provide your non-English users a much better user experience if you spend the time setting up your PackageContents.xml to suit. 
Your App localization Support  
Apps should utilize standard localization features of Microsoft technology, the use of localized string resources with locale specific resource switching depending on the host product (AutoCAD, Revit, etc) locale setting is recommended.
Here are the Exchange Store currently supported locales:
<Languages>
  <!-- see http://www.science.co.il/language/locale-codes.asp -->
  <Language>
    <Name>Enu</Name>
    <LocaleId>1033</LocaleId>
  </Language>
  <Language>
    <Name>Deu</Name>
    <LocaleId>1031</LocaleId>
  </Language>
  <Language>
    <Name>Esp</Name>
    <LocaleId>1034</LocaleId>
  </Language>
  <Language>
    <Name>Fra</Name>
    <LocaleId>1036</LocaleId>
  </Language>
  <Language>
    <Name>Ita</Name>
    <LocaleId>1040</LocaleId>
  </Language>
  <Language>
    <Name>Plk</Name>
    <LocaleId>1045</LocaleId>
  </Language>
  <Language>
    <Name>Ptb</Name>
    <LocaleId>1046</LocaleId>
  </Language>
  <Language>
    <Name>Chs</Name>
    <LocaleId>2052</LocaleId>
  </Language>
  <Language>
    <Name>Cht</Name>
    <LocaleId>1028</LocaleId>
  </Language>
  <Language>
    <Name>Csy</Name>
    <LocaleId>1029</LocaleId>
  </Language>
  <Language>
    <Name>Hun</Name>
    <LocaleId>1038</LocaleId>
  </Language>
  <Language>
    <Name>Jpn</Name>
    <LocaleId>1041</LocaleId>
  </Language>
  <Language>
    <Name>Kor</Name>
    <LocaleId>1042</LocaleId>
  </Language>
  <Language>
    <Name>Rus</Name>
    <LocaleId>1049</LocaleId>
  </Language>
</Languages>

