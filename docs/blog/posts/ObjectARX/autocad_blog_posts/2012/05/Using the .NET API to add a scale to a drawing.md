---
title: "Using the .NET API to add a scale to a drawing"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C#
  - Database
  - Unicode
description: "Below C# code shows the procedure to add a scale to scale list."
author: Autodesk
---
# Using the .NET API to add a scale to a drawing

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/using-the-net-api-to-add-a-scale-to-a-drawing.html

## 文章内容

By Virupaksha Aithal
Below C# code shows the procedure to add a scale to scale list.
[CommandMethod("AddScale")]
static public void addScale()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 // next get the objectContextManager           
 try
 {
     ObjectContextManager contextManager =
                                    db.ObjectContextManager;
     // if ok               
     if (contextManager != null)
     {
         // now get the Annotation Scaling context collection
         // (named ACDB_ANNOTATIONSCALES_COLLECTION)                   
         ObjectContextCollection contextCollection =
           contextManager.GetContextCollection(
                                    "ACDB_ANNOTATIONSCALES");
         // if ok                   
         if (contextCollection != null)
         {
             // create a brand new scale context                       
             AnnotationScale annotationScale =
                                    new AnnotationScale();
             annotationScale.Name = "WBScale2 1:28";
             annotationScale.PaperUnits = 1;
             annotationScale.DrawingUnits = 28;
             // now add to the drawing's context collection                       
             contextCollection.AddContext(annotationScale);
         }
     }
 }
 catch (System.Exception ex)
 {
     Editor ed = doc.Editor;
     ed.WriteMessage(ex.ToString());
 }
}

## 评论

**内容**: David Prontnicki said...
I have added a list of scales to this, how can this be modified to check if annoscale is there already and ignore if already exists?
Reply
04/04/2018 at 08:09 AM

---
**内容**: Alexandre said in reply to David Prontnicki...
if !(contextCollection.hascontext(annotationScale.Name)) contextCollection.AddContext(annotationScale);
Reply
07/19/2023 at 04:20 PM

---
