---
title: "Controlling the Highlight Types in AutoCAD"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
description: "When calling AcDbEntity::highlight() or Entity.Highlight() (in .NET) as we all know you get the normal AutoCAD dashed highlight draw."
author: Autodesk
---
# Controlling the Highlight Types in AutoCAD

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/controlling-the-highlight-types-in-autocad.html

## 文章内容

by Fenton Webb
When calling AcDbEntity::highlight() or Entity.Highlight() (in .NET) as we all know you get the normal AutoCAD dashed highlight draw.
However, using these functions before and after your highlight call you can really get some nice new highlight types of your own.
void acgsSetHighlightColor( Adesk::UInt16 colorIndex );
void acgsSetHighlightLinePattern( AcGs::LinePattern pattern );
void acgsSetHighlightLineWeight( Adesk::UInt16 weight );
  If you need to PInvoke these from .NET, here are the C# DLLImport signatures for 2013…
[DllImport("acdb19.dll", CallingConvention = CallingConvention.Cdecl,
EntryPoint = "?acgsSetHighlightColor@@YAXG@Z"]
public static extern void  acgsSetHighlightColor(uint colorIndex);
[DllImport("acdb19.dll", CallingConvention = CallingConvention.Cdecl,
EntryPoint = "?acgsSetHighlightLinePattern@@YAXW4LinePattern@AcGs@@@Z"]
public static extern void  acgsSetHighlightLinePattern(int pattern);
[DllImport("acdb19.dll", CallingConvention = CallingConvention.Cdecl,
EntryPoint = "?acgsSetHighlightLineWeight@@YAXG@Z"]
public static extern void  acgsSetHighlightLineWeight(uint weight);

## 评论

**内容**: Maxence said...
On ACAD 2011, these functions are exported from acad.exe. You have to save the initial color in order to restore it at the end. You can get it with acgsGetHighlightColor
[DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl, EntryPoint = "?acgsGetHighlightColor@@YAGXZ")]
static extern uint acgsGetHighlightColor();
But when I override the color, the pattern (dots) is not displayed anymore. Why?
Reply
04/15/2013 at 08:25 AM

---
