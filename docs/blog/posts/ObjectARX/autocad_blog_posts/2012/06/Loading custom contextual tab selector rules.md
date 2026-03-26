---
title: "Loading custom contextual tab selector rules"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Unicode
description: "After creating a custom ContextualTabSelectorRules xaml file and copying it to the AutoCAD install folder, you may still not see the custom rule in..."
author: Autodesk
---
# Loading custom contextual tab selector rules

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/loading-custom-contextual-tab-selector-rules.html

## 文章内容

By Balaji Ramamoorthy
After creating a custom ContextualTabSelectorRules xaml file and copying it to the AutoCAD install folder, you may still not see the custom rule in the CUI Editor after launching AutoCAD.
This is a known behaviour in AutoCAD. AutoCAD loads the custom rules only if it recognises that the time stamp of the xaml file is more recent as compared to the time it had last read the rules from disk. To workaround this behaviour, following are the two possibilities :
1) After you copy the xaml file to the AutoCAD install folder, change the modified timestamp of the file to indicate the current time.
2) Delete the "ContextualTabSelectorRules.dll" that was last created by AutoCAD in the User's Roaming folder.
Any of the above two workarounds will ensure that AutoCAD loads the custom rule file.

