---
title: "Read-only non-COM property"
date: 2012-04-01
categories:
  - AutoCAD COM
tags:
  - COM
description: "If you want to make your property read-only (greyed out), then you just have to return eNotApplicable from your property's subSetValue() function:"
author: Autodesk
---
# Read-only non-COM property

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/read-only-non-com-property.html

## 文章内容

By Adam Nagy
If you want to make your property read-only (greyed out), then you just have to return eNotApplicable from your property's subSetValue() function:
Acad::ErrorStatus MyDoubleProperty::subSetValue(
  AcRxObject* pO, const AcRxValue& value) const
{
  return Acad::eNotApplicable;
}

## 评论

**内容**: Aura Properties said...
Thanks for the the post Adam, I was keep searching for the issue and guess what I found you.
Reply
03/02/2023 at 10:07 PM

---
