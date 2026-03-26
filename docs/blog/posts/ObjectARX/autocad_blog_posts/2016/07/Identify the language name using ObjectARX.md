---
title: "Identify the language name using ObjectARX"
date: 2016-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Plot
description: "ObjectARX 2017 SDK exposes class “AcLocale” using which language information of the AutoCAD can be retrieved. This “AcLocale” is new class in 2017."
author: Autodesk
---
# Identify the language name using ObjectARX

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/identify-the-language-name-using-objectarx.html

## 文章内容

By Virupaksha Aithal
ObjectARX 2017 SDK exposes class “AcLocale” using which language information of the AutoCAD can be retrieved. This “AcLocale” is new class in 2017.
#include "rxregsvc.h"
void getLocal()
{
 AcLocale locale = acrxProductLocale();
 acutPrintf(locale.iso2LangName());
 acutPrintf(locale.iso2CountryName());
}

