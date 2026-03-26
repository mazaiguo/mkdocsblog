---
title: "Creating and accessing layer filter information"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Database
  - Layer
description: "Here is a ObjectARX and .Net sample code to create and access the layer filters. A simple trick to know the layer filter expression that will suit ..."
author: Autodesk
---
# Creating and accessing layer filter information

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-and-accessing-layer-filter-information.html

## 文章内容

By Balaji Ramamoorthy
Here is a ObjectARX and .Net sample code to create and access the layer filters. A simple trick to know the layer filter expression that will suit your needs, is to create a layer filter in AutoCAD and use this code to find the filter expression for it. This can then be used in your code to create a new layer filter.
Using ObjectARX :
Acad::ErrorStatus es = Acad::eOk;
AcDbDatabase *pDb =
             acdbHostApplicationServices()->workingDatabase();
  AcLyLayerFilterManager *pLayerFilterManager =
                               aclyGetLayerFilterManager(pDb);
  AcLyLayerFilter *pRoot = NULL;
AcLyLayerFilter *pCurrent = NULL;
es = pLayerFilterManager->getFilters(pRoot, pCurrent);
if(es != Acad::eOk)
    return;
  if(pRoot != NULL)
{
    AcArray<AcLyLayerFilter *> filters;
    filters = pRoot->getNestedFilters();
      // Lets find out about the root filter
    acutPrintf
            (
                ACRX_T("\n(Root) Name : %s Expr : %s"),
                pRoot->name(),
                pRoot->filterExpression()
            );
      // Lets find out about all the filters
    for(int i=0; i < filters.length();i++)
    {
        acutPrintf
                (
                    ACRX_T("\nName : %s Expr : %s"),
                    filters.at(i)->name(),
                    filters.at(i)->filterExpression()
                );
    }
      // Lets find out about the current filter
    if(pCurrent != NULL)
    {
        acutPrintf
                (
                    ACRX_T("\n(Current) Name : %s Expr : %s"),
                    pCurrent->name(),
                    pCurrent->filterExpression()
                );
    }
      // Create and add a new layer filter
    AcLyLayerFilter *pMyLyFilter = new AcLyLayerFilter();
    pMyLyFilter->setName(ACRX_T("MyLyFilter"));
    pMyLyFilter->setFilterExpression(ACRX_T("NAME == \"*Test*\""));
      es = pRoot->addNested(pMyLyFilter);
    es = pLayerFilterManager->setFilters(pRoot, pMyLyFilter);
      delete pRoot;
}
Using AutoCAD .Net API :
using Autodesk.AutoCAD.LayerManager;
[CommandMethod("CreateLayerFilter")]
public void CreateLayerFilter()
{
    Document doc
                = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      LayerFilterTree filterTree = db.LayerFilters;
    LayerFilterCollection filters
                            = filterTree.Root.NestedFilters;
      // Lets find out about the root filter
    ed.WriteMessage
            (
                String.Format("\n(Root) Name : {0} Expr : {1}",
                db.LayerFilters.Root.Name,
                db.LayerFilters.Root.FilterExpression)
            );
      // Lets find out about all the filters
    foreach(LayerFilter f in filters)
    {
        ed.WriteMessage
                (
                    String.Format("\nName : {0} Expr : {1}",
                    f.Name,
                    f.FilterExpression)
                );
    }
      // Lets find out about the current filter
    if(db.LayerFilters.Current != null)
    {
        ed.WriteMessage
        (
            String.Format("\n(Current) Name : {0} Expr : {1}",
            db.LayerFilters.Current.Name,
            db.LayerFilters.Current.FilterExpression)
        );
    }
      // Create and add a new layer filter
    LayerFilter layerFilter = new LayerFilter();
    layerFilter.Name = "MyLyFilter";
    layerFilter.FilterExpression = "NAME == \"*Test*\"";
    filters.Add(layerFilter);
      // Set the changed layer filters tree to the database
    db.LayerFilters = filterTree;
}

## 评论

**内容**: Anonymoose said...
// Lets find out about all the filters
foreach(LayerFilter f in filters)
{
ed.WriteMessage
(
String.Format("\nName : {0} Expr : {1}",
f.Name,
f.FilterExpression)
);
}
This code does not find out about all the filters, only the immediate children of the root filter.
Reply
05/15/2012 at 07:08 PM

---
**内容**: petcon said...
how to create a layer filter
Reply
05/16/2012 at 04:33 AM

---
**内容**: joantopo said...
Hi.
How can I get layerId collection for each layerFilter?
LayerGroup has method "LayerIds" but that method doesn´t exist in LayerFilter.
Thank you.
Reply
11/01/2013 at 09:05 AM

---
**内容**: Craig said...
For 2014, Layergroup, which has a layers collection, is derived from LayerFilter so you should be able to cast it.
Reply
07/26/2016 at 06:12 AM

---
**内容**: layerfiter said...
It doesn't work.
You must closed the Layer manager windowform, then open it again , then you will see the new layerfiter just created.
if you don't close and open it . you will not see the layerfiter .
Reply
04/18/2018 at 01:45 AM

---
