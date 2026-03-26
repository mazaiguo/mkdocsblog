---
title: "How to Import Step (.stp) Files to AutoCAD"
date: 2020-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "Though there is not a direct API to import a Step file in to AutoCAD drawing unlike Body.AcisIn, we use Editor.Command API to invoke Import command"
author: Autodesk
---
# How to Import Step (.stp) Files to AutoCAD

发布日期: 2020-07-01

原始链接: https://adndevblog.typepad.com/autocad/2020/07/how-to-import-step-stp-files-to-autocad.html

## 文章内容

By Madhukar Moogala
Though there is not a direct API to import a Step file in to AutoCAD drawing unlike Body.AcisIn, we use Editor.Command API to invoke Import command
public void StepIn()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;            
ed.Command(new object[] { "_.IMPORT",
                  "D:\\Work\\CADFiles\\Scafolf_Bracket_Asy.stp"});
}

