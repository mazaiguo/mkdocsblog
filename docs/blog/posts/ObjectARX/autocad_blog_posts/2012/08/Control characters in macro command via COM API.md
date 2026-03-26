---
title: "Control characters in macro command via COM API"
date: 2012-08-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
description: "I added a toolbar button with IAcadToolbar::AddToolbarButton() with the following macro command "^C^C^PLINE\n^P". When I press that button, AutoCAD..."
author: Autodesk
---
# Control characters in macro command via COM API

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/control-characters-in-macro-command-via-com-api.html

## 文章内容

By Philippe Leefsma
Q:
I added a toolbar button with IAcadToolbar::AddToolbarButton() with the following macro command "^C^C^P_LINE\n^P". When I press that button, AutoCAD respond the following:
Command: ^C^C^P_TI
Unknown command "^C^C^P_TI". Press F1 for help.
The same command written in a menu file will work ok. What is wrong there?
A:
The reason AutoCAD says the command is not valid is because you need to format your string with the proper control characters instead of using the menu syntax. For example, the menu file ^C should be replaced by character 0x03 and ^P should be replaced by character 0x10. The rules for this is to subtract 0x40 to any character controls preceded by ^. Note that you should replace the pair ^ + P by just character 0x10 and so on.
I.e.:
    Character P is ASCII 0x50
    0x50 - 0x40 = 0x10
    So replace ^P by character 0x10
NB: If you are using C++ and ObjectARX API, you can then use the CAcUiString::ConvertMenuExecString() method which will do the work for you.

