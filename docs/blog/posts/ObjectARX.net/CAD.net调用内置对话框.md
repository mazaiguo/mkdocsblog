---
title: CAD.net调用内置对话框
date: 2024-06-30
categories:
  - CAD开发
  - .NET
  - 对话框
tags:
  - CAD.net
  - 对话框
  - ColorDialog
  - LinetypeDialog
description: CAD.net中调用内置颜色对话框和线型对话框的使用方法
author: JerryMa
---

# CAD.net调用内置对话框

```csharp
[CommandMethod("CmdTest_ShowDialog")]
public void CmdTest_ShowDialog()
{
    var dm = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager;
    var doc = dm.MdiActiveDocument;
    var ed = doc.Editor;
    var db = doc.Database;
    ed.WriteMessage("\n测试cad颜色面板+线型面板");

    var cd = new ZwSoft.ZwCAD.Windows.ColorDialog();
    var dr = cd.ShowDialog();
    if (dr == System.Windows.Forms.DialogResult.OK)
        ed.WriteMessage("\ncad颜色选择了: " + cd.Color.ToString());

    var ld = new ZwSoft.ZwCAD.Windows.LinetypeDialog();
    dr = ld.ShowDialog();
    if (dr == System.Windows.Forms.DialogResult.OK)
        ed.WriteMessage("\ncad线型选择了: " + ld.Linetype.ToString());

    var dlg = new System.Windows.Forms.ColorDialog();
    dr = dlg.ShowDialog();
    if (dr == System.Windows.Forms.DialogResult.OK)
        ed.WriteMessage("\n系统颜色选择了: " + dlg.Color.ToString());
}
```

