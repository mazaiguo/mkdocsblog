---
title: "Reset UCS to World for multiple drawings"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - UCS
description: "In this blog post we will look at a simple way to reset the UCS to World for large number of drawings by batch processing drawings from a folder us..."
author: Autodesk
---
# Reset UCS to World for multiple drawings

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/reset-ucs-to-world-for-multiple-drawings.html

## 文章内容

By Balaji Ramamoorthy
In this blog post we will look at a simple way to reset the UCS to World for large number of drawings by batch processing drawings from a folder using AccoreConsole.exe
Here is the main batch file to iterate drawings in a folder :
 ::Make changes to these parameters as per requirement
 SET ACCOREEXEPATH="C:\\Program Files\\Autodesk\\AutoCAD 2015\\accoreconsole.exe" 
 SET DWGINDIR="C:\\Temp\\IN" 
 echo off
 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
 IF NOT EXIST %DWGINDIR% MD %DWGINDIR%
 cls
 SET UCSRESETBATFILEPATH="%~dp0" 
 set UCSRESETBATFILEPATH=%UCSRESETBATFILEPATH:~1,-1%ResetUCS.bat
 for  /f "delims="  %%a IN ( ) do  call "%UCSRESETBATFILEPATH%"  %ACCOREEXEPATH% %DWGINDIR% "%%a" 
 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
 :End
  Here is the batch file that invokes AccoreConsole.exe :
 SET ACCOREEXEPATH=%1
 IF NOT EXIST "%ACCOREEXEPATH%"  goto  ACCOREEXENOTFOUND
 SET DWGINPATH=%2
 SET DWGFILENAME=%3
 set DWGFILENAME=%DWGFILENAME:~1,-1%
 set DWGINPATH=%DWGINPATH:~1,-1%\\%DWGFILENAME%
 :: Get the script file path
 SET SCRIPTFILEPATH="%~dp0" 
 set SCRIPTFILEPATH=%SCRIPTFILEPATH:~1,-1%ResetUCS.scr
 ::Reset the UCS to World
 %ACCOREEXEPATH% /i "%DWGINPATH%"  /s "%SCRIPTFILEPATH%"  /l en-US
 goto  END
 :ACCOREEXENOTFOUND
 echo %ACCOREEXEPATH%
 echo "Accoreconsole.exe path is incorrect." 
 goto  END
 :DRAWINGNOTFOUND
 echo %DWGINPATH%
 echo "Drawing file not found." 
 goto  END
 :END
  Here is the AutoCAD Script file to reset the UCS which is only a few lines :
;Script begins here
UCS
SAVE
;Script ends here
Here are files for download. To try this, copy all the files to C:\Temp and place the drawings that you want to process under C:\Temp\IN folder
Download ResetUCSToWorld

