---
title: "Using c:solprof from Visual LISP"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Layer
  - Selection
description: "For a properly selection set ss1, the next information required is the data for the prompt ("Display hidden profile lines on separate layer?"). Thi..."
author: Autodesk
---
# Using c:solprof from Visual LISP

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-csolprof-from-visual-lisp.html

## 文章内容

By Augusto Goncalves
For a properly selection set ss1, the next information required is the data for the prompt ("Display hidden profile lines on separate layer?"). This results in the 2nd ("Project profile lines onto a plane?") and 3rd ("Delete tangential edges?") prompts being answered with "Y". We can substitute 1 and 0 to represent "Y" and "N", respectively, the tangential edges are retained:
(setq err (vl-catch-all-apply 'c:solprof (list ss1 1 1 0)))

