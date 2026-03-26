---
title: "Hide entity in given paper space viewports using overrule"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Layer
  - Plugin
description: "I would like to hide some entities in specific viewports. I thought about using overrule but not sure how to get started."
author: Autodesk
---
# Hide entity in given paper space viewports using overrule

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/hide-entity-in-given-paper-space-viewports-using-overrule-.html

## 文章内容

By Adam Nagy
I would like to hide some entities in specific viewports. I thought about using overrule but not sure how to get started.
Solution
If you only need to hide given entities in certain paper space viewports, i.e. you do not need this functionality for model space viewports, then you can use layers which are designed to solve per viewport visibility.
These are the things your AddIn needs to do:
Create a clone of the layer that the entity you want to hide in a specific viewport is using. This is needed so that when the entity is drawing itself in the viewports where it is still visible, it will use the same color, line width, etc, that it would originally use 
For the same reason, you would also need to keep the clone layer properties in sync with the original layer 
Freeze the clone layer in the appropriate viewports 
Use overrule to make the entity use the previously created clone layer 
When the layer is cloned, the program adds an extension dictionary entry to it with the ObjectId of the original layer. It also monitors the layers for changes in order to update the cloned layers.
It also adds an extension dictionary entry to the overruled entity with the ObjectId of the clone layer it should use - also the Overrule is filtered to entities that have this specific extension dictionary entry.
And this is the Overrule's implementation:
public class MyOverrule : DrawableOverrule
{
  public override int SetAttributes(
    Drawable drawable, DrawableTraits traits)
  {
    int ret = base.SetAttributes(drawable, traits);
      ObjectId id = HideControl.GetEntityLayerId(drawable);
    if (!id.IsNull)
      traits.Layer = id;
      return ret;
  }
}
The attached project is just to show the concept, and is not fully implemented or tested.
Download _hideobjectpervp_2011-02-15

