---
title: "Determine if the user makes an empty selection set"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
description: "The "+B:S" option with acedSSGet() allow the user to make a single"
author: Autodesk
---
# Determine if the user makes an empty selection set

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/determine-if-the-user-makes-an-empty-selection-set.html

## 文章内容

By Augusto Goncalves
The "+B:S" option with acedSSGet() allow the user to make a single
selection with a pick, window, or polygon. Is there a way to distinguish when
a user presses the Return key or when a user makes an empty selection set with
the mouse?
In both cases, acedSSGet() return RTERROR, but it’s possible check the AutoCAD variable ERRNO if acedSSGet() returns RTERROR.
If the user presses the Return key, ERRNO contains '52'; if the user makes an
empty selection set with the mouse, ERRNO contains '0'.
ads_name ss;
int res; 
res = acedSSGet(L"+B:S", NULL, NULL, NULL, ss);
if (res == RTERROR) {
  // Nothing selected or <RETURN>?
  resbuf rb;
  rb.restype = RTSHORT;
  acedGetVar(L"ERRNO", &rb);
  if (rb.resval.rint == 52)
    acutPrintf(L"\n<Enter>");
  else
    acutPrintf(L"\nEmpty selection");
  return;
} 
acutPrintf(L"\nSomething selected.");
acedSSFree(ss);

