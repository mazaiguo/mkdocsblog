---
title: "Running OEMMAKEWIZARD from Command Line"
date: 2018-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "This is small batch script may be useful for OEM Developers."
author: Autodesk
---
# Running OEMMAKEWIZARD from Command Line

发布日期: 2018-05-01

原始链接: https://adndevblog.typepad.com/autocad/2018/05/running-oemmakewizard-from-command-line.html

## 文章内容

By Madhukar Moogala
This is small batch script may be useful for OEM Developers.
Once you have created your project, you can run the AutoCAD OEM Make Wizard from the command line to automate building your product. In this mode, you can use any of the build options available on the Build Your Product page of the AutoCAD OEM Make Wizard. Enter the following command to display a Help screen describing the command-line options for the AutoCAD OEM Make Wizard:
oemmakewizard /? 
Build Options:
Path Options  
   /PA:  Specifies the path for AutoCAD OEM location  
   /PB:  Specifies the path for bitmap location  
Import Options  
   /IC:  Specifies a file for enabling\disabling AutoCAD commands  
   /IAS:  Specifies a file for adding your commands  
   /IRS:  Specifies a file that allows you to remove user specified commands or setvars  
Build Options  
   /BALL  Builds all (does not include the files executed by /BT command)  
   /BA  Binds ObjectARX/Core ObjectARX applications  
   /BB  Binds managed applications  
   /BBA  Binds managed ObjectARX applications  
   /BL  Binds AutoLISP applications  
   /BD  Binds DLL modules  
   /BV  Bind DVB macros  
   /BC  Copies files  
   /BT  Builds type libraries and registry files  
   /BT+  Registers associated registry files  
   /BI  Change icons  
   /BR  Rebuilds resources  
   /BR+  Rebuilds resources and uses settings with AutoCAD OEM  
   /BR-  Rebuilds resources, but does not bind the DLLs  
   /STOP  Interrupts batch mode when errors are encountered  
   /?  Displays the Help screen for all command options
@echo off
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::
::: Created by Madhukar Moogala
::: Autodesk Devtech
::: 
:::
::: This batch program builds an AutoCAD OEM Product, TestCAD. This product is used 
::: as the host application for the OEM Build and Diagnositics.
:::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
::"=================================================================================
:: @see MIT License
:: =================================================================================
::
set ProjectName=TestCAD
set BuildDir=C:\users\default\Documents\AutoCAD OEM 2019\build
set ProjectDir=C:\users\default\Documents\AUTOCAD OEM 2019\projects\%ProjectName%
set EXEDIR=c:\program files\autodesk\autocad oem 2019 - english
set ACSUP=c:\program files\autodesk\autocad oem 2019 - english\Support
set ACTOOLKIT=C:\Users\Default\Documents\AutoCAD OEM 2019\Projects\TestCAD\Toolkit
set PRODUCTNAME=TestWorks
set PRODNAME=TestCAD
set ACBMP=c:\program files\autodesk\autocad oem 2019 - english\Toolkit\Bitmaps;c:\program files\autodesk\autocad oem 2019 - english\Toolkit
set LOCALROOT=C:\Users\moogalm\AppData\Local\Autodesk\AutoCAD OEM 2019\R23\enu\
set ROAMINGROOT=C:\Users\moogalm\AppData\Roaming\Autodesk\AutoCAD OEM 2019\R23\enu\
::Setting directories sto PATH will Oemwizard to find and execute properly
set PATH=%PATH%;C:\Users\Default\Documents\AutoCAD OEM 2019\Projects\TestCAD\Toolkit;c:\program files\autodesk\autocad oem 2019 - english;c:\program files\autodesk\autocad oem 2019 - english\Toolkit;C:\Users\Default\Documents\AutoCAD OEM 2019\build\TestCAD\
:: Please enter your keycode, DDFiveDigitsofSerialNumberMM
set KeyCode=DDxxxxxMM
set LogProfile="%ACTOOLKIT%\OemStampxml.log"
set ErrProfile="%ACTOOLKIT%\OemStampxml.err"
cd "%ProjectDir%"
if exist %LogProfile% (
del %LogProfile% 
echo %LogProfile% deleted)
if exist %ErrProfile% (
del %LogProfile% 
echo %ErrProfile% deleted
)
"%EXEDIR%\Toolkit\oemmakewizard.exe" %ProjectName% %KeyCode% /BALL /BT /BR /PA:"%EXEDIR%"
view raw
Build-AutoCADOem.bat hosted with ❤ by GitHub

## 评论

**内容**: Jim Massengale said...
I've been running the command line for Make Wizard for a while but now I have (2) entries to a same PRODUCT but from different code streams Product 2018 and Product 2019 but still building from the same OEM engine 2018. I have PROD.xml our 2018 Code and PROD2019.xml our 2019 code. In the IDE I can open the year specific and edit them, but the issue seems to be that the AOEMREG.exe is looking for a PROD.XML not the PROD2019.XML.

Is it required to have the project files be PROD.xml since the registry doesn't seem to point to the specific xml file except for the key.

Help?
Reply
09/07/2018 at 09:25 AM

---
**内容**: Madhukar Moogala said...
Hi,
Can you please try passing full qualified path of your program .xml, i.e filepath +filename.
call "%PROGRAMFILES(x86)%\Microsoft Visual Studio\2017\Professional\Common7\Tools\VsDevCmd.bat"
set ProjectName=TestCAD
set BuildDir=C:\users\default\Documents\AutoCAD OEM 2019\build
set ProjectDir=C:\users\default\Documents\AUTOCAD OEM 2019\projects\%ProjectName%
set KeyCode=09abcde05
set AOEMDIR=C:\Program Files\Autodesk\AutoCAD OEM 2019 - English
@echo on
 
goto build
:build
if not exist "%ProjectDir%" mkdir "%ProjectDir%"
if not exist "%BuildDir%\%ProjectName%" mkdir "%BuildDir%\%ProjectName%"
"%AOEMDIR%\toolkit\oemmakewizard.exe" "%ProjectDir%\%ProjectName%.xml" %KeyCode% /BALL /BT /BR
:eof
                
            
Reply
09/10/2018 at 01:31 AM

---
**内容**: Loic Jourdan said in reply to Madhukar Moogala...
In case of someone is still facing the issue, there's an important line missing in the Madhukar initial post (which has been added to his second post):
call "%PROGRAMFILES(x86)%\Microsoft Visual Studio\2017\Professional\Common7\Tools\VsDevCmd.bat"
I've experienced that missing this line was causing oemmakewizard complaining about invalid project name.
Thanks Madhukar for your help, despite this little error, you really saved me hours.
Reply
02/27/2019 at 11:50 PM

---
