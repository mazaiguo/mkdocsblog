---
title: "Autoloader–Tool Palette support"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
  - Plugin
description: "Another feature added to Autoloader in AutoCAD 2013 is support for adding Toolpalette support paths. Here’s how …"
author: Autodesk
---
# Autoloader–Tool Palette support

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autoloadertool-palette-support.html

## 文章内容

By Stephen Preston
Another feature added to Autoloader in AutoCAD 2013 is support for adding Toolpalette support paths. Here’s how …
Create your Tool palette
Start the TOOLPALETTES command in AutoCAD.
Right click on the tool palettes control bar, and select New Palette.
Give the new Palette a name and drag your content onto it. Here’s one I created called ‘Stephen’s Palette’.
Copy the Tool palette to your .bundle
Check the Tool Palettes File Locations folder on your OPTIONS dialog –> Files tab. The default will be something like %appdata%\Roaming\Autodesk\AutoCAD 2013 - English\R19.0\enu\Support\ToolPalette\Palettes.
Open that folder and look for the tool palette you just created.The file name will be <PaletteName>_<GUID>.atc, so the one I just created is called ‘Stephen's Palette_10E78C8E-A3D5-40DF-A284-2A61AC4E0E90.atc’
Move the ATC file into your bundle and delete palette from your Tool palettes window by right clicking on the control bar again. You might as well close down AutoCAD too, so it doesn’t try to load your bundle while you’re editing it.
Add the ToolPalettePath to PackageContents.xml
Your XML will look something like this – the ToolPalettePath highlighted in bold is the location within the bundle of the ATC file(s):
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" Name="ToolPaletteTest" Description="Sample showing Tool Palette filepath support" AppVersion="1.0.0" ProductType="Application" AppNameSpace="appstore.exchange.autodesk.com" Author="Stephen Preston" ProductCode="{52C2A8B7-A32D-4369-AE6C-76FEC5531243}" UpgradeCode="{A13F2CDA-43FE-41E4-BD0C-558AD7973E86}">
  <CompanyDetails Name="ADN" Email="AutoCAD.DevBlog@autodesk.com" />
  <Components>
    <RuntimeRequirements OS="Win64|Win32" Platform="AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.0" ToolPalettePath="./Contents/"/>
  </Components>
</ApplicationPackage>
Test
Move your bundle to %appdata%\Autodesk\ApplicationPlugins.
Launch AutoCAD. Your Toolpalette is now loaded:
Go to the options dialog and your search path has been added:

## 评论

**内容**: Wiebe van der Worp said...
Hello Stephen
An interesting article. Greatly appreciated. However it returns some question marks, some answers and information for other readers...
After following your instructions I managed to get it working for blocks. I tested a library with 185 Dutch traffic signs and dragged them from explorer to a new palette, copied the files, closed the palette, et cetera as you described.
So I thought it would be smart to create a spreadsheet that constructs the xml needed for a new palette. Does not work and I haven't the faintest idea why: name_uuid.atc with bit-wise exact same syntax fails. Uuids generated with $ for i in {1..400}; do uuidgen -r; done (with Linux or Cygwin). Noticed that uuid in file name equals xml entry ItemID of Palette. Searched with regedit for both name and uuid in name_uuid.atc – without result. Can you clarify? Palette shows up in AutoCAD but dragging a button gives: "Unable to execute tool. Possible causes are: The tool is not registered properly. Check your installation. The tool is from another application and is incompatible with the current application." It drove me nuts. Where is it registered? It would really be helpful to be able to generate large palettes outside AutoCAD and simply dump them in the name.bundle\contents folder.
One thing I noticed is that a palette file assumes there is a folder "Images" under the palette holding folder. So copying the .atc files isn't enough, I copied the images too, not sure if they are needed in an app distribution. Are they? Off topic: What a pity svg's are not supported.
Another obstacle is about file names. The generated xml / atc file contains absolute paths – like C:\ProgramData\Autodesk\ApplicationPlugins\a.bundle\contents\lib\trafficsigns\_colors.dwg. Needless to say this is a problem when distributing an app into the wild, in this case the app lives under %programdata% but it could also be under %appdata%. PackageContents.xml contains a valid entry ToolPalettePath="./contents/". Apparently it is possible to cut of the prefix "C:\ProgramData\Autodesk\ApplicationPlugins\a.bundle\contents\" for all entries in the .atc file – leaving "lib\trafficsigns\blockname.dwg" – and keep a functional palette. So my conclusion is that locations relative to the app's ToolPalettePath will be valid – very handy and I hope my conclusion is right.
Best regards, Wiebe van der Worp
Reply
11/25/2014 at 02:46 PM

---
**内容**: Håkan said...
Long time have I Googled for the solution for distributing custom made Tool Palettes and changing ToolPalettePath. I have only found LISP-solutions until I found this. This was a very simple way to do it. I load a .bundle-file that points to a Tool Palette located on our server. Then I´m able to update the ToolPalette and my collegues gets the latest one on every AutoCAD startup. All links are relative. Many thanks!
Reply
06/15/2016 at 09:07 AM

---
