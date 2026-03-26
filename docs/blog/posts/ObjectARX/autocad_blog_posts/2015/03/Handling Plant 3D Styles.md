---
title: "Handling Plant 3D Styles"
date: 2015-03-01
categories:
  - Plant 3D
tags:
  - API
  - Plant 3D
description: "Plant 3D use styles to managed how parts and assets are shown on the project. Most of that information is stored on the dictionaries, more specific..."
author: Autodesk
---
# Handling Plant 3D Styles

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/handling-plant-3d-styles.html

## 文章内容

By Augusto Goncalves
Plant 3D use styles to managed how parts and assets are shown on the project. Most of that information is stored on the dictionaries, more specifically under NOD>Autodesk_PNP.
But the supported way to handle the styles is by the direct APIs, such as the following methods. One important note: this is valid for current/active drawings.
PnIDStyleUtils.GetStyleIdFromName
ProjectSymbolStyleUtils.CopyStyle

