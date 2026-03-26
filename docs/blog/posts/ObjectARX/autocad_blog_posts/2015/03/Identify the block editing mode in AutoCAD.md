---
title: "Identify the block editing mode in AutoCAD"
date: 2015-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C++
  - ObjectARX
description: "In last couple of weeks we have received quires related to identifying the block editing state in AutoCAD. One approach to identify the state is to..."
author: Autodesk
---
# Identify the block editing mode in AutoCAD

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/identify-the-block-editing-mode-in-autocad.html

## 文章内容

By Virupaksha Aithal
In last couple of weeks we have received quires related to identifying the block editing state in AutoCAD. One approach to identify the state is to read the system variable “BLOCKEDITOR” using GetSystemVariable in .NET or using acedGetVar in ObjectARX. BLOCKEDITOR will be 1 if you are in block editing mode.

## 评论

**内容**: Alexander Rivlis said...
Not acedGetSym but acedGetVar.
Reply
03/06/2015 at 03:31 AM

---
**内容**: Virupaksha Aithal said in reply to Alexander Rivlis...
Hi Alexander,
Thanks for pointing out. The blog is corrected now.
regards
Viru
Reply
03/08/2015 at 09:35 PM

---
**内容**: Alexander Rivlis said...
Hi Virupaksha!
And what about to know the name of block which is editing in BEDIT command? For REFEDIT command there is REFEDITNAME system variable, but for BEDIT I can not found such system variable or other method to identify block name.
Reply
03/09/2015 at 01:55 PM

---
**内容**: Alexander Rivilis said...
My solution:
{code}
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
[assembly: CommandClass(typeof(Rivilis.BEdit))]
namespace Rivilis
{
public class BEdit
{
[CommandMethod("TestBEDIT")]
public void TestBEdit()
{
Document doc =
Application.DocumentManager.MdiActiveDocument;
Editor ed;
if (doc != null)
{
ed = doc.Editor;
if (Autodesk.AutoCAD.Internal.AcAeUtilities.IsInBlockEditor())
{
ed.WriteMessage("\nWe are in block editor of block \"{0}\"",
Autodesk.AutoCAD.Internal.AcAeUtilities.GetBlockName());
}
else
{
ed.WriteMessage("\nWe are NOT in block editor");
}
}
}
}
}
{/code}
Reply
06/25/2015 at 01:58 PM

---
