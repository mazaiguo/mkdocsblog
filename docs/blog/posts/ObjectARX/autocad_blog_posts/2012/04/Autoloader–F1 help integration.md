---
title: "Autoloader–F1 help integration"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Dimension
  - Migration
  - Plugin
  - Unicode
description: "Another new Autoloader feature introduced in AutoCAD 2013 – an easy way to link your commands to your helpfile. I’m going to take the AutoCAD 2013 ..."
author: Autodesk
---
# Autoloader–F1 help integration

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autoloaderf1-help-integration.html

## 文章内容

By Stephen Preston
Another new Autoloader feature introduced in AutoCAD 2013 – an easy way to link your commands to your helpfile. I’m going to take the AutoCAD 2013 version of my DimensionPatrol Plugin of the Month which is posted to the Exchange store. (You can download that for free if you want to study a working example).
Here is the XML from that bundle (excluding the AutoCAD 2012 Components section):
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" ProductType="Application" Name="DimensionPatrol" AppVersion="1.1.1" Description="ADN Plugin of the Month: DimensionPatrol" Author="Stephen Preston" Icon="./Contents/Resources/DimensionPatrol.bmp" AppNameSpace="appstore.exchange.autodesk.com" OnlineDocumentation="http://labs.autodesk.com/utilities/ADN_Plugins" HelpFile="./Contents/Resources/ADNDimensionPatrolHelp.htm" ProductCode="{0A5FDE70-BDE5-4906-9663-D877B8C72EBE}" UpgradeCode="{EC5625DD-AB28-494A-8AA8-E188C2D3F899}">
  <CompanyDetails Name="Autodesk" Phone=" " Url="http://labs.autodesk.com/utilities/ADN_Plugins" Email="labs.plugins@autodesk.com" />
  <Components>
    <RuntimeRequirements SupportPath="./Contents/Resources" OS="Win32|Win64" Platform="AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="ADNPlugin-DimensionPatrol" Version="1.1.1" ModuleName="./Contents/Windows/2013/ADNPlugin-DimensionPatrol.dll" AppDescription="ADN Plugin of the Month: DimensionPatrol" LoadOnCommandInvocation="True">
      <Commands GroupName="ADNPLUGINS">
        <Command Local="DIMPATROL" Global="DIMPATROL" />
        <Command Local="DIMPATROLCOLOR" Global="DIMPATROLCOLOR" />
      </Commands>
    </ComponentEntry>
    <ComponentEntry AppName="ADNPlugin-DimensionPatrol" Version="1.1.1" ModuleName="./Contents/Resources/DimensionPatrol.cuix" AppDescription="ADN Plugin of the Month: DimensionPatrol" />
  </Components>
</ApplicationPackage>
All you have to do in your own PackageContents.xml is to include the HelpFile parameter in the ApplicationPackage element, and define some commands inside one or more of my ComponentEntry elements. Now when you hit F1 while the command is running (or when hovering over a ribbon button that invokes your command), AutoCAD will launch your helpfile.
[Note: Its not strictly necessary to include the Commands element if you don’t set your plug-in to ‘LoadOnCommandInvocation’, but it is required if you want the F1 help integration. Its good practice to document your commands in the XML anyway].
As an added bonus, you can also include a HelpTopic element for each Command to display the correct section of your helpfile, like this:
        <Command Local="DIMPATROL" Global="DIMPATROL" HelpTopic="CommandTopic1"/>
        <Command Local="DIMPATROLCOLOR" Global="DIMPATROLCOLOR" HelpTopic="CommandTopic2"/>
Without your HelpTopic defined, AutoCAD will simply display
./Contents/Resources/ADNDimensionPatrolHelp.htm
in your browser. With the HelpTopics defined, it will display
./Contents/Resources/ADNDimensionPatrolHelp.htm#CommandTopic1
or
./Contents/Resources/ADNDimensionPatrolHelp.htm#CommandTopic2
depending on the command for which you’re requesting F1 help.

## 评论

**内容**: Jimmy Bergmark - JTB World said...
The documentation online now specify the attribute HelpFile like Helpfile and when 'f' is in lower case F1 will not work.
The HelpTopic attribute is not documented well either. It just says: "Help topic to open when the command is active and F1 is pressed."
AppName attribute for ComponentEntry is mandatory for cuix files but is not documented. If not used you get an error like: Autoloader is missing an appName for module name ./Contents/whatever.cuix
Is really Version="1.1.1" needed for ComponentEntry with the cuix file? If so it is not in the documentation right now.
Reply
06/12/2012 at 10:27 PM

---
**内容**: Madhukar Moogala said...
Hi Jimmy,
Correct. HelpFile has an uppercase 'F'. And AppName is required for a ComponentEntry.
But Version is optional for a ComponentEntry.
Cheers,
Stephen
Reply
06/13/2012 at 06:53 AM

---
**内容**: TimStalin said...
Is there a secret to getting the HelpTopic working? The HelpFile displays as expected but the #suffix is not appended to the address string.
Hyperlinks in AutoCAD have never respected the #suffix (at least for our office set up), I assume that this is probably related.
Reply
08/28/2012 at 03:02 PM

---
