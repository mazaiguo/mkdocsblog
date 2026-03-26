---
title: "Tracking entity handles through BEDIT"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "Entity handles in AutoCAD are unique within a database, but AutoCAD can still change them while still retaining them as unique. Block editing using..."
author: Autodesk
---
# Tracking entity handles through BEDIT

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/tracking-entity-handles-through-bedit.html

## 文章内容

By Balaji Ramamoorthy
Entity handles in AutoCAD are unique within a database, but AutoCAD can still change them while still retaining them as unique. Block editing using BEDIT command is one such operation where you can expect the handle values to change. If your code is holding handle values of entities within a BlockTableRecord, you may be interested in tracking the handle values as they get changed during block editing.
Here is a sample code that monitors a few events to keep track of the handle values.
 private  static  String _blockName = "Test" ;
   private  static  ObjectIdCollection _idsToMonitor 
      = new  ObjectIdCollection();
   private  static  Dictionary<long , long > _idMap 
     = new  Dictionary<long , long >();
   [CommandMethod("StartTracking" )]
 public  void  StartTracking()
 {
     CreateBlockDef();
       Document activeDoc 
   = Application.DocumentManager.MdiActiveDocument;
       activeDoc.CommandWillStart 
   +=new  CommandEventHandler(activeDoc_CommandWillStart);
       activeDoc.CommandEnded 
   +=new  CommandEventHandler(activeDoc_CommandEnded);
       Database db = activeDoc.Database;
        db.BeginDeepCloneTranslation 
  += new  IdMappingEventHandler(db_BeginDeepCloneTranslation);
        db.ObjectErased 
   += new  ObjectErasedEventHandler(db_ObjectErased);
 }
   void  activeDoc_CommandEnded(object sender, CommandEventArgs e)
 {
     String cmdName = e.GlobalCommandName;
     if (cmdName.Equals("BCLOSE" ))
     {
         Document activeDoc 
    = Application.DocumentManager.MdiActiveDocument;
         Database db = activeDoc.Database;
         // Check if the ObjectId exist 
         int  i = 0;
         foreach (ObjectId id in _idsToMonitor)
         {
             bool  findReplacement 
     = id.IsErased || id.IsEffectivelyErased;
               if (findReplacement)
             { // Has changed. Find the new one. 
                 if  (_idMap.ContainsKey(id.Handle.Value))
                 {
                     Handle newHandle 
       = new  Handle(_idMap[id.Handle.Value]);
                       ObjectId newId = ObjectId.Null;
                     if  (db.TryGetObjectId(newHandle, 
           out newId))
                     {
                         // New Id Exists 
                         _idsToMonitor[i] = newId;
                           activeDoc.Editor.WriteMessage(
                           String.Format(
       "{0} {1} mapped to {2} {3}" , 
                         Environment.NewLine, 
                         id.Handle, 
                         newId.Handle, 
                         (newId.IsEffectivelyErased 
       || newId.IsErased) ?
                         "Erased"  : String.Empty)
               );
                     }
                     else 
                     {
                         // Cannot determine the new handle !! 
                         activeDoc.Editor.WriteMessage(
                         "Sorry, Cannot find the new handle !!" );
                     }
                 }
                 else 
                 { 
                     // Cannot determine the new handle !! 
                     activeDoc.Editor.WriteMessage(
                     "Sorry, Cannot find the new handle !!" );
                 }
             }
             i++;
         }
           // New set of ids to monitor 
         _idsToMonitor.Clear();
         using  (Transaction tr 
    = db.TransactionManager.StartTransaction())
         {
             BlockTable bt 
     = tr.GetObject(db.BlockTableId, OpenMode.ForRead)
     as BlockTable;
               if  (bt.Has(_blockName))
             {
                 BlockTableRecord btr 
     = tr.GetObject(bt[_blockName], OpenMode.ForRead)
     as BlockTableRecord;
                   foreach (ObjectId id in btr)
                 {
                     _idsToMonitor.Add(id);
                 }
             }
             tr.Commit();
         }
     }
 }
   void  activeDoc_CommandWillStart(
  object sender, CommandEventArgs e)
 {
     String cmdName = e.GlobalCommandName;
     if  (cmdName.Equals("BEDIT" ))
     {
         _idMap.Clear();
     }
 }
   [CommandMethod("EndTracking" )]
 public  void  EndTracking()
 {
     Database db 
   = Application.DocumentManager.MdiActiveDocument.Database;
       db.BeginDeepCloneTranslation 
   -= new  IdMappingEventHandler(db_BeginDeepCloneTranslation);
       db.ObjectErased 
   -= new  ObjectErasedEventHandler(db_ObjectErased);
 }
   static  void  db_BeginDeepCloneTranslation(
     object sender, IdMappingEventArgs e)
 {
     foreach (ObjectId id in _idsToMonitor)
     {
         if  (e.IdMapping.Contains(id))
         {
             Editor ed 
    = Application.DocumentManager.MdiActiveDocument.Editor;
               IdPair idPair = e.IdMapping[id];
             _idMap.Add(
     idPair.Key.Handle.Value, 
     idPair.Value.Handle.Value);
               ed.WriteMessage(
     String.Format("{0} {1} mapped to {2}" , 
     Environment.NewLine, 
     idPair.Key.Handle, 
     idPair.Value.Handle));
         }
     }
 }
   void  db_ObjectErased(object sender, ObjectErasedEventArgs e)
 {
     foreach (ObjectId id in _idsToMonitor)
     {
         if  (e.DBObject.ObjectId.Equals(id))
         {
             Editor ed 
    = Application.DocumentManager.MdiActiveDocument.Editor;
               ed.WriteMessage(String.Format("{0} {1} erased" , 
     Environment.NewLine, id.Handle));
         }
     }
       foreach(KeyValuePair<long , long > kvp in _idMap)
     {
         if (e.DBObject.ObjectId.Handle.Value.Equals(kvp.Value))
         {
             Editor ed 
     = Application.DocumentManager.MdiActiveDocument.Editor;
               ed.WriteMessage(String.Format("{0} {1} erased" , 
     Environment.NewLine, kvp.Value.ToString("X" )));
         }
     }
 }
   public  static  void  CreateBlockDef()
 {
     Document activeDoc 
   = Application.DocumentManager.MdiActiveDocument;
     Database db = activeDoc.Database;
     Editor ed 
  = Application.DocumentManager.MdiActiveDocument.Editor;
       _idsToMonitor.Clear();
       using  (Transaction tr 
   = db.TransactionManager.StartTransaction())
     {
         BlockTable bt = tr.GetObject(
    db.BlockTableId, OpenMode.ForRead) as BlockTable;
           if  (bt.Has(_blockName) == false )
         {
             bt.UpgradeOpen();
             BlockTableRecord btr = new  BlockTableRecord();
             btr.Name = _blockName;
             btr.Origin = Point3d.Origin;
             bt.Add(btr);
             tr.AddNewlyCreatedDBObject(btr, true );
               ObjectId id = ObjectId.Null;
               Circle c1 = new  Circle(
     Point3d.Origin, 
     Vector3d.ZAxis, 1.0);
               id = btr.AppendEntity(c1);
             _idsToMonitor.Add(id);
             tr.AddNewlyCreatedDBObject(c1, true );
               Circle c2 = new  Circle(
     Point3d.Origin, 
     Vector3d.ZAxis, 2.0);
               id = btr.AppendEntity(c2);
             _idsToMonitor.Add(id);
             tr.AddNewlyCreatedDBObject(c2, true );
         }
   else 
   {
    BlockTableRecord btr 
     = tr.GetObject(bt[_blockName], OpenMode.ForRead)
     as BlockTableRecord;
               foreach (ObjectId id in btr)
             {
                 _idsToMonitor.Add(id);
             }
   }
           tr.Commit();
     }
 }
  To try this code, open a new drawing in AutoCAD and run "StartTracking" command. Now "BEDIT" the newly created "Test" block. Watch out for messages in the command line to track the entity handles. Here is a sample output in the command line during my test, although the actual handle values can vary in your case.

## 评论

**内容**: Dru said...
This is interesting I thought that handles never changed and they were "safe" to use when tracking objects between the file being open.
So if you had an app tracking handles and tried to do a sync between known handles and what is existing in the drawing you could end up thinking that they are deleted when really they have just been bedit'ed?
I am guessing I know the answer to this already but there is no mechanism in the API to track an object/entity definitely without condition between drawing open/close?
Reply
01/21/2015 at 10:04 AM

---
**内容**: Balaji said...
Hi Dru,
I am not aware of any other built-in mechanism to track it.
You can try using DBObject events, but I wanted to only track the changes during the BEDIT operation.
The reason for that being, BEDIT is the only operation that i know which changes the handle, so it may not be worth to have DBObject events subscribed all the time.
Regards,
Balaji
Reply
01/21/2015 at 08:54 PM

---
**内容**: Sanjoy Nath said...
Hi Balaji,
This is interesting , but in Autodesk AdvanceSteel For every command Seperate COM process starts and that modifies many Objects togather .So this Code hangs when we close those Joint Box (COM interfaces)
What Precautions should we take
When Model Browser is opened this mechanism hangs and Model Browser Goes to Not Responding State
Regards
Sanjoy
Reply
09/14/2016 at 04:44 AM

---
