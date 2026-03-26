---
title: "OEM Troubleshooting: Unable to find main dictionary, Could Not Start Speller"
date: 2016-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "Q. When I run my app and hit any key at AutoCAD command line, I get a AutoCAD dialog saying:"
author: Autodesk
---
# OEM Troubleshooting: Unable to find main dictionary, Could Not Start Speller

发布日期: 2016-03-01

原始链接: https://adndevblog.typepad.com/autocad/2016/03/oem-troubleshooting-unable-to-find-main-dictionary-could-not-start-speller.html

## 文章内容

By Madhukar Moogala
  Q. When I run my app and hit any key at AutoCAD command line, I get a AutoCAD dialog saying:
"Unable to find main dictionary. Could not start speller"
AutoCAD command line then reports: "Can't find speller module: AcSpellEng.dll"
What am I supposed to do in the OEM wizard to get this going?
A.
It seems that Copying and Patching Spell files has not taken place while building your OEM application, this is because "_Spell" command has not enabled in your commands page.
OEM Wizard while creating stamp.bat file  wizard initiates stamping for each enabled command such that all dependencies are copied to your project folder [.\AutoCAD OEM XXXX- English\Projects\<OEMAPP>\Toolkit]
XXXX stands for version for e.g. 2016.
So enable full support for "'_Spell'", after building application, open <oemapp>stamp.bat and find for :SPELLDONE, you 'll find stamping of AcSpell.dll takes place.

## 评论

**内容**: mamatha981@yahoo.com said...
Hi Madhukar,
I am working on AUTOLISP, I need to run the routine in while loop. The while loop should start with keyboard input and stop with enter. Do you know how to do it, please let me know.
Thanks
Reply
05/01/2017 at 08:19 AM

---
