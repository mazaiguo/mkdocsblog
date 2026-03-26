---
title: "Working with ToolPalette groups using .Net"
date: 2013-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - CUI
  - Palette
  - Plugin
description: "The "CAcTcUiToolPaletteGroup" class is not exposed in the .Net API. To work around this limitation, utility methods can be implemented using mixed-..."
author: Autodesk
---
# Working with ToolPalette groups using .Net

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/working-with-toolpalette-groups-using-net.html

## 文章内容

By Balaji Ramamoorthy
The "CAcTcUiToolPaletteGroup" class is not exposed in the .Net API. To work around this limitation, utility methods can be implemented using mixed-managed code that perform actions such as creating a tool palette group, adding palettes to it and removing the tool palette group.
Here is a sample project that uses the mixed-managed assembly in a .Net project to demonstrate this.
This project implements the following commands in .Net :
1) "Demo1" : Demonstrates iterating through all the ToolPalette groups and the ToolPalettes added to them. After this command is run, a series of message boxes appear to display the names of the ToolPalette groups and ToolPalettes.
2) "Demo2" : Demonstrates activating a specific palette using its name. After this command is run, the ToolPalette named "Mechanical" is set as the Active ToolPalette.
3) "Demo3" : Demonstrates the creation of a ToolPalette group, creation of a ToolPalette and adding ToolPalettes to the newly created ToolPalette group. After this command is run, a new group named "MyTPGroup" can be found with two ToolPalettes added to them. One of the two ToolPalette is a newly created ToolPalette called "MyPalette".
4) "Demo4" : Demonstrates the removal of a ToolPalette and ToolPaletteGroup. After this command is run, the "MyTPGroup" and "MyPalette" are removed.
Download ToolPaletteGroupMixedManagedDemo

## 评论

**内容**: imvivs said...
Hello Balaji,
I have some query, I hope u will answer me.
Can u list out the benefits, extra features, and reason why we are creating Tools Palettes using .NET API(Programming) rather than simply use AutoCAD's Tool Palette from the menu item?
Reply
10/21/2013 at 11:36 AM

---
**内容**: Balaji said in reply to imvivs...
Hi,
In this case, what can be done using the AutoCAD UI is the same as what is done using the API. It is a way to automate the creation of tool palette and tool palette groups without requiring your end-user to modify the tool palette to invoke your custom commands. I hope this explains.
Regards,
Balaji
Reply
10/22/2013 at 12:20 AM

---
**内容**: sakbhat said in reply to Balaji...
Hi Balaji,
I also want to know the same but could you please elaborate it a bit so that i can easily understand the role of using .Net for developing tool palletes.
Thanks in advance

Reply
10/22/2013 at 12:42 AM

---
**内容**: imvivs said...
Ok, Thanks for your quick response.
Can u elaborate what can be automate using programming? And one more thing, is there possibility in AutoCAD or using .NET or in both: To save and reuse the tool palettes on new drawing or on start-up once user log off?
Regards,
vivs
Reply
10/22/2013 at 01:11 AM

---
**内容**: Balaji said in reply to imvivs...
Hi Vivs,
Sorry, I am not sure what you want me to elaborate.
About saving the changes for the next session - yes, it does get saved as demonstrated in the sample project in the blog post.
Regards,
Balaji
Reply
10/22/2013 at 01:53 AM

---
**内容**: imvivs said...
Hi Balaji thanks for reply,
Can you please list out the point that can be automated using .NET since AutoCAD also provides TP features.
Does AutoCAD provide Save option for saving the Tool Palettes after user has logged off?
Reply
10/22/2013 at 02:42 AM

---
**内容**: vnsharifi@gmail.com said...
Hello Balaji,
Not sure if this is a reight question to ask here in this forum.if not please direct me to right location.
I don't have any experience in C++ . Just wanted to Compile your source code and use the wrapper in my project.
I have AutoCAD 2015 and VS2012 Express
I intalled [ObjectArx 2015] and when tried to make the Built it gives me errors like below.
=================================================
3 IntelliSense: cannot open source file "afxwin.h" c:\2015 RebarCAD custom Files\Misc Code Downloaded From InterNet\Create Tool Palette Group Using wrapper\ToolPaletteWrapperDemo\stdafx.h 15 1 ToolPaletteWrapperDemo
==================================================
That error happens for :
afxwin.h
afxext.h
afxole.h
afxodlgs.h
afxdisp.h
afxdb.h
afxdao.h
afxdtctl.h
afxcmn.h

Any help from you or other experts would be apprecited.
Janet.
Reply
12/17/2014 at 06:38 AM

---
**内容**: Balaji said...
Hi Janet,
I do not think MFC is included in the Visual Studio Express edition. Is it possible for you to try it in any other version of Visual studio ?
Regards,
Balaji
Reply
12/18/2014 at 02:50 AM

---
**内容**: Alain said...
Hello Balaji,
I tried to start the project using Visual studio 2013 and AutoCAD 2013, but get this error in Studio :
"error LNK1104: cannot open file 'AcTcUi.lib'"
Am I missing a reference? I can't find the File.
Regards,
Alain

Reply
01/15/2015 at 05:30 AM

---
**内容**: Balaji said in reply to Alain...
Hello Alain,
You should be finding that lib in \ObjectARX 2013\lib-x64 or \ObjectARX 2013\lib-win32 folder. Do you have one of those paths added to the library directories ?
Also, you would need platform toolset set as V100 to load it in AutoCAD 2013. The option to set v100 is only available in Visual Studio 2013 if you have Visual Studio 2010 also installed in the system.
Regards,
Balaji
Reply
01/15/2015 at 08:35 AM

---
**内容**: Rob said...
Hello Balaji,
I have managed to build solution fine and have 2 dlls, I have loaded in the demoproject dll but if I try to run one of the demo commands it states the following:
System.IO.FileNotFoundException: Could not load file or assembly 'ToolPaletteWrapperDemo.dll' or one of its dependencies. The specified module could not be found.
File name: 'ToolPaletteWrapperDemo.dll'
at DemoProject.MyCommands.Demo1()
Do you have any ideas?
Regards,
Rob
Reply
11/30/2015 at 08:56 AM

---
**内容**: Thineshbabu said in reply to Rob...
Hello Rob, How did you resolve the above issue? I am also facing the same error while using demo commands. Please reply.. thank you!
System.IO.FileNotFoundException: Could not load file or assembly 'ToolPaletteWrapperDemo, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null' or one of its dependencies. The system cannot find the file specified.
File name: 'ToolPaletteWrapperDemo, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null'
at DemoProject.MyCommands.Demo1()
Reply
05/17/2023 at 12:09 AM

---
**内容**: Gdm9 said in reply to Thineshbabu...
Hello Thineshbabu,
I'm working on Autocad 2023, and I've solved this problem by putting for :
the "Include directory" : C:\ObjectARX 2009\inc
Because otherwise with version 2023 I had the error: error LNK2019: external symbol not resolved "public: virtual __cdecl CAdUiPathname::~CAdUiPathname(void)".
For the "Library directories": c:\ObjectARX 2023\lib-x64
Because otherwise I had the problem "System.IO.FileNotFoundException: Could not load file or assembly 'ToolPaletteWrapperDemo'"
( and so you have to adapt the version of adui24.lib to that of your autocad )
This will load the dll dependencies for your version of autocad, for example adui24.dll for autocad 2023.
I hope it works for you
Reply
07/18/2023 at 07:21 AM

---
**内容**: Stacy Dunn said...
I am trying to compile this in VS 2017 using the 2020 SDK. I have updated all of the references, but I get a series of errors:
Error LNK2019 unresolved external symbol "protected: virtual void __cdecl CAdUiPathname::AssignCopy(class CAdUiPathname const &)" (?AssignCopy@CAdUiPathname@@$$FMEAAXAEBV1@@Z) referenced in function "public: __cdecl CAdUiPathname::CAdUiPathname(class CAdUiPathname const &)" (??0CAdUiPathname@@$$FQEAA@AEBV0@@Z) ToolPaletteWrapperDemo
Error LNK2001 unresolved external symbol "protected: virtual void __cdecl CAdUiPathname::AssignCopy(class CAdUiPathname const &)" (?AssignCopy@CAdUiPathname@@MEAAXAEBV1@@Z) ToolPaletteWrapperDemo

I am not that familiar with C++. VS is not flagging any of the code or references. Are there settings that need to be changed in VS2017 that were not present when this was written?
Thank you,
Stacy
Reply
01/27/2021 at 07:19 PM

---
**内容**: Thinesh said in reply to Stacy Dunn...
I am facing the same problem. Please could you suggest me how did you resolve this issue. Thanks!!
Reply
04/26/2023 at 02:41 AM

---
