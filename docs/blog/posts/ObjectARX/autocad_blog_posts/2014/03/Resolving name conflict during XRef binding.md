---
title: "Resolving name conflict during XRef binding"
date: 2014-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - XREF
description: "Recently a developer reported a behavior that a few entities went missing after the external references in a drawing were bound using API. On analy..."
author: Autodesk
---
# Resolving name conflict during XRef binding

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/resolving-name-conflict-during-xref-binding.html

## 文章内容

By Balaji Ramamoorthy
Recently a developer reported a behavior that a few entities went missing after the external references in a drawing were bound using API. On analyzing the drawing and its external references, the reason for this strange behavior was a block definition with the same name being present in the host and in one of the XRef drawings.
Although the block definitions were different in the drawings, they shared the same name. When such XRef drawings are bound, this can result in block references using the block definition from the host drawing.
 If the "insertBind" parameter is set to false in the call to "BindXrefs", this should help resolve such name conflicts. Here is an explanation from acadauto.chm on how AutoCAD resolves such name conflicts during XRef binding :
If the bPrefixName parameter is set to FALSE, the symbol names of the xref drawing are prefixed in the current drawing with <blockname>$x$, where x is an integer that is automatically incremented to avoid overriding existing block definitions. If the bPrefixName parameter is set to TRUE, the symbol names of the xref drawing are merged into the current drawing without the prefix. If duplicate names exist, AutoCAD uses the symbols already defined in the local drawing. If you are unsure whether your drawing contains duplicate symbol names, it is recommended that you set bPrefixName to FALSE.

