---
title: "Identify the visibility of Layer property manager dialog"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Layer
description: "You can use system variable “LAYERMANAGERSTATE” to identify the state of the Layer property manager.   LAYERMANAGERSTATE is ready only system varia..."
author: Autodesk
---
# Identify the visibility of Layer property manager dialog

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/identify-the-visibility-of-layer-property-manager-dialog.html

## 文章内容

By Virupaksha Aithal
You can use system variable “LAYERMANAGERSTATE” to identify the state of the Layer property manager.   LAYERMANAGERSTATE is ready only system variable and indicates below states of the window
[CommandMethod("LayerDlgState")]
static public void LayerDlgState()
{
    short dlg =
        (short)Application.GetSystemVariable("LAYERMANAGERSTATE");
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      if (dlg == 0)
    {
        ed.WriteMessage("Layer Palette is closed\n");
    }
    else if (dlg == 1)
    {
        ed.WriteMessage("Layer Palette is open\n");
    }
  }

