---
title: "Remove insertion grip point using overrule"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "If you think that the insertion grip point of a block reference is in the way then you can use GripOverrule to remove it."
author: Autodesk
---
# Remove insertion grip point using overrule

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/remove-insertion-grip-point-using-overrule.html

## 文章内容

By Adam Nagy
If you think that the insertion grip point of a block reference is in the way then you can use GripOverrule to remove it.
The following sample only removes the insertion grip point of dynamic block references:
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
  namespace ClassLibrary1
{
  public class Commands
  {
    public class MyGripOverrule : GripOverrule
    {
      public override void GetGripPoints(
        Entity entity, GripDataCollection grips, 
        double curViewUnitSize, int gripSize, 
        Vector3d curViewDir, GetGripPointsFlags bitFlags)
      {
        // It should not be anything else, since we are
        // filtering for block references
        BlockReference br = (BlockReference)entity;
          base.GetGripPoints(entity, grips,
          curViewUnitSize, gripSize,
          curViewDir, bitFlags); 
          // We'll only remove it for dynamic blocks
        if (br.IsDynamicBlock)
        {
          GripData toRemove = null;
          foreach (GripData gd in grips)
          {
            if (gd.GripPoint == br.Position)
            {
              toRemove = gd;
              break;
            }
          }
            if (toRemove != null)
            grips.Remove(toRemove); 
        }
      }
    }
      [CommandMethod("RemoveInsertionPoint")]
    public static void RemoveInsertionPoint()
    {
      Overrule.AddOverrule(
        RXClass.GetClass(typeof(BlockReference)), 
        new MyGripOverrule(), true
      );
      Overrule.Overruling = true;
    }
  }
}

## 评论

**内容**: David said...
Adam,
That Was Great.
David
Reply
11/28/2012 at 05:17 AM

---
**内容**: Sam said...
Thanks.
This really should be an option in the block editor.
Reply
09/02/2017 at 03:42 AM

---
