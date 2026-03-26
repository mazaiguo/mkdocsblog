---
title: "Importing Layer Filters"
date: 2014-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Layer
description: "Here is a sample code snippet to import layer filters including nested layer filters from another drawing. The layers that qualify the filters are ..."
author: Autodesk
---
# Importing Layer Filters

发布日期: 2014-06-01

原始链接: https://adndevblog.typepad.com/autocad/2014/06/importing-layer-filters.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code snippet to import layer filters including nested layer filters from another drawing. The layers that qualify the filters are also imported.
A sample drawing with a few nested layer filters that I tested this code with can be downloaded here.
Download Test
 using  Autodesk.AutoCAD.LayerManager;
   [CommandMethod ("ImportLayerFilters" )]
 public  static  void  ImportLayerFilters()
 {
     String filePath = @"D:\\\\Temp\\\\Test1.dwg" ;
     if  (!System.IO.File.Exists(filePath))
         return ;
       Document doc = Application.DocumentManager.MdiActiveDocument;
     Database destDb = doc.Database;
       LayerFilterTree lft = destDb.LayerFilters;
     using  (Database srcDb
                     = new  Database(false , false ))
     {
         srcDb.ReadDwgFile(
             filePath,
             FileOpenMode.OpenForReadAndAllShare,
             false , String.Empty);
           ImportNestedFilters(
             srcDb.LayerFilters.Root,
             lft.Root, srcDb, destDb);
     }
       destDb.LayerFilters = lft;
 }
   public  static  void  ImportNestedFilters(
                             LayerFilter srcFilter,
                             LayerFilter destFilter,
                             Database srcDb,
                             Database destDb)
 {
     using  (Transaction tr
         = srcDb.TransactionManager.StartTransaction())
     {
         LayerTable lt = tr.GetObject(
                         srcDb.LayerTableId,
                         OpenMode.ForRead, false )
                         as  LayerTable;
           foreach  (LayerFilter sf in  srcFilter.NestedFilters)
         {
             // Get the layers to be cloned to the dest db.  
             // Only those that are pass the filter  
             ObjectIdCollection layerIds
                                 = new  ObjectIdCollection();
             foreach  (ObjectId layerId in  lt)
             {
                 LayerTableRecord ltr = tr.GetObject(
                     layerId, OpenMode.ForRead, false )
                                 as  LayerTableRecord;
                   if  (sf.Filter(ltr))
                 {
                     layerIds.Add(layerId);
                 }
             }
               // clone the layers to the dest db  
             IdMapping idmap = new  IdMapping();
             if  (layerIds.Count > 0)
             {
                 srcDb.WblockCloneObjects(
                                 layerIds,
                                 destDb.LayerTableId,
                                 idmap,
                                 DuplicateRecordCloning.Replace,
                                 false );
             }
               // Find if a destination database already   
             // has a layer filter with the same name  
             LayerFilter df = null ;
             foreach  (LayerFilter f in  destFilter.NestedFilters)
             {
                 if  (f.Name.Equals(sf.Name))
                 {
                     df = f;
                     break ;
                 }
             }
               if  (df == null )
             {
                 if  (sf is  LayerGroup)
                 {
                     // create a new layer filter group  
                     // if nothing found  
                     LayerGroup sfgroup = sf as  LayerGroup;
                     LayerGroup dfgroup = new  LayerGroup();
                     dfgroup.Name = sf.Name;
                       df = dfgroup;
                       LayerCollection lyrs = sfgroup.LayerIds;
                     foreach  (ObjectId lid in  lyrs)
                     {
                         if  (idmap.Contains(lid))
                         {
                             IdPair idp = idmap[lid];
                             dfgroup.LayerIds.Add(idp.Value);
                         }
                     }
                     destFilter.NestedFilters.Add(df);
                 }
                 else 
                 {
                     // create a new layer filter  
                     // if nothing found  
                     df = new  LayerFilter();
                     df.Name = sf.Name;
                     df.FilterExpression = sf.FilterExpression;
                     destFilter.NestedFilters.Add(df);
                 }
             }
               // Import other filters  
             ImportNestedFilters(sf, df, srcDb, destDb);
         }
         tr.Commit();
     }
 }

## 评论

**内容**: Dale Bartlett said...
Hi, I get an error on df = destFilter.NestedFilters.Cast()
LayerManager.LayerFilterCollection does not contain "Cast". Perhaps this is for 2015? I am using 2014 for the moment.
Reply
06/10/2014 at 05:44 AM

---
**内容**: Balaji said...
Hi Dale,
I am not sure why that fails. You can simply replace it using this for now. It simply finds if the destination filter with the same name already exists. If so, we will not create it again. This is needed for some of the default layer filters.
LayerFilter df = null;
foreach(LayerFilter f in destFilter.NestedFilters)
{
if(f.Name.equals(sf.Name))
{
df = f;
break;
}
}
Regards,
Balaji
Reply
06/10/2014 at 05:53 AM

---
**内容**: Matinau said...
I get the same error on the second loop, think the destFilter is still open.
Reply
06/10/2014 at 04:46 PM

---
**内容**: Balaji said in reply to Matinau...
I will review the code and get back to you.
Thanks
Balaji
Reply
06/10/2014 at 09:36 PM

---
**内容**: Balaji said in reply to Matinau...
Hi Matinau,
Can you please try the updated code.
Sorry, It was my mistake to have ignored Layer filter groups. The earlier code only considered the Layer property filters.
Regards,
Balaji
Reply
06/10/2014 at 10:19 PM

---
**内容**: JH said...
Is there a way to modify this so that it will not import the layers too?
Thanks
JH
Reply
03/06/2017 at 07:00 AM

---
