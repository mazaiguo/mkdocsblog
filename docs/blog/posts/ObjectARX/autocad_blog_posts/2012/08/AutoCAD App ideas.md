---
title: "AutoCAD App ideas"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "The Autodesk Exchange Apps store is going great guns now, averaging over 9000 unique visitors a week (and rising). We’re also seeing an increasing ..."
author: Autodesk
---
# AutoCAD App ideas

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/autocad-app-ideas.html

## 文章内容

By Stephen Preston
The Autodesk Exchange Apps store is going great guns now, averaging over 9000 unique visitors a week (and rising). We’re also seeing an increasing variety of apps available on the store. Nevertheless, our store manager is keen for more, more more …
Here is a list of some of the suggestions he’s come up with for app ideas:
Simple Increment Tool: A simple tool which would increment objects tags or wherever incremental values are needed. This was a favorite suggestion from a recent Facebook survey.
Google Doc Spreadsheet Integration: An app which would allow viewing/editing of an AutoCAD table in Google documents (spreadsheet). This would open up many collaboration opportunities.
Stretch Reminder: A simple app which would remind a user to take a break from time to time to stretch and exercise.
.NET Macro Recorder: A utility which would convert recorded macros to .NET code.
Music Feed: Plug-in which could allow a user to manage music without leaving their Autodesk project through integration with one of the many streaming music services. (Ed: And automatically choose tracks to suit your mood depending on what AutoCAD commands you’re using .)
Custom Help: A tool to share and compile commonly used commands/sysvar in a small office or team. This would replace CAD ‘cheat sheets’ and serve as an in-CAD wiki.
Sketching/Designing in program: Simple sketching tools within AutoCAD, perhaps integrated with SketchBook Designer.
Preview Handler for Outlook: Handler which would allow previews of DWG/DWF files attached to emails.
But I’m sure that you, dear reader, can come up with some even better ideas (and probably already have).
Wait … No … Don’t tell me!
Go ahead and submit your finished app to the Exchange store. It could be the start of a beautiful friendship . And if you’d like to check out more ideas or suggest some of your own, take a look at our Google Moderator group.

## 评论

**内容**: Khoa Ho said...
Hi Stephen,
Can you have a tutorial showing how to create a msi installation file using Autodesk Plug-in Installer. Thank you.
Reply
08/15/2012 at 05:26 PM

---
**内容**: Madhukar Moogala said...
Hi Khoa,
For Exchange store apps, we recommend you use the Autoloader mechanism I've described in earlier posts. If you do that, then we will create the installer for you. (Or if you're not posting to the store, then you can create a simple MSI using VS that just copies your bundle to %appdata%\Autodesk\ApplicationPlugins or |programdata%\Autodesk\ApplicationPlugins. No registry access is required.
For a non-Autoloader installer, you have a lot of work (which is why we created Autloader). I suggest you watch this old webcast - http://download.autodesk.com/media/adn/AutoCAD-Creating_an_Application_Installer.zip. (See the whole webcast archive at http://www.adskconsulting.com/adn/cs/api_course_webcast_archive.php).
Reply
08/16/2012 at 11:16 AM

---
**内容**: Khoa Ho said...
Thanks Stephen, I now understand why many apps on the Exchange Store have the same installation interface, as Autodesk has the Autoloader mechanism helping to create the installer. Otherwise developers have to make their own MSI packages and write to Windows registry info of the loader files. Phew, LOTS of good stuffs on the DevBlog to read recently! Thank you.
Reply
08/17/2012 at 11:54 AM

---
