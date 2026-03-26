---
title: "Where did my Interop assemblies go?"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - COM
  - COM Interop
description: "As of AutoCAD 2013, we stopped registering AutoCAD COM Interop assemblies in the Global Assembly Cache (GAC). We continue to ship reference assembl..."
author: Autodesk
---
# Where did my Interop assemblies go?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/where-did-my-interop-assemblies-go.html

## 文章内容

By Stephen Preston
As of AutoCAD 2013, we stopped registering AutoCAD COM Interop assemblies in the Global Assembly Cache (GAC). We continue to ship reference assemblies in the ObjectARX SDK.
The correct way to use these assemblies is follows:
Reference the interop assemblies in your project from the ObjectARX SDK 2013 inc-win32 or inc-x64 folder, depending on whether you’re building a 32-bit or 64-bit plug-in. The two assemblies are Autodesk.AutoCAD.Interop and Autodesk.AutoCAD.Interop.Common.
By default in Visual Studio 2010, these are referenced with Copy Local = False, and Embed Interop Types = True:
  Erm. That’s all.
The ‘Embed Interop Types’ setting ensures the information required to access the ActiveX APIs you use in your code is embedded into your plug-in assembly. You don’t have to try to register the interop in the GAC, or ship the ObjectARX SDK reference assemblies with your plug-in, or create your own interop assemblies. If you’re migrating an older project instead of creating a new one, then you will have to check that ‘Embed Interop Types’ is set to true.
As an interesting aside, I was talking to Brian Ekins at the Manufacturing DevCamp and the conversation somehow drifted onto this topic. Turns out that it’s the other way around for Inventor: it causes problems for Inventor add-ins if you have ‘Embed Interop Types’ set to True  – so you must set it to false for Inventor. We don’t create such differences between our products to confuse people, its just that they follow very different architectures and have completely different development teams. To coordinate to that level of granularity would surely cause every development team in the company to grind to a standstill .

## 评论

**内容**: Pat K said...
When using a reference to Autodesk.AutoCAD.Interop are you required to build two different .dlls if you have a need to support Windows 32-bit and Windows 64-bit?
(e.g. HelloWorld32.dll and HelloWorld64.dll)
Reply
09/05/2012 at 02:16 PM

---
**内容**: Madhukar Moogala said in reply to Pat K...
The 32-bit and 64-bit ActiveX APIs use different GUIDs. So unless you use late binding, you would be looking at two versions.
Reply
09/05/2012 at 04:46 PM

---
**内容**: Oddpets said...
Interesting article.
I have an interesting problem with the assemblies in ACAD 2017 using ObjectARX_2017

LINE 1: AcadAcCmColor aColor = new AcadAcCmColor();
LINE 2: aColor.ColorIndex = (AcColor)WIRE_COLOUR;
LINE 3: line.TrueColor = aColor;

All compiles Ok but LINE 2: produces a runtime error
Exception thrown: 'System.Runtime.InteropServices.COMException' in mscorlib.dll
Retrieving the COM class factory for component with CLSID {8489ED0D-5A6D-4C59-B173-2F9855DE496C} failed due to the following error: 80040154 Class not registered (Exception from HRESULT: 0x80040154 (REGDB_E_CLASSNOTREG)).
I have my environment configured as suggested to 'embed' the assemblies.
Any advice welcome
Mark
Reply
02/23/2017 at 06:41 PM

---
**内容**: Norman said...
Contrarily to what Stephen said, when I use AutoCAD COM interop assemblies, I ALWAYS make sure NOT EMBED them (i.e. always set "Embed Inperop Types" to False). In fact, the error you got might just be the result of embedding.
As for "Copy to Local" being True of False, it depends on which AutoCAD COM interop assemblies you are using. If you use the ones coming from ObjectARX SDK, it should be set to False, because AutoCAD installation has the 2 COM interop assemlies installed in AutoCAD folder. You can also set references to the 2 interops directly to the ones in AutoCAD installtion folders (thus, "Copy to Local" is false, of course). However, if you use Visual Studio to generate the interop for you (that is, in adding references dialog box's COM tab, select AutoCAD COM libraries...), then the generated interops should be set "Copy to Local" as True.
Reply
02/28/2017 at 10:13 AM

---
