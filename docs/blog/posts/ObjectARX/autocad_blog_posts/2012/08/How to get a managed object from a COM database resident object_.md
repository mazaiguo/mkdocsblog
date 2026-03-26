---
title: "How to get a managed object from a COM database resident object?"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - COM
  - Database
description: "The following sample illustrates how to retrieve the .Net managed object once we have access to its COM wrapper. The best way to achieve that is to..."
author: Autodesk
---
# How to get a managed object from a COM database resident object?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-get-a-managed-object-from-a-com-database-resident-object.html

## 文章内容

By Philippe Leefsma
The following sample illustrates how to retrieve the .Net managed object once we have access to its COM wrapper. The best way to achieve that is to use the old objectId property as below:
[CommandMethod("Com2DotNet")]
public static void Com2DotNet()
{
    AcadApplication acadApp = Application.AcadApplication
        as AcadApplication;
      Object obj = new Object();
    Object pt = new Object();
                 acadApp.ActiveDocument.Utility.GetEntity(
        out obj,
        out pt,
        "\nPick an entity: ");
      Autodesk.AutoCAD.Interop.Common.AcadEntity acadEntity = obj
        as Autodesk.AutoCAD.Interop.Common.AcadEntity;
          Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using(Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ObjectId id = new ObjectId((IntPtr)acadEntity.ObjectID);
          Entity entity = Tx.GetObject(id, OpenMode.ForWrite)
            as Entity;
          entity.ColorIndex = 1;
          Tx.Commit();
    }
}

## 评论

**内容**: Anonymoose said...
It appears that you've overlooked the following static member of DBObject:

public static unsafe ObjectId FromAcadObject(object acadObj)
Reply
08/25/2012 at 03:46 AM

---
**内容**: Andrey said...
Hi Philippe.
>How to get a managed object from a COM
Why you wrote such many code rows? Maybe such:
id.ObjectClass.Create().GetType()
Regards
Reply
08/29/2012 at 01:13 PM

---
**内容**: Andrey said...
Oh, I seem confused managed object with controlled type.
Reply
08/29/2012 at 01:17 PM

---
