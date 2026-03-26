---
title: "How To Retrieve Ordinals For AEC Exported Functions"
date: 2017-09-01
categories:
  - AutoCAD
tags:
  - DWG
description: "The ordinals for Functions may be useful for RealDWG Apps, one such scenario when realDWG app explodes any AEC entities which are view dependent en..."
author: Autodesk
---
# How To Retrieve Ordinals For AEC Exported Functions

发布日期: 2017-09-01

原始链接: https://adndevblog.typepad.com/autocad/2017/09/how-to-retrieve-ordinals-for-aec-exported-functions.html

## 文章内容

By Madhukar Moogala
The ordinals for Functions may be useful for RealDWG Apps, one such scenario when realDWG app explodes any AEC entities which are view dependent entities, explode of an entity in particular view may result certain geometry respective to that view, to get desired result one may require to set the view of the entity in the drawing and explode.
For reference please look at this blog post
First get OMF SDK for relevant version from https://adn.autodesk.io/
Go To Software and download SDK after accepting License Agreement.

Launch Visual Studio Developer Command
Change to OMFSDK\Lib_$Platform folder
Execute
dumpbin /exports $libname | findstr $functionName
For Example
D:\OMF2018\Lib-x64>dumpbin /EXPORTS AecBase.lib | findstr "drawingPromoterAndIniter"
           897    ?drawingPromoterAndIniter@AecAppDbx@@SAXPEAVAcDbDatabase@@_N@Z (public: static void __cdecl AecAppDbx::drawingPromoterAndIniter(class AcDbDatabase *,bool))
" 897 " is Ordinal number

