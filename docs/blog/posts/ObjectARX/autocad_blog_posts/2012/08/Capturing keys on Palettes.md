---
title: "Capturing keys on Palettes"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - Palette
description: "Different from Form, on a User Control do not have the KeyPreview property usually used to modify the behavior to capture keys. Actually there is a..."
author: Autodesk
---
# Capturing keys on Palettes

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/capturing-keys-on-palettes.html

## 文章内容

By Augusto Goncalves
Different from Form, on a User Control do not have the KeyPreview property usually used to modify the behavior to capture keys. Actually there is another way that works for both forms and user controls, by using ProcessCmdKey override, as shown below.
protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
{
  if (keyData == (Keys.Escape))
  {
    MessageBox.Show("Escape pressed");
  }
  return base.ProcessCmdKey(ref msg, keyData);
}

