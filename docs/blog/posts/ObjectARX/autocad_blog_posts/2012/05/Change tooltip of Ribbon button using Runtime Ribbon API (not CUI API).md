---
title: "Change tooltip of Ribbon button using Runtime Ribbon API (not CUI API)"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - CUI
description: "I want to change the tooltip of my ribbon button. I was hoping to do it like this:"
author: Autodesk
---
# Change tooltip of Ribbon button using Runtime Ribbon API (not CUI API)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/change-tooltip-of-ribbon-button-using-runtime-ribbon-api-not-cui-api.html

## 文章内容

By Adam Nagy
I want to change the tooltip of my ribbon button. I was hoping to do it like this:
thisCmdbutton.ToolTip.Title = tipTitle;
thisCmdbutton.ToolTip.Content = tipContent;
Unfortunately RibbonButton.ToolTip does not seem to have any string properties.
Solution
RibbonButton.ToolTip simply returns an object, but you can cast it to RibbonToolTip:
RibbonToolTip toolTip = myRibbonButton.ToolTip as RibbonToolTip;
if (toolTip == null)
  return;
  toolTip.Title = "New Title";
toolTip.Content = "New Content";

