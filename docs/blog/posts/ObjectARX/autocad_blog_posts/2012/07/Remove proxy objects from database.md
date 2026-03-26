---
title: "Remove proxy objects from database"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - Database
description: "I found a sample which is showing how to remove proxy entities from the drawing using ObjectARX and AcDbEntity::handOverTo. Is it possible to do th..."
author: Autodesk
---
# Remove proxy objects from database

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/remove-proxy-objects-from-database.html

## 文章内容

By Adam Nagy
I found a sample which is showing how to remove proxy entities from the drawing using ObjectARX and AcDbEntity::handOverTo. Is it possible to do the same using .NET API?
I actually would like to remove some non graphical proxy elements whose enabler cannot be found anywhere and are just causing problems.
Solution
I guess by "non graphical proxy elements" you mean proxy objects. Those you would probably find in the Named Objects Dictionary (NOD) or an entity’s Extension Dictionary. The same functionality that was achieved using ARX in the sample you pointed out can also be done using .NET.
However, in case of removing objects from the NOD you might not even need to use the HandOverTo() method, but can simply call DBDictionary.Remove(ObjectId id). The below sample shows both ways: RemoveEntry1/RemoveEntry2
The code goes through the NOD and deletes all the proxies.
The best is to check what proxy you found before deleting it as it could also be other types of proxy, e.g. an AutoCAD Mechanical object, that you might not actually want to remove.
Similarly, you could remove proxy entities from the block table records as well.
using System;
  using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly: CommandClass(typeof(RemoveSaverDictionary.Commands))]
  namespace RemoveSaverDictionary
{
  public class Commands
  {
    public void RemoveEntry1(
      DBDictionary dict, ObjectId id, Transaction tr)
    {
      ProxyObject obj =
        (ProxyObject)tr.GetObject(id, OpenMode.ForRead);
        // If you want to check what exact proxy it is
      if (obj.OriginalClassName != "ProxyToRemove")
        return;
        dict.Remove(id);
    }
      public void RemoveEntry2(
      DBDictionary dict, ObjectId id, Transaction tr)
    {
      ProxyObject obj =
        (ProxyObject)tr.GetObject(id, OpenMode.ForRead);
        // If you want to check what exact proxy it is
      if (obj.OriginalClassName != "ProxyToRemove")
        return;
        obj.UpgradeOpen();
        using (DBObject newObj = new Xrecord())
      {
        obj.HandOverTo(newObj, false, false);
        newObj.Erase();
      }
    }
      public void RemoveProxiesFromDictionary(
      ObjectId dictId, Transaction tr)
    {
      using (ObjectIdCollection ids = new ObjectIdCollection())
      {
        DBDictionary dict =
          (DBDictionary)tr.GetObject(dictId, OpenMode.ForRead);
          foreach (DBDictionaryEntry entry in dict)
        {
          RXClass c1 = entry.Value.ObjectClass;
          RXClass c2 = RXClass.GetClass(typeof(ProxyObject));
            if (entry.Value.ObjectClass.Name == "AcDbZombieObject")
            ids.Add(entry.Value);
          else if (entry.Value.ObjectClass ==
            RXClass.GetClass(typeof(DBDictionary)))
            RemoveProxiesFromDictionary(entry.Value, tr);
        }
          if (ids.Count > 0)
        {
          dict.UpgradeOpen();
            foreach (ObjectId id in ids)
            RemoveEntry2(dict, id, tr);
        }
      }
    }
      [CommandMethod("RemoveProxiesFromNOD", "RemoveProxiesFromNOD",
      CommandFlags.Modal)]
    public void RemoveProxiesFromNOD()
    {
      Database db = HostApplicationServices.WorkingDatabase;
        // Help file says the following about HandOverTo:
      // "This method is not allowed on objects that are
      // transaction resident.
      // If the object on which the method is called is transaction
      // resident, then no handOverTo operation is performed."
      // That's why we need to use Open/Close transaction
      // instead of the normal one
      using (Transaction tr =
        db.TransactionManager.StartOpenCloseTransaction())
      {
        RemoveProxiesFromDictionary(db.NamedObjectsDictionaryId, tr);
          tr.Commit();
      }
    }
      [CommandMethod("RemoveProxiesFromBlocks", "RemoveProxiesFromBlocks",
      CommandFlags.Modal)]
    public void RemoveProxiesFromBlocks()
    {
      Database db = HostApplicationServices.WorkingDatabase;
        using (Transaction tr =
        db.TransactionManager.StartOpenCloseTransaction())
      {
        BlockTable bt =
          (BlockTable)tr.GetObject(
            db.BlockTableId, OpenMode.ForRead);
          foreach (ObjectId btrId in bt)
        {
          BlockTableRecord btr =
            (BlockTableRecord)tr.GetObject(btrId, OpenMode.ForRead);
            foreach (ObjectId entId in btr)
          {
            if (entId.ObjectClass.Name == "AcDbZombieEntity")
            {
              ProxyEntity ent =
                (ProxyEntity)tr.GetObject(entId, OpenMode.ForRead);
                // If you want to check what exact proxy it is
              if (ent.ApplicationDescription != "ProxyToRemove")
                return;
                ent.UpgradeOpen();
                using (DBObject newEnt = new Line())
              {
                ent.HandOverTo(newEnt, false, false);
                newEnt.Erase();
              }
            }
          }
        }
          tr.Commit();
      }
    }
  }
}

