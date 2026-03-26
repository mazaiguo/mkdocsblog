---
title: "Using CAcUiNumericEdit - Is it possible to enter values in feet & inches and get the data back in inches?"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - API
  - CUI
description: "Using CAcUiNumericEdit it's easy to enter feet and inches into the editbox, but I also get feet and inches as my return value... How can I convert ..."
author: Autodesk
---
# Using CAcUiNumericEdit - Is it possible to enter values in feet & inches and get the data back in inches?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/using-cacuinumericedit-is-it-possible-to-enter-values-in-feet-inches-and-get-the-data-back-in-inches.html

## 文章内容

By Philippe Leefsma
Q:
Using CAcUiNumericEdit it's easy to enter feet and inches into the editbox, but I also get feet and inches as my return value... How can I convert from feet and inches to inches?
A:
To convert from feet and inches to a decimal value you can use acdbDisToF API

