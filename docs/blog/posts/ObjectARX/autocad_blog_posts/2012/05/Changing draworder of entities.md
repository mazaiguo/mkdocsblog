---
title: "Changing draworder of entities"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Unicode
description: "An MText with background mask set can hide entities that are behind it. To send the MText to the back and make the entity behind it to be visible, ..."
author: Autodesk
---
# Changing draworder of entities

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/changing-draworder-of-entities.html

## 文章内容

By Balaji Ramamoorthy
An MText with background mask set can hide entities that are behind it. To send the MText to the back and make the entity behind it to be visible, we can set the DrawOrder in AutoCAD using the context menu option. This can also be achieved programmatically for an entity.
Here is a sample code to send a selected entity behind. i.e., change the draworder of the selected entity to bottom.
Using ObjectARX :
static void ADSProjectSendToBottom(void)
{
    ads_name ent;
    ads_point pt;
      Acad::ErrorStatus es;
    int ret = RTNORM;
    ret = acedEntSel(    _T("\nSelect Entity: "),
                ent,
                pt
              );
      if (RTNORM != ret)
        return;
      AcDbObjectId ent_id;
    if (Acad::eOk != acdbGetObjectId( ent_id, ent ))
        return;
      configureSortents();
      AcDbEntity *pEnt;
    es = acdbOpenObject( pEnt, ent_id, AcDb::kForRead );
    if (Acad::eOk != es)
        return;
      AcDbSortentsTable *pSt = GetSortentsTableOf( pEnt );
      pEnt->close();
    if (NULL == pSt)
        return;
      AcDbObjectIdArray entity_array;
    entity_array.append( ent_id );
      pSt->moveToBottom( entity_array );
    pSt->close();
      // Send regen command or use the
    // undocumented ads_regen method.
    acDocManager->sendStringToExecute
                            (
                                acDocManager->curDocument(),
                                L"_regen\n",
                                false,
                                true
                            );
}
Using AutoCAD .Net API :
[CommandMethod("SendToBottom")]
public void commandDrawOrderChange()
{
    Document activeDoc
                = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      PromptEntityOptions peo
                = new PromptEntityOptions("Select an entity : ");
    PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status != PromptStatus.OK)
    {
        return;
    }
    ObjectId oid = per.ObjectId;
      SortedList<long, ObjectId> drawOrder
                            = new SortedList<long, ObjectId>();
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = tr.GetObject(   
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
        BlockTableRecord btrModelSpace =
                tr.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForRead
                            ) as BlockTableRecord;
          DrawOrderTable dot =
                tr.GetObject(
                                btrModelSpace.DrawOrderTableId,
                                OpenMode.ForWrite
                            ) as DrawOrderTable;
          ObjectIdCollection objToMove = new ObjectIdCollection();
        objToMove.Add(oid);
        dot.MoveToBottom(objToMove);
          tr.Commit();
    }
    ed.WriteMessage("Done");
}

## 评论

**内容**: Account Deleted said...
Hi Balaji!
It specifically did you write such a complex code to ObjectARX, and so simple in C#?
With the help of ObjectARX code can be as laconic as using C#. For example:
static void MoveBelow(AcDbObjectId &idDown, AcDbObjectId &idUp)
{
AcDbSortentsTable *pSortTab = NULL;
AcDbObjectId spaceId = AcDbObjectId::kNull;
AcDbEntityPointer pEnt(idDown,AcDb::kForRead);
if (pEnt.openStatus() == Acad::eOk) {
spaceId = pEnt->ownerId();
pEnt->close();
}
if (!spaceId.isNull()) {
AcDbObjectPointer pBTR(spaceId,AcDb::kForRead);
if (pBTR.openStatus() == Acad::eOk) {
if (pBTR->getSortentsTable(pSortTab, AcDb::kForWrite, true) == Acad::eOk) {
AcDbObjectIdArray ar; ar.append(idDown);
pSortTab->moveBelow(ar,idUp);
pSortTab->close();
}
}
}
}
Reply
05/10/2012 at 09:49 PM

---
**内容**: Balaji said...
Hi Alexander,
The C# sample is from my recent reply to a developer while the ObjectARX one is a bit old. I did not attempt to make them look similar. Thanks for your sample code. I will update the post.
Reply
05/10/2012 at 10:15 PM

---
**内容**: petcon said...
用点心
Reply
05/10/2012 at 10:51 PM

---
**内容**: Balaji said...
I used Google translate and got this "用点心" = "A Snack".
Thanks to petcon, I am learning chinese :)
Reply
05/10/2012 at 10:57 PM

---
**内容**: Norman Yuan said...
Well, you cannot trust Google translator (or any electronic/onlne translator, for that matter) in this case.
the cobination of the 3 Chinese characters can have different meanings, depending on the context when it is used.
In this particular case, petcon' really meant to ask to be more CAREFUL, or have more thought on what you were posting.
It only means to have some snack when someone points at some snack to you.
Reply
05/11/2012 at 02:11 PM

---
**内容**: Balaji said...
Thanks Norman :)
I get it now, and will be careful in future.
BTW the ObjectARX code that I posted does work. Anyway, I will be reposting the ObjectARX code to make it simpler.
Thanks again for explaining what those 3 chinese letters meant :)

Reply
05/11/2012 at 06:49 PM

---
**内容**: Account Deleted said...
Hi Balaji!
Another idea. What about not using asynchronous sendStringToExecute method but using ads_regen function: http://adn.autodesk.com/adn/servlet/devnote?siteID=4814862&id=11845587&linkID=4900509 ?
Reply
05/13/2012 at 02:51 AM

---
**内容**: Balaji said...
Thank you.
Reply
05/14/2012 at 10:39 PM

---
**内容**: Anonymoose said...
SortedList drawOrder = new SortedList();
I don't see the SortedList used anywhere. Is there some other code missing?
Reply
06/03/2012 at 10:02 AM

---
**内容**: Eddy Lucas said...
Thanks, i used this C# code and it worked good
Reply
02/10/2023 at 09:49 AM

---
**内容**: Amanda The Adventurer said...
This code assumes you are working with AutoCAD's ObjectARX/VLAX interface. If you are using a different programming language or API, the syntax and method calls may vary.
Reply
06/26/2023 at 12:57 AM

---
