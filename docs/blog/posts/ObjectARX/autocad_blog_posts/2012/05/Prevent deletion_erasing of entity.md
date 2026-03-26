---
title: "Prevent deletion/erasing of entity"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "One way to avoid erasing of entity is to use object overrule. With object overrule, you can override the “Erase” functionality and stop users from ..."
author: Autodesk
---
# Prevent deletion/erasing of entity

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/prevent-deletionerasing-of-entity.html

## 文章内容

By Virupaksha Aithal
One way to avoid erasing of entity is to use object overrule. With object overrule, you can override the “Erase” functionality and stop users from erasing the object.
Below example avoids erasing of only those entities which has xdata with “ADS” application name. To add a xdata with “ADS” application name, refer DevBlog Using .NET API to Add and Remove XData @ http://adndevblog.typepad.com/autocad/2012/04/using-net-api-to-add-and-remove-xdata-.html#tp .
To use the code, first create few entities and add Xdata with “ADS” application name. Run command “eraseOverrule”, which adds an object overrule. The call to “SetXDataFilter()” will make sure overrule is effective only for the entities which has “ADS” application name in xdata.  Now try to deleted entities with xdata, the object overrule callback “Erase” will be called from which code return the “NotApplicable” value. This will force the AutoCAD not delete the entity.
static EraseOverrule eraseRule = null;
  public class EraseOverrule : ObjectOverrule
{
 public override void Erase(DBObject dbObject, bool erasing)
 {
     throw new Autodesk.AutoCAD.Runtime.Exception(
            Autodesk.AutoCAD.Runtime.ErrorStatus.NotApplicable);
       //base.Erase(dbObject, erasing);
 }
}
  [CommandMethod("eraseOverrule")]
static public void eraseOverrule()
{
    if (eraseRule == null)
 {
     eraseRule = new EraseOverrule();
       Overrule.AddOverrule(RXObject.GetClass(typeof(Entity)),
                                            eraseRule, true);
     Overrule.Overruling = true;
     eraseRule.SetXDataFilter("ADS");
 }
 else
 {
     Overrule.Overruling = false;
     Overrule.RemoveOverrule(RXObject.GetClass(typeof(Entity)),
                                                  eraseRule);
     eraseRule.Dispose();
     eraseRule = null;
 }
}

## 评论

**内容**: cincir said...
Hi
Throwing an exception destroys the Undo mechanism. Any remedy?
Reply
11/01/2016 at 07:24 AM

---
**内容**: burak said in reply to cincir...
This will be a little bit delayed answer, but maybe it will be helpful to someone else.
Just add "if (dbObject.IsUndoing) return;" at the begining of the Erase method to run undo mechanism properly.

public override void Erase(DBObject dbObject, bool erasing)
{
if (dbObject.IsUndoing) return;
throw new Autodesk.AutoCAD.Runtime.Exception(
Autodesk.AutoCAD.Runtime.ErrorStatus.NotApplicable);
//base.Erase(dbObject, erasing);
}
Reply
02/23/2023 at 12:49 PM

---
