---
title: "When does IsEffectivelyErased return True"
date: 2013-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "For a database resident object that is not itself erased, there are three reasons why isEffectivelyErased() could return true:"
author: Autodesk
---
# When does IsEffectivelyErased return True

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/when-does-iseffectivelyerased-return-true.html

## 文章内容

by Fenton Webb
For a database resident object that is not itself erased, there are three reasons why isEffectivelyErased() could return true:
Some owner up the ownership hierarchy is erased.
This object, or some object up the ownership hierarchy is returning an empty ObjectId from its ownerId() method.
An owner cannot be opened for some reason somewhere up the ownership hierarchy.

