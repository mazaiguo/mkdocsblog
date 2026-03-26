---
title: "Create an anonymous group"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Database
description: "Anonymous groups can be created using the function “SetAt”, on the group dictionary. Please refer to the sample code shown below"
author: Autodesk
---
# Create an anonymous group

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/create-an-anonymous-group.html

## 文章内容

By Virupaksha Aithal
Anonymous groups can be created using the function “SetAt”, on the group dictionary. Please refer to the sample code shown below
  [CommandMethod("creatAnonymGroup")]
public void creatAnonymGroup()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
      PromptSelectionResult result = ed.GetSelection();
    if (result.Status != PromptStatus.OK)
        return;
      using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
          DBDictionary groupDic =
            (DBDictionary)Tx.GetObject(db.GroupDictionaryId,
                                              OpenMode.ForWrite);
        Group anonyGroup = new Group();
        groupDic.SetAt("*", anonyGroup);
          foreach (SelectedObject acSSObj in result.Value)
        {
            anonyGroup.Append(acSSObj.ObjectId);
        }
        //groupDic
        Tx.AddNewlyCreatedDBObject(anonyGroup, true);
          Tx.Commit();
    }
}

## 评论

**内容**: Maxence said...
Important note in the doc:
> Group plants persistent reactors on its entries when the entries are added to the group. To accomplish this, it must have an objectId. When the group is added to the group dictionary, it is also added to the database, and thus it obtains an objectId. Therefore, do not attempt to add entries to a newly created group before adding the group to the group dictionary.
So be carefull, add the group to the dictionnary first before appending entities. And from my experience, entities must be closed.
Reply
01/02/2013 at 08:09 AM

---
**内容**: James Maeding said...
what is groupDic.SetAnonymous() for?
Reply
07/12/2018 at 11:52 AM

---
