---
title: "How To Make MultiViewBlocks Annotative"
date: 2017-02-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
description: "Though the post is very much related to AutoCAD Architecture or MEP, I have taken little liberty to attract AutoCAD audience too"
author: Autodesk
---
# How To Make MultiViewBlocks Annotative

发布日期: 2017-02-01

原始链接: https://adndevblog.typepad.com/autocad/2017/02/how-to-make-multiviewblocks-annotative.html

## 文章内容

By Madhukar Moogala
Though the post is very much related to AutoCAD Architecture or MEP, I have taken little liberty to attract AutoCAD audience too
There isn’t a direct API to make annotative MVBlock, however if the internal ACAD block is annotative, same behaviour can be exposed to MVBlocks, we will get all referenced blocks and set annotation on each block which is an ACAD block.
[CommandMethod("MakeMVBlockAnnotative")]
        public static void makeMVBlockAnnotative()
        {
            /*You need to include AecBaseMgd reference from OMF SDK or available with ACA\MEP installations*/
            Document doc = Application.DocumentManager.MdiActiveDocument;
            Database db = doc.Database;
            Editor ed = doc.Editor;
            PromptEntityOptions peo = new PromptEntityOptions("Select a MVBlockreference");
            PromptEntityResult result = ed.GetEntity(peo);
            if (result.Status != PromptStatus.OK) return;
            try
            {
                using (Transaction tr =
                    db.TransactionManager.StartTransaction())
                {
                    MultiViewBlockReference mvBref = 
                        tr.GetObject(result.ObjectId, OpenMode.ForWrite) as MultiViewBlockReference;
                    MultiViewBlockDefinition mbBdef = 
                        tr.GetObject(mvBref.BlockDefId, OpenMode.ForWrite) as MultiViewBlockDefinition;
                    /*Each MVBlockDefination has various internal ACAD Blocks,
                     *  each such block holds view dependent entities                     
                     * If a internal ACAD Block has annotative behavior, 
                     * same can be exposed to mvblocks.                
                     
                     */

                    Autodesk.AutoCAD.DatabaseServices.ObjectIdCollection BrefIds =
                        mbBdef.GetAllBlocksReferenced();
                    /*Utility*/
                    printHandlesToEditor(BrefIds);
                    foreach(Autodesk.AutoCAD.DatabaseServices.ObjectId id in BrefIds)
                    {
                        BlockTableRecord btr = tr.GetObject(id, OpenMode.ForWrite) as BlockTableRecord;
                        btr.Annotative = AnnotativeStates.True;
                    }
                    BrefIds.Clear();
                    
                    bool status = mvBref.UpdateAnnotative();
                    tr.Commit();

                }
            }
            catch (System.Exception ex)
            {
                ed.WriteMessage(ex.ToString());
            }
        }
        /*Helper*/
        private static void printHandlesToEditor(Autodesk.AutoCAD.DatabaseServices.ObjectIdCollection ids)
        {
            Document doc = Application.DocumentManager.MdiActiveDocument;
            Database db = doc.Database;
            Editor ed = doc.Editor;
            foreach (Autodesk.AutoCAD.DatabaseServices.ObjectId id in ids)
            {
                Handle handle = id.Handle;
                ed.WriteMessage("\n" + handle.Value.ToString());
            }

        }

## 评论

**内容**: Hanauer said...
Cool to see new posts. AutoCAD, ACA and MEP still lives? The last post on the AEC Devblog was in 07/20/2016.
Reply
02/16/2017 at 02:08 AM

---
**内容**: Madhukar Moogala said in reply to Hanauer...

Typepad HTML Email

Pretty much!, they are not yet dead, in recent AU, our Engineering colleagues made a presentation on OMF.
  Thanks,
Madhu.
  Reply
02/16/2017 at 02:13 AM

---
