---
title: "CAdUiCoupledGroupCtrl and CAdUiGroupCtrl in a custom palette"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
  - Plugin
  - Selection
description: "I would like to add grouped controls to my custom palette, but when adding a CDialog derived window to the CAdUiGroupCtrl, CAdUiCoupledGroupCtrl do..."
author: Autodesk
---
# CAdUiCoupledGroupCtrl and CAdUiGroupCtrl in a custom palette

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/caduicoupledgroupctrl-and-caduigroupctrl-in-a-custom-palette.html

## 文章内容

By Adam Nagy
I would like to add grouped controls to my custom palette, but when adding a CDialog derived window to the CAdUiGroupCtrl, CAdUiCoupledGroupCtrl does not seem to work properly. Also the dialog color does not match the AutoCAD palette color and the combo box placed on the dialog does not seem to send the selection changed messages. How could I solve these problems?
Solution
The attached sample (Download Mycustompalettevs2008) shows how you can do it.
It has a dialog panel called MyPanel derived from CDialog which is added directly to the palette and also to the grouped controls that the coupled groups control contain.
The dialog handles resizing and also overrides the color of the dialog to match the AutoCAD palette color using CAdUiThemeManager and CAdUiTheme.
It also shows messages in the Command Window when the selection changes in the combo or tree view control.
This is what it looks like:

