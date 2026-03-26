---
title: "Tab order and tabbed dialog boxes using CAcUiTab"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
description: "When using the CAcUiTab class, you might observe some problems tabbing between the main dialog controls and the child dialog controls of the curren..."
author: Autodesk
---
# Tab order and tabbed dialog boxes using CAcUiTab

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/tab-order-and-tabbed-dialog-boxes-using-cacuitab.html

## 文章内容

By Gopinath Taget
When using the CAcUiTab class, you might observe some problems tabbing between the main dialog controls and the child dialog controls of the current tab.
It should work like ordinary AutoCAD tab dialogs. So how can you do that i.e, to the controls in child dialog to be in "Tab Order".
The tabbing problem can be resolved by setting WS_EX_CONTROLPARENT style for the child dialog. This can also be done through the dialog resource editor by setting the child dialog's style 'control' to true by selecting the same from properties window.

