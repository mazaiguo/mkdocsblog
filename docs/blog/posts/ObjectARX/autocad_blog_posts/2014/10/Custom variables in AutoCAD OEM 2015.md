---
title: "Custom variables in AutoCAD OEM 2015"
date: 2014-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
  - Plugin
description: "One of the enhancements in AutoCAD OEM 2015 is the support for custom system variables."
author: Autodesk
---
# Custom variables in AutoCAD OEM 2015

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/custom-variables-in-autocad-oem-2015.html

## 文章内容

By Balaji Ramamoorthy
One of the enhancements in AutoCAD OEM 2015 is the support for custom system variables. 
To create a custom system variable, the following registry key is to be created. Here is a sample reg file for adding a custom system variable named "LevelOfDetail" for a OEM product that I named GOCAD.
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\GOCAD\R20\GOCAD-E001:409\Variables\LevelOfDetail]
"StorageType"=dword:00000002
"LowerBound"=dword:00000000
"UpperBound"=dword:00000064
"PrimaryType"=dword:0000138b
@="3"
For the custom variable to be accessible in your OEM product, add the name of the custom variable in "Your Module Settings" page with a "##" prefix. Here is a screenshot from the OEM MakeWizard :
                Build the OEM product and before running the exe, remember to run the .reg file to update the registry. Note that if you rebuild your product and testing it using the MakeWizard, the registry keys will need to be created again by running the .reg file.
The custom system variable can be accessed using acedSetVar / acedGetVar in your ObjectARX code or using the Application.SetSystemVariable / Application.GetSystemVariable from your .Net code. Users of your OEM product can change the variable using the "SetVar" command.

## 评论

**内容**: Doug Goforth said...
This is extra cool, Balaji. Are the registry settings the same if I want to store a string instead of an integer?
Here is what I think it should be for a string, but I am not sure what TypeFlags is:

[HKEY_LOCAL_MACHINE\SOFTWARE\Company\MYOEM\R19\MYOEM-E001:409\Variables\MYSTRINGVAR]
"PrimaryType"=dword:0000138d
"StorageType"=dword:00000002
"TypeFlags"=dword:00000009
@="MYSTRINGVAL"
Reply
02/06/2015 at 11:20 AM

---
**内容**: Balaji said...
Hi Doug,
Sorry for the delay in getting back to you.
You can find examples of different types stored by AutoCAD in its registry path. Here is one such example that stores a string :
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\AutoCAD\R20.0\ACAD-E001\Variables\*UILOCALE]
"PrimaryType"=dword:0000138d
"TypeFlags"=dword:00000007
"StorageType"=dword:00000001
@="en-US"
This should help modify it for your OEM product.
Regards,
Balaji
Reply
02/09/2015 at 09:29 PM

---
