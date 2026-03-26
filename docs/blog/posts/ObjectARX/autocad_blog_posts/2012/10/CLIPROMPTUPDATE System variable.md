---
title: "CLIPROMPTUPDATE System variable"
date: 2012-10-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "From AutoCAD 2013, CLIPROMPTUPDATE system variable controls the whether the command line displays the progress as a command or script is run."
author: Autodesk
---
# CLIPROMPTUPDATE System variable

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/clipromptupdate-system-variable.html

## 文章内容

By Virupaksha Aithal
From AutoCAD 2013, CLIPROMPTUPDATE system variable controls the whether the command line displays the progress as a command or script is run.
When CLIPROMPTUPDATE is set to 1, AutoCAD updates the command line during the running of command or lisp routine. With Value set as 0, AutoCAD only updates the command line at the end of command or end of lisp routine
Try DevBlog (princ "\r") does not update the command line anymore with CLIPROMPTUPDATE with value 0 and 1 to find the difference.

