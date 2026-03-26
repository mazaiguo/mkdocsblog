---
title: "avoid module loading issues with DBX enablers"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "I have an ObjectARX User Interface (.ARX) module that is dependent on an ObjectDBX Object Enabler (.DBX) module. I link the .ARX module with the im..."
author: Autodesk
---
# avoid module loading issues with DBX enablers

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/avoid-module-loading-issues-with-dbx-enablers.html

## 文章内容

By Xiaodong Liang
Issue
I have an ObjectARX User Interface (.ARX) module that is dependent on an ObjectDBX Object Enabler (.DBX) module. I link the .ARX module with the import library (.LIB) for the .DBX, but even though the .DBX demand-loads correctly on proxy detection, the .ARX will not demand-load on command invocation and the following error occurs:
"MyApplication.arx cannot find a DLL or other file that it needs."
This works correctly if I add the location of the .DBX to the Windows system path or install it into C:\Program Files\Common Files\Autodesk Shared, but I don't want to do this.
Solution
There is a mechanism available in Visual C++ called "delay loading". This mechanism allows you to link to a library via the standard DLL linking mechanism, but delays its initialization until required.
To specify that your .ARX delay-loads your .DBX, edit your .ARX project's linker settings as follows:
1. Add the delayimp.lib library file to the "Object/library modules" list.
2. Manually specify the setting, /delayload:"MyDbxModule.dbx, in the Project Options text box.
You can demand-load both the .ARX module and the .DBX without being constrained by the Windows system path. You will need to programmatically loadthe DBX application from the ARX application for this technique to work, therefore, use either acrxLoadMoudle() or acexDynamicLinker->loadModule()..
For more information, please refer to MSDN such as :
Specifying DLLs to Delay Load
/DELAYLOAD

## 评论

**内容**: mikes said...
A better solution would be to use side by side assembly manifests.
The delay load + acrxLoadModule approach requires that the ARX doesn't called any functions imported from the DBX before the acrxLoadModule call. This probably won't be a problem if you call acrxLoadModule right away in acrxEntryPoint, but is something to watch out for since you could have code running prior to that. For example in constructors for globals. Also, delay loading isn't possible if you're using DLL imported data from the DBX.
Reply
01/31/2013 at 11:50 AM

---
