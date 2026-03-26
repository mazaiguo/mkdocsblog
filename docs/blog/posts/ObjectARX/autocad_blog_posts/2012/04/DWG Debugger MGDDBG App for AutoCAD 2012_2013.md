---
title: "DWG Debugger MGDDBG App for AutoCAD 2012/2013"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Migration
  - Unicode
description: "Following on from my previous post DWG Inspector for AutoCAD 2012/2013, here is the MgdDbg tool migrated to 2012 and 2013 bundled as an Exchange Ap..."
author: Autodesk
---
# DWG Debugger MGDDBG App for AutoCAD 2012/2013

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/dwg-debugger-mgddbg-app-for-autocad-20122013.html

## 文章内容

by Fenton Webb
Following on from my previous post DWG Inspector for AutoCAD 2012/2013, here is the MgdDbg tool migrated to 2012 and 2013 bundled as an Exchange App – you can download it here
One thing to note is that there are commands included in the app, however, because this app has startup code (it creates context menu entries) I have omitted all ComponentEntry initialization options, so LoadOnStartup is assumed. (I have not used the LoadOnCommandInvocation attribute)
  Here’s the PackageContents.xml found in the base of the .bundle folder, in case you are interested:
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="AutoCAD" ProductType="Application" Name="DWG MgdDBG" AppVersion="1.0.0" Description="Debugging tools for AutoCAD - MgdDBG" Author="Fenton Webb" Icon="./Contents/Resources/resource/Inspector.jpg" AppNameSpace="adn.exchange.autodesk.com" OnlineDocumentation=" www.autodesk.com" HelpFile="./Contents/Resources/helpfile.html" ProductCode="{DB35F952-289A-4453-A46D-B424A6FCFDFB}" UpgradeCode="{E5B78003-2D7B-490F-B947-65D804392151}" SupportedLocales="Enu|Ptb|Deu|Esp|Fra|Ita">
  <CompanyDetails Name="Autodesk" Phone=" " Url=" www.autodesk.com" Email=" adn.autodesk.com" />
  <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD|AutoCAD*" SeriesMin="R18.2" SeriesMax="R19.0" />
  <Components Description="AutoCAD 2012">
    <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD*|AutoCAD" SeriesMin="R18.2" SeriesMax="R18.2" />
    <ComponentEntry AppName="DWGMgdDBG" Version="1.0.0" ModuleName="./Contents/Resources/DWGMgdDbgSource/bin/Debug2012/MgdDbg.dll" AppDescription="Debugging tools for AutoCAD - MgdDBG" />
  </Components>
  <Components Description="AutoCAD 2013">
    <RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD*|AutoCAD" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="DWGMgdDBG" Version="1.0.0" ModuleName="./Contents/Resources/DWGMgdDbgSource/bin/Debug2013/MgdDbg.dll" AppDescription="Debugging tools for AutoCAD - MgdDBG" />
  </Components>
</ApplicationPackage>

## 评论

**内容**: Kerry Brown said...

Hello Fenton
Can you please point us to some documentation regarding changing this to 'LoadOnCommandInvocation'
Regards,
Kerry
Reply
04/24/2012 at 08:52 PM

---
**内容**: Kerry Brown said...

Fenton, Stephen ;
Regarding LoadOnCommandInvocation
I've posted at theSwamp because this site and the Discussion Group don't like XML in comments.
http://www.theswamp.org/index.php?topic=41576.0
Regards
Kerry

Reply
04/25/2012 at 05:41 AM

---
**内容**: Madhukar Moogala said...
That's right Kerry. You add the LoadOnCommandInvocation parameter and the Commands element to PackageContents.xml.
MgdDbg registers a context menu when its loaded (which I always use instead of typing the commands). If you want to always have that menu available (as I do) then using LoadOnStartup (the default) is the way to go. I'm sure that's why Fenton set it so - for our work we can almost guarantee that we'll want to use MdgDbg every time we start up AutoCAD :-).
(The XML in comment thing is a bit annoying :-( ).
Reply
04/25/2012 at 08:49 AM

---
**内容**: Kerry Brown said...
Thanks Stephan
Any ideas why the LocalName is not being recognised ??

Regards
Reply
04/25/2012 at 12:45 PM

---
**内容**: Fenton Webb said...
Might need an underscore...
Reply
04/25/2012 at 01:45 PM

---
**内容**: Fenton Webb said...
...at the front of the GlobalName
Reply
04/25/2012 at 07:33 PM

---
**内容**: Fenton Webb said...
Also, localized LocalName attributes are defined by suffixing LocalName with the corresponding NLS 3 letter language abbreviation, first char upper case, the second and third in lowercase... e.g.
LocalName="Neutral/EnglishCommand"
LocalNameEsp="SpanishCommand"
LocalNameFra="FrenchCommand"
all documented here http://www.microsoft.com/resources/msdn/goglobal/default.mspx
Reply
04/25/2012 at 07:47 PM

---
**内容**: Kerry Brown said...

I think I've found the issue.
The Group name and Local name are not actually used in the CommandMethodAttribute Constructor .. so any usage of them in the XML is redundant.
I've updated the post at theSwamp and attached my revised PackageContents.xml
Thanks for the help.
Regards
Kerry
Reply
04/26/2012 at 03:43 AM

---
**内容**: Madhukar Moogala said...
That's a relief Kerry. Was scared you'd found a bug there for a minute. :-)
Reply
04/26/2012 at 08:06 AM

---
**内容**: Rudolf Honke said...
Dear Fenton,
when starting the help after installing the tool, the website title is "AutoCAD Exchange - Minesweeper Help".
This affects both the MGDDBG and the Inspector installation.
Best regards,
Rudolf
Reply
06/22/2012 at 08:44 AM

---
**内容**: Madhukar Moogala said in reply to Rudolf Honke...
Lol. I'm so proud that Fenton is reusing *my* code - even if it is just a HTML page template :-P.
(Sorry Fents - Couldn't resist that :-D)
Reply
06/22/2012 at 11:14 AM

---
**内容**: BlackBox said...
Hi guys,
Has anyone tried using 'Snoop Entities...' on an MLeader?
Using MgdDbg in Civil 3D 2012 (Win7, 64-bit), ContentType.MTextContent, nor ContentType.BlockContent, etc. seem to make a difference, as all ContentTypes that I've tested seem to result in an unhandled 'eInvalidContext' exception, and an empty 'Selected Entities' modal form....
[code]
************** Exception Text **************
Autodesk.AutoCAD.Runtime.Exception: eInvalidContext
at Autodesk.AutoCAD.DatabaseServices.MLeader.get_BlockPosition()
at MgdDbg.Snoop.CollectorExts.Entity.Stream(ArrayList data, MLeader mleader) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\CollectorExts\Entity.cs:line 897
at MgdDbg.Snoop.CollectorExts.Entity.Stream(ArrayList data, Entity ent) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\CollectorExts\Entity.cs:line 255
at MgdDbg.Snoop.CollectorExts.Entity.CollectEvent(Object sender, CollectorEventArgs e) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\CollectorExts\Entity.cs:line 59
at MgdDbg.Snoop.Collectors.Collector.CollectorExt.Invoke(Object sender, CollectorEventArgs e)
at MgdDbg.Snoop.Collectors.Collector.FireEvent_CollectExt(Object objToSnoop) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\Collectors\Collector.cs:line 63
at MgdDbg.Snoop.Collectors.Objects.Collect(Object obj) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\Collectors\Objects.cs:line 52
at MgdDbg.Snoop.Forms.DBObjects.TreeNodeSelected(Object sender, TreeViewEventArgs e) in C:\Temp\test\2010Migration\DWG MgdDbg Source\Snoop\Forms\DBObjects.cs:line 452
at System.Windows.Forms.TreeView.TvnSelected(NMTREEVIEW* nmtv)
at System.Windows.Forms.TreeView.WmNotify(Message& m)
at System.Windows.Forms.TreeView.WndProc(Message& m)
at System.Windows.Forms.NativeWindow.Callback(IntPtr hWnd, Int32 msg, IntPtr wparam, IntPtr lparam)
[/code]
... Is this something you've encountered before? If so, is there an updated version of MgdDbg perhaps (I have used this one for +/- 1 year)?
Cheers
Reply
09/09/2013 at 10:58 AM

---
**内容**: Fenton Webb said...
Hey Blackbox!
Sorry, I've only tested it under raw AutoCAD. The source code is in the bundle, feel free to find out what the problem is...!
Reply
09/09/2013 at 11:11 AM

---
**内容**: BlackBox said in reply to Fenton Webb...
Hi Fenton, always a pleasure to speak with you.
While vanilla AutoCAD, and Civil 3D are different builds, that shouldn't affect how AutoCAD would handle this particular situation, methinks... Especially as we're dealing with an MLeader typed Object.
However, at the risk of Civil 3D being the cause, I've just tested in vanilla AutoCAD, and the eInvalidContext exception persists.
Not sure I'm the right person to debug such a robust plug-in, but perhaps I'll attempt your challenge after portathon.
Cheers
Reply
09/09/2013 at 02:12 PM

---
**内容**: BlackBox said...
Another issue when using Snoop Database, after applying a VP Color to Layer "0", digging into the LayerTableRecord's Extension Dictionary's XRecord:
DbMisc.cs(678)
DbMisc.cs(59)
Collector.cs(63)
Object.cs(365)
... More not shown, as this appears in a modal form titled:
"Assertion Failed: Abort=Quit, Retry=Debug, Ignore=Continue"
... Where "Retry" results in a fatal error, and locked up all AutoCAD application windows which were unable to be ended via Task Manager... I had to actually terminate acad.exe in Processes tab.
Reply
09/11/2013 at 09:59 AM

---
**内容**: Chris Fugitt said...
It appears the programmer of the Civil 3D Profile inserted an exception that doesn't follow the pattern of other objects that causes an unhandled exception when selecting a Civil 3D profile. The fix is to look for the additional exception in the Entity.cs file:
// the following is only valid in some cases
try {
data.Add(new Snoop.Data.Object("Spline", crv.Spline));
}
catch (Autodesk.AutoCAD.Runtime.Exception e) {
if (e.ErrorStatus == Autodesk.AutoCAD.Runtime.ErrorStatus.NotApplicable)
data.Add(new Snoop.Data.Exception("Spline", e));
else if (e.ErrorStatus == Autodesk.AutoCAD.Runtime.ErrorStatus.NotImplementedYet)
data.Add(new Snoop.Data.Exception("Spline", e));
else
throw e;
}
Reply
12/28/2013 at 09:51 AM

---
**内容**: Mike Hutchinson said...
Has this been updated for AutoCAD 2014... will is show 3rd party software database 'stuff'?
Reply
02/12/2014 at 09:22 AM

---
**内容**: Peter2 said...
Hi
is there a current release for Acad versions 2014 / 2015 / 2016?
regards
Peter
Reply
04/13/2015 at 02:24 AM

---
**内容**: BlackBox said...
Who at Autodesk is responsible for maintaining this, and where is MGDDBG for 2016?
Gile's provided an update for 2015 version here, which seems to work in 2016 so far:
http://forums.augi.com/showthread.php?156005-MgdDbg-for-AutoCAD-2015&p=1267715&viewfull=1#post1267715
Reply
01/04/2016 at 07:13 AM

---
