---
title: "Checking if custom entity is selected inside a contextual tab selection rule"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Palette
  - Selection
  - Unicode
description: "I'm using the solution from DevBlog [Using custom contextual ribbon tabs], but it does not work for my custom entities. I pass in the name of my en..."
author: Autodesk
---
# Checking if custom entity is selected inside a contextual tab selection rule

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/checking-if-custom-entity-is-selected-inside-a-contextual-tab-selection-rule.html

## 文章内容

By Adam Nagy
I'm using the solution from DevBlog [Using custom contextual ribbon tabs], but it does not work for my custom entities. I pass in the name of my entity that is displayed in the Property Palette, but still, Selection.ContainsOnly("MyEntity") is always false.
Solution
The selection rule is using the .NET type name of the selected entities. So if your entity does not have a .NET wrapper then the selection set will know it as the type name of the .NET wrapper of your custom entity's base class - i.e. if your entity is based on AcDbEntity then the selection set will know it as type "Entity"
So, if you want to check if only your custom entities are selected (and they do not have a .NET wrapper class), then create a utility assembly which iterates through the Selection set and checks each entity's RxClass.Name.
We could simply modify the sample code in DevBlog [Using custom contextual ribbon tabs] the following way to check if only my custom entities called "MyLine" are selected:
public static bool ShowMyTab(object selObj)
{
  Selection sel = (Selection)selObj;
  if (sel.Count < 1)
    return false;
    foreach (IDataItem item in sel)
  {
    if (item.ObjectId.ObjectClass.Name != "MyLine")
      return false;
  }
    return true;
}

