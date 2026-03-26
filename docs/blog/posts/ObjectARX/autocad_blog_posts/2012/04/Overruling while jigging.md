---
title: "Overruling while jigging"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Unicode
description: "If you filter your overrule based on entries in an entity’s extension dictionary (SetExtensionDictionaryEntryFilter method), then your overrules wo..."
author: Autodesk
---
# Overruling while jigging

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/overruling-while-jigging.html

## 文章内容

By Stephen Preston
If you filter your overrule based on entries in an entity’s extension dictionary (SetExtensionDictionaryEntryFilter method), then your overrules won’t be applied the entity is being jigged (e.g. in a copy, rotate or move command). In general, AutoCAD copies an entity (creating a non-database-resident copy) while jigging it in a command, and the extension dictionary is not copied. This means the overrule isn't applied.
If you instead filter on an Xdata registered app id (SetXdataFilter method), then the xdata should be copied with the entity, and your overrule will be applied while jigging.

