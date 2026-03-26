---
title: "Programmatically mimic the Burst command"
date: 2015-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - Unicode
description: "The "Burst" command from the express tools is quite useful when exploding block references with attributes. Unlike the usual explode command, it le..."
author: Autodesk
---
# Programmatically mimic the Burst command

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/programmatically-mimic-the-burst-command.html

## 文章内容

By Balaji Ramamoorthy
The "Burst" command from the express tools is quite useful when exploding block references with attributes. Unlike the usual explode command, it leaves the attributes unchanged when a block reference is exploded.
Here is a sample code to mimic the Burst command using the AutoCAD .Net API. It first explodes a block reference and replaces any attribute definitions in the exploded entity collection by a DBText.
 [CommandMethod("EB" , CommandFlags.UsePickSet)]
 public  void  ExplodeBock()
 {
     Document doc 
         = Application.DocumentManager.MdiActiveDocument;
     Editor ed = doc.Editor;
       PromptSelectionResult psr = ed.SelectImplied();
     if  (psr.Status != PromptStatus.OK)
     {
         ed.WriteMessage(@"Please select the  
         block references to explode and  
         then run the command" );
           return ;
     }
       using  (SelectionSet ss = psr.Value)
     {
         if  (ss.Count <= 0)
         {
             ed.WriteMessage(@"Please select the  
             block references to explode and  
             then run the command" );
               return ;
         }
           Database db = doc.Database;
         using  (Transaction tr 
             = db.TransactionManager.StartTransaction())
         {
               ObjectId msId 
             = SymbolUtilityServices.GetBlockModelSpaceId(db);
             BlockTableRecord ms = tr.GetObject(msId, 
                 OpenMode.ForWrite) as  BlockTableRecord;
               foreach  (SelectedObject selectedEnt in  ss)
             {
                 BlockReference blockRef = tr.GetObject(
                 selectedEnt.ObjectId, 
                 OpenMode.ForRead) as  BlockReference;
                   if  (blockRef != null )
                 {
                     DBObjectCollection toAddColl 
                             = new  DBObjectCollection();
                       BlockTableRecord blockDef 
                     = tr.GetObject(
                     blockRef.BlockTableRecord,
                     OpenMode.ForRead) as  BlockTableRecord;
                       // Create a text for const and  
                     // visible attributes 
                     foreach  (ObjectId entId in  blockDef)
                     {
                         if  (entId.ObjectClass.Name 
                             == "AcDbAttributeDefinition" )
                         {
                             AttributeDefinition attDef 
                             = tr.GetObject(entId, 
                             OpenMode.ForRead) 
                             as  AttributeDefinition;
                               if  ((attDef.Constant && 
                                 !attDef.Invisible))
                             {
                                 DBText text = new  DBText();
                                 text.Height = attDef.Height;
                                   text.TextString 
                                     = attDef.TextString;
                                   text.Position = 
                                 attDef.Position.TransformBy
                                 (blockRef.BlockTransform);
                                   toAddColl.Add(text);
                             }
                         }
                     }
                       // Create a text for non-const  
                     // and visible attributes 
                     foreach  (ObjectId attRefId 
                         in  blockRef.AttributeCollection)
                     {
                         AttributeReference attRef 
                         = tr.GetObject(attRefId, 
                         OpenMode.ForRead)
                         as  AttributeReference;
                           if  (attRef.Invisible == false )
                         {
                             DBText text = new  DBText();
                             text.Height = attRef.Height;
                               text.TextString 
                                 = attRef.TextString;
                               text.Position = attRef.Position;
                               toAddColl.Add(text);
                         }
                     }
                       // Get the entities from the  
                     // block reference 
                     // Attribute definitions have  
                     // been taken care of.. 
                     // So ignore them 
                     DBObjectCollection entityColl 
                     = new  DBObjectCollection();
                     blockRef.Explode(entityColl);
                     foreach  (Entity ent in  entityColl)
                     {
                         if  (! (ent is  AttributeDefinition))
                         {
                             toAddColl.Add(ent);
                         }
                     }
                       // Add the entities to modelspace 
                     foreach  (Entity ent in  toAddColl)
                     {
                         ms.AppendEntity(ent);
                         tr.AddNewlyCreatedDBObject
                         (ent, true );
                     }
                       // Erase the block reference 
                     blockRef.UpgradeOpen();
                     blockRef.Erase();
                   }
                   tr.Commit();
             }
         }
     }
 }

## 评论

**内容**: CAD bloke said...
Iterating through the AttributeReference collection will miss the Constant Attributes, they are only in the block definition, not in the BlockReference.AttributeCollection. You will get the constant Attribute definitions when you explode the block but they are not added to toAddColl when you iterate the AttributeReferences and they are not added to it after you explode the block.
Also "Then Else"? Is that an empty "Then" clause instead of a "Not"?
Reply
06/03/2015 at 08:23 PM

---
**内容**: Balaji said...
Thanks for pointing that out.
Yes, you are right and the code can still be improved.
I will try and get that done.
Meanwhile, if other readers want to include constant attributes, this blog post should help :
http://adndevblog.typepad.com/autocad/2012/07/constant-and-non-constant-block-attributes.html
Regards,
Balaji
Reply
06/03/2015 at 09:15 PM

---
**内容**: Alexander Rivilis said...
Russian translation of this post and C# sample: http://adn-cis.org/programmnaya-imitacziya-komandyi-burst.html
Reply
06/05/2015 at 01:05 AM

---
**内容**: Balaji said in reply to Alexander Rivilis...
Thanks CAD bloke and Alex
I have updated the code to consider constant and invisible attributes and switched over to C# as the blog post formatting made it difficult to copy the code directly.
Regards,
Balaji
Reply
06/06/2015 at 03:55 AM

---
