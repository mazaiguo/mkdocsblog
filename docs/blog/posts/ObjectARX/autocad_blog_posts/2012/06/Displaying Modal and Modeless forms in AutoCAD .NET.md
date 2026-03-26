---
title: "Displaying Modal and Modeless forms in AutoCAD .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Palette
  - VBA
description: "Another in my occasional series of common beginner mistakes that take forever and a day to debug ."
author: Autodesk
---
# Displaying Modal and Modeless forms in AutoCAD .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/displaying-modal-and-modeless-forms-in-autocad-net.html

## 文章内容

By Stephen Preston
Another in my occasional series of common beginner mistakes that take forever and a day to debug .
Sometimes what we already know gets in the way. If you want to display a form in .NET, you use Form.ShowDialog. Right?
Wrong! If you do, you’re likely to find AutoCAD hanging or displaying other unexpected behavior – particularly if you’re doing this in conjunction with VBA macros. Instead display your dialogs using the AutoCAD .NET APIs provided for the purpose:
Application.ShowModalDialog
Application.ShowModelessDialog
And if you’re working with modeless dialogs, consider using a palette instead. Kean Walmsley explains why that’s a good idea here.

