---
title: "Iterating through the group dictionary"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below code shows the procedure to Iterating through the group dictionary. The code also shows the procedure to get entity ids from the groups."
author: Autodesk
---
# Iterating through the group dictionary

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/iterating-through-the-group-dictionary.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to Iterating through the group dictionary. The code also shows the procedure to get entity ids from the groups.
[CommandMethod("listGroup")]
static public void listGroup()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        DBDictionary groups = tr.GetObject(db.GroupDictionaryId,
                                   OpenMode.ForRead) as DBDictionary;
          foreach (DBDictionaryEntry entry in groups)
        {
            Group group = (Group)tr.GetObject(
                                entry.Value, OpenMode.ForRead);
            ObjectId[] ids = group.GetAllEntityIds();
              //check if the group is Anonymous
            //group.IsAnonymous;
              //get each entity in the group
            /*
            foreach (ObjectId id in ids)
            {
                //get each entity....
            }
            */
              ed.WriteMessage(group.Name + " contains "
                            + ids.Length.ToString() + " entity\n");
            }
          tr.Commit();
    }
}

