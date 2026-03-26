---
title: "Finding out if a layer contains entities"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
description: "Is there a quick way to find out if there are entities associated with a layer?"
author: Autodesk
---
# Finding out if a layer contains entities

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/finding-out-if-a-layer-contains-entities.html

## 文章内容

By Adam Nagy
Is there a quick way to find out if there are entities associated with a layer?
Solution
I have a simple solution for you. We can use the Purge() method of the class Database to check whether the layer can be purged or not. If it can be, it is not associated with any objects; if not, it is associated with other objects. The Purge() method accepts an ObjectId collection argument. If the layers in the collection can be purged, they will remain in the collection; otherwise will be removed from the collection. Therefore, we can check whether the layer id is still in the collection or not to know whether it can be purged or not. Here, we can just check whether the count of the collection is zero or not since we only add a single layer to the collection.
Please make a layer named “Layer1” and draw something on it before testing the command.
[CommandMethod("CheckLayerDependence")]
public void CheckLayerDependence()
{
  Editor ed =
    Autodesk.AutoCAD.ApplicationServices.Application.
    DocumentManager.MdiActiveDocument.Editor;
    Database db = HostApplicationServices.WorkingDatabase;
    using (Transaction tr = db.TransactionManager.StartTransaction())
  {
    LayerTable lt =
      (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);
      if (lt.Has("Layer1"))
    {
      ObjectId ltrId = lt["Layer1"];
        ObjectIdCollection idCol = new ObjectIdCollection();
      idCol.Add(ltrId);
      db.Purge(idCol);
        if (idCol.Count != 0)
      {
        ed.WriteMessage("\nLayer1 does not have dependencies.");
      }
      else
      {
        ed.WriteMessage("\nLayer1 has dependencies.");
      }
    }
    else
    {
      ed.WriteMessage("\nLayer1 does not exist!");
    }
      tr.Commit();
  }
}

