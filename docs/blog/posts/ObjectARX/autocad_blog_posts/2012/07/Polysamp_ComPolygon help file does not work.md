---
title: "Polysamp/ComPolygon help file does not work"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - Unicode
  - VBA
description: "I was looking at the ARX 2011 SDK\samples\entity\polysamp project and I can see that under the compoly subfolder there is a WinHelp project (compol..."
author: Autodesk
---
# Polysamp/ComPolygon help file does not work

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/polysampcompolygon-help-file-does-not-work.html

## 文章内容

By Adam Nagy
I was looking at the ARX 2011 SDK\samples\entity\polysamp project and I can see that under the compoly subfolder there is a WinHelp project (compoly.hpj, compoly.hm, compoly.rtf). Using Microsoft Help Workshop we can create a WinHelp file (*.hlp) from that, which is referenced from compoly.idl, and that should provide some help somewhere. However when I run the sample, create a ComPolygon entity, select it and press F1, then it still takes me to the AutoCAD help instead of the help provided with polysamp.
Solution
The help file provided with polysamp is only for its COM interface.
Once you created the *.hlp file and placed it where it can be found (e.g. with the dbx files), then when you are inside a programming environment like VBA for AutoCAD (VBAIDE) and select one of the ComPolygon specific properties/methods and click F1 then the appropriate topic inside that help file will come up:
This help file does not provide help in other contexts, inc. when inside the AutoCAD drawing environment and you select an AsdkPoly entity, whose COM wrapper is ComPolygon, and click F1.

