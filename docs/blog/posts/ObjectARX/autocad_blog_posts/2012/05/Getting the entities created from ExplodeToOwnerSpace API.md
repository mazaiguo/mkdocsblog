---
title: "Getting the entities created from ExplodeToOwnerSpace API"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "You can use database reactor to identify the entities created due to the call of “ExplodeToOwnerSpace”. Refer below code, which adds a “ObjectAppen..."
author: Autodesk
---
# Getting the entities created from ExplodeToOwnerSpace API

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/getting-the-entities-created-from-explodetoownerspace-api.html

## 文章内容

By Virupaksha Aithal
You can use database reactor to identify the entities created due to the call of “ExplodeToOwnerSpace”. Refer below code, which adds a “ObjectAppended” event callback just before calling “ExplodeToOwnerSpace”. The event callback is removed after the call to “ExplodeToOwnerSpace”. An “ObjectIdCollection” is populated inside the “ObjectAppended” callback which can be used to determine the objects added in “ExplodeToOwnerSpace” API
static ObjectIdCollection ids = new ObjectIdCollection();
  [CommandMethod("ExplodeToOwnerSpace")]
public static void ExplodeToOwnerSpace()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
              new PromptEntityOptions("\nSelect block reference");
    options.SetRejectMessage("\nSelect only block reference");
    options.AddAllowedClass(typeof(BlockReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      using (Transaction tx =
                        db.TransactionManager.StartTransaction())
    {
        BlockReference blockRef = tx.GetObject(acSSPrompt.ObjectId,
                               OpenMode.ForRead) as BlockReference;
        //add event
        ids.Clear();
        db.ObjectAppended +=
                        new ObjectEventHandler(db_ObjectAppended);
        blockRef.ExplodeToOwnerSpace();
        //remove event
        db.ObjectAppended -=
                        new ObjectEventHandler(db_ObjectAppended);
          foreach (ObjectId id in ids)
        {
            //get each entity....
            ed.WriteMessage("\n" + id.ToString());
        }
          tx.Commit();
    }
}
  static void db_ObjectAppended(object sender, ObjectEventArgs e)
{
    //add the object id
    ids.Add(e.DBObject.ObjectId);
}

## 评论

**内容**: Matus Brlit said...
I was exploding the block using blockRef.Explode(DBObjectCollection) and then adding those objects to the database
this looks much better
Reply
06/01/2012 at 10:11 AM

---
**内容**: David said...
Hi Virupaksha.
Thanks for post.
If block is an overrulled block, using your code and even using blockRef.Explode methos will explode the original block to original state not overruled state.
I had overrule explode class for that block, which works fine from within command line, using Explode command. But I want to be able to explode the overrulled block from code . How could I achieve this?
Thanks.
Davdi.
Reply
07/19/2012 at 03:57 PM

---
**内容**: Virupaksha Aithal said...
Hi,
try below code... code adds a circle to me retaining the original block reference.
class Myexplode : TransformOverrule
{
public override void Explode(Entity entity, DBObjectCollection entitySet)
{
//Just 1 circle..
Circle cir = new Circle(Point3d.Origin, Vector3d.ZAxis, 10);
entitySet.Add(cir);
//base.Explode(entity, entitySet);
}
}
[CommandMethod("explodeRef")]
static public void explodeRef()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
PromptEntityOptions options =
new PromptEntityOptions("\nSelect block reference");
options.SetRejectMessage("\nSelect only block reference");
options.AddAllowedClass(typeof(BlockReference), false);
Myexplode test = new Myexplode();
Overrule.AddOverrule(RXObject.GetClass(typeof(BlockReference)), test, true);
Overrule.Overruling = true;
PromptEntityResult acSSPrompt =
ed.GetEntity(options);
using (Transaction tx =
db.TransactionManager.StartTransaction())
{
BlockReference blockRef = tx.GetObject(acSSPrompt.ObjectId,
OpenMode.ForRead) as BlockReference;
DBObjectCollection entitySet = new DBObjectCollection();
blockRef.Explode(entitySet);
BlockTableRecord table = (BlockTableRecord)tx.GetObject(
db.CurrentSpaceId, OpenMode.ForWrite);
foreach (DBObject obj in entitySet)
{
if (obj is Entity)
{
table.AppendEntity((Entity)obj);
tx.AddNewlyCreatedDBObject(obj, true);
}
}
tx.Commit();
}
Overrule.RemoveOverrule(RXObject.GetClass(typeof(BlockReference)), test);
test.Dispose();
}
Reply
07/23/2012 at 02:37 AM

---
**内容**: David said in reply to Virupaksha Aithal...
Hi .
Thanks , It worked like a charm and it was exactly what I needed. Thanks for your time .
I am a big fan now.
David
Reply
07/24/2012 at 05:27 AM

---
**内容**: Hermann Weiß said...
How can I make the DrawOrderTable the resolved parts again?
Reply
07/08/2014 at 05:14 AM

---
