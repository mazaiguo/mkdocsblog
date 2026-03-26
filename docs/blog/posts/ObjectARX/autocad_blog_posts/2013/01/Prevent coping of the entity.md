---
title: "Prevent coping of the entity"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - API
  - Block
description: "One way to avoid erasing of entity is to use object overrule. With object overrule, you can override the “WblockClone” and "DeepClone" functionalit..."
author: Autodesk
---
# Prevent coping of the entity

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/prevent-coping-of-the-entity.html

## 文章内容

By Virupaksha Aithal
One way to avoid erasing of entity is to use object overrule. With object overrule, you can override the “WblockClone” and "DeepClone" functionality and return NULL from the overridden API. This stops the users from copying the objects.
Below code shows the procedure.
static ObjOverrule objRule = null;
  public class ObjOverrule : ObjectOverrule
{
    public override DBObject WblockClone(DBObject dbObject,
            RXObject ownerObject, IdMapping idMap, bool isPrimary)
    {
        return null;
        //return base.WblockClone(dbObject,
                                //ownerObject, idMap, isPrimary);
    }
      public override DBObject DeepClone(DBObject dbObject,
                DBObject ownerObject, IdMapping idMap, bool isPrimary)
    {
        return null;
        //return base.DeepClone(dbObject,
                                    //ownerObject, idMap, isPrimary);
    }
}
  [CommandMethod("copyOverrule")]
static public void copyOverrule()
{
    if (objRule == null)
    {
        objRule = new ObjOverrule();
          Overrule.AddOverrule(RXObject.GetClass(typeof(Line)),
                                               objRule, true);
        Overrule.Overruling = true;
    }
    else
    {
        Overrule.Overruling = false;
        Overrule.RemoveOverrule(RXObject.GetClass(typeof(Line)),
                                                     objRule);
        objRule.Dispose();
        objRule = null;
    }
}

