---
title: "Invoking commands in localized versions"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Layer
description: "You can append the following prefixes to all AutoCAD commands and options in order to avoid localization issues:"
author: Autodesk
---
# Invoking commands in localized versions

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/invoking-commands-in-localized-versions.html

## 文章内容

By Virupaksha Aithal
You can append the following prefixes to all AutoCAD commands and options in order to avoid localization issues:
An underscore _
This calls the English version of the command. For example, the command, _LINE, can be issued from all localized releases and English AutoCAD.
A period .
This calls the original command when a command was redefined. For example, whena user redefines the LINE command. In such a case, _.line can be issued from all localized releases and English AutoCAD. It will always invoke the original LINE command.
A hyphen -
This calls the command-line version of the command (when available). For example, _.-layer calls the command line version of the original layer command in all AutoCAD releases, independent of the localization.

## 评论

**内容**: Anonymoose said...
Not exactly.
The hypen is not an independent prefix like the underscore and period - it is a literal part of the command's name, and it is not available for use with all commands, including many with command line versions.
Reply
11/09/2012 at 08:43 AM

---
