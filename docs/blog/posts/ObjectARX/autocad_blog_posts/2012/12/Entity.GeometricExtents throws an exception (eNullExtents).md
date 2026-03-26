---
title: "Entity.GeometricExtents throws an exception (eNullExtents)"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Block
description: "When I calculate the extents of entities in a drawing, for some entities an exception is thrown with the "eNullExtents" message. What is wrong?"
author: Autodesk
---
# Entity.GeometricExtents throws an exception (eNullExtents)

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/entitygeometricextents-throws-an-exception-enullextents.html

## 文章内容

By Marat Mirgaleev
Issue
When I calculate the extents of entities in a drawing, for some entities an exception is thrown with the "eNullExtents" message. What is wrong?
Solution
This exception occurs for an insert of an empty block or for an empty block attribute. It is "as designed", it's just a notification to the developer about an empty object. An easy solution is to add a separate catch block for this particular exception:
      Extents3d extents;
      try
      {
        extents = pEntity.GeometricExtents;
      }
      catch (Autodesk.AutoCAD.Runtime.Exception ex)
      {
        if (ex.Message == "eNullExtents")
        // The entity is empty and has no extents
        {
          // TODO. We can simply skip this entity...
        }
        else
        //  something is wrong ...
          TODO!
      }

## 评论

**内容**: Oleg said...
Hi, Marat
I think we may use this way as well:
if(pEntity.Bounds.HasValue)
{
extents = pEntity.GeometricExtents;
}
else
{
ed.WrieMessage("\nNo chance, sorry...\n");
return;
}
Reply
12/25/2012 at 06:56 AM

---
**内容**: Sailor said...
Not only an empty block will throw the "eNullExtents" exception, but the ProfileView.GeometricExtents also throws.
Reply
06/10/2014 at 11:54 PM

---
