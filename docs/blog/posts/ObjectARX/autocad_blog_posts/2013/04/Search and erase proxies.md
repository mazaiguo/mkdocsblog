---
title: "Search and erase proxies"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - ObjectARX
description: "This post is quite similar to this another one, Remove all proxy entities from a drawing using ObjectARX. Both start at the same principle: search ..."
author: Autodesk
---
# Search and erase proxies

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/search-and-erase-proxies.html

## 文章内容

By Augusto Goncalves
This post is quite similar to this another one, Remove all proxy entities from a drawing using ObjectARX. Both start at the same principle: search for object that are proxy. This .NET version goes a little deeper and try find dictionaries that hold proxy objects. Note that some objects cannot be erased, so we perform a trick: hand over to another entity. For others, we just try erase and see what happens.
The main idea is to perform a clean up and avoid the proxy message. Please be advised that this will erase objects and entities, so it may not be safe. Use carefully.
Suggestions to improve this? Feel free to comment.
[CommandMethod("searchAndEraseProxy")]
public static void searchAndEraseProxy()
{
  _NODEntriesForErase = new ObjectIdCollection();
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
  using (Transaction trans = db.TransactionManager.
    StartTransaction())
  {
    // open block table
    BlockTable bt = trans.GetObject(db.BlockTableId,
      OpenMode.ForRead) as BlockTable;
    // for each block table record
    // (mspace, pspace, other blocks)
    foreach (ObjectId btrId in bt)
    {
      BlockTableRecord btr = trans.GetObject(btrId,
        OpenMode.ForRead) as BlockTableRecord;
      // for each entity on this block table record
      foreach (ObjectId entId in btr)
      {
        Entity ent = trans.GetObject(entId,
          OpenMode.ForRead) as Entity;
        if ((ent.IsAProxy))
        {
          ent.UpgradeOpen();
          ent.Erase();
          Application.DocumentManager.
            MdiActiveDocument.Editor.WriteMessage(
              string.Format(
              "\nProxy entity found: {0}",
              ent.GetType().Name));
        }
      }
    }
      // now search for NOD proxy entries
    DBDictionary nod = trans.GetObject(
      db.NamedObjectsDictionaryId,
      OpenMode.ForRead) as DBDictionary;
    searchSubDictionary(trans, nod);
    trans.Commit();
  }
    // the HandOverTo operation must
  // be perfomed outside transactions
  foreach (ObjectId nodID in _NODEntriesForErase)
  {
    //replace with an empty Dic Entry
    DBDictionary newNODEntry = new DBDictionary();
    DBObject NODEntry = nodID.Open(OpenMode.ForWrite);
    try
    {
      NODEntry.HandOverTo(newNODEntry, true, true);
    }
    catch (Autodesk.AutoCAD.Runtime.Exception ex) { }
      // if we cannot close the OLD entry,
    // then is not database resident
    try { NODEntry.Close(); }
    catch { Application.DocumentManager.
      MdiActiveDocument.Editor.
      WriteMessage("\nErased"); }
      //close the new one
    try { newNODEntry.Close(); }
    catch { }
  }
}
  private static ObjectIdCollection
  _NODEntriesForErase;
  private static void searchSubDictionary(
  Transaction trans, DBDictionary dic)
{
  foreach (DBDictionaryEntry dicEntry in dic)
  {
    DBObject subDicObj = trans.GetObject(
      dicEntry.Value, OpenMode.ForRead);
    if (subDicObj.IsAProxy)
    {
      Application.DocumentManager.
        MdiActiveDocument.Editor.WriteMessage(
          string.Format(
          "\nProxy found at key {0}",
          dicEntry.Key));
      subDicObj.UpgradeOpen();
        // for several Proxy Entities the
      // Erase is not allowed withyou the
      // Object Enabler throw an exception,
      // just treat
      try { subDicObj.Erase(); continue; }
      catch
      {
        Application.DocumentManager.
          MdiActiveDocument.Editor.
          WriteMessage(" | Erase not allowed");
        //try again latter
        _NODEntriesForErase.Add(subDicObj.ObjectId);
      }
    }
    else
    {
      //if this key is not proxy, let go into sub keys
      DBDictionary subDic =
        subDicObj as DBDictionary;
      if (subDic != null)
        searchSubDictionary(trans, subDic);
    }
  }
}

## 评论

**内容**: Alexander Rivilis said...
Hi, Augusto!
But proxy object can be owned not only NOD...
Maybe more useful will be direct scan Database from Database.BlockTableId.Handle to Database.Handseed, check every object and erase if proxy.
What do you think about that algorithm? I've used it more then 10 years with ObjectARX.
Reply
04/11/2013 at 12:15 PM

---
**内容**: Augusto Goncalves said in reply to Alexander Rivilis...
Alexander,
So you are going to the list of object directly...sounds good to. I just like the AutoCAD database structure, so I followed it :)
Thanks for sharing.
Cheers,
Augusto Goncalves
Reply
04/11/2013 at 12:44 PM

---
