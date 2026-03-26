---
title: "Copy extension dictionary"
date: 2014-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below command shows the procedure to copy the extension dictionary entries from one entity to another. A special logic is placed at the end to set ..."
author: Autodesk
---
# Copy extension dictionary

发布日期: 2014-06-01

原始链接: https://adndevblog.typepad.com/autocad/2014/06/copy-extension-dictionary.html

## 文章内容

By Virupaksha Aithal
Below command shows the procedure to copy the extension dictionary entries from one entity to another. A special logic is placed at the end to set the names of the dictionary same as source object as “DeepCloneObjects” copy the objects with different names in target entity.
[CommandMethod("copyExtDic")]
public void copyExtDic()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityResult surRes =
                ed.GetEntity("Select source entity");
      if (surRes.Status != PromptStatus.OK)
        return;
      PromptEntityResult tarRes =
                ed.GetEntity("Select target entity");
      if (tarRes.Status != PromptStatus.OK)
        return;
      ObjectIdCollection ids = new ObjectIdCollection();
    ObjectId tarId = ObjectId.Null;
    ObjectId surId = ObjectId.Null;
      using (Transaction tr =
            db.TransactionManager.StartTransaction())
    {
        DBObject dbObj = tr.GetObject(surRes.ObjectId,
                                       OpenMode.ForRead);
          surId = dbObj.ExtensionDictionary;
          if (surId != ObjectId.Null)
        {
            DBDictionary dbExt =
                      (DBDictionary)tr.GetObject(surId,  
                                    OpenMode.ForRead);
              foreach (DBDictionaryEntry entry in dbExt)
            {
                ids.Add(entry.Value);
            }
        }
        else
        {
            ed.WriteMessage("No dictionary to copy");
            return;
        }
        //find if entiy has
        DBObject target = tr.GetObject(tarRes.ObjectId,
                                          OpenMode.ForRead);
        tarId = target.ExtensionDictionary;
          if (tarId == ObjectId.Null)
        {
            target.UpgradeOpen();
            target.CreateExtensionDictionary();
            tarId = target.ExtensionDictionary;
        }
          tr.Commit();
    }
      IdMapping mapping = new IdMapping();
    db.DeepCloneObjects(ids, tarId, mapping, false);
      //
    using (Transaction tr =
            db.TransactionManager.StartTransaction())
    {
        DBDictionary dbExt =
         (DBDictionary)tr.GetObject(surId, OpenMode.ForRead);
          DBDictionary dbTarg =
            (DBDictionary)tr.GetObject(tarId, OpenMode.ForWrite);
          foreach (IdPair pair in mapping)
        {
            DBObject target = tr.GetObject(pair.Value,
                                              OpenMode.ForRead);
            dbTarg.SetName(
                dbTarg.NameAt(pair.Value),
                dbExt.NameAt(pair.Key));
        }
        tr.Commit();
    }
}

## 评论

**内容**: Oleg said...
The code doesn't work... It throw an excrption at the end
Reply
06/15/2023 at 04:22 AM

---
