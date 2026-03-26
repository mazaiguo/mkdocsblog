---
title: "Retrieving the original path of an Xref, even if it is unresolved using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Database
  - ObjectARX
  - XREF
description: "There are 2 ways to get the original path, using acdbOriginalXrefFullPathFor() or scanning the Block Table."
author: Autodesk
---
# Retrieving the original path of an Xref, even if it is unresolved using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/retrieving-the-original-path-of-an-xref-even-if-it-is-unresolved-using-objectarx.html

## 文章内容

By Gopinath Taget
There are 2 ways to get the original path, using acdbOriginalXrefFullPathFor() or scanning the Block Table.
There is a slight problem using acdbOriginalXrefFullPathFor() though. If the XRef's being scanned are unresolved, you won't be able to get the path because you won't be able to get a valid AcDbDatabase to pass to acdbOriginalXrefFullPathFor() function. Here's the code anyway in case unresolved XRef's are not a problem to you:
//////////////////////////////////////////
// This is command 'TEST3'
void asdktest3()
{
AcDbXrefGraph graph;
 // get a graph of all the xrefs
 if (acedGetCurDwgXrefGraph (graph) == Acad::eOk)
{
  // save the number of nodes for our loop later
  int numNodes = graph.numNodes ();
  // a little test to see if it worked
  acutPrintf (_T("\nNumber of nodes = %d"), numNodes);
  // loop round and extract the xref filepaths
  for (int i=0; i<numNodes; ++i)
  {
   // extract the ith node
   AcDbXrefGraphNode *node = graph.xrefNode (i);
   // if ok
   if (node != NULL)
   {
    // get the xref database
    AcDbDatabase *xrefDb = node->database ();
    // if the xref is resolved
    if (xrefDb != NULL)
    {
     // get the orginal filepath for this xref,
     const TCHAR *xrefPathName =
      acdbOriginalXrefFullPathFor (xrefDb);
     // if ok
     if (xrefPathName != NULL)
      acutPrintf (
      _T("\n\tXRef filepath = %s"), xrefPathName);
     // means this is the current drawing
     else
      acutPrintf (
      _T("\n\tXRef %s - no path saved"), node->name());
    }
    // no database means that the xref is unresolved
    else
    {
     acutPrintf (
      _T("\nXRef %s is unresolved"), node->name());
    }
   }
   // display if is nested
   acutPrintf (
    _T(" is nested = %d"), node->isNested ());
  }
}
}
The best way to get the original path of an XRef, for both resolved and unresolved XRefs, is to use the Block Table Record. However, there is one drawback with this approach. It will not return the filepath if the "Retain Path" check box in "External Reference" dialog is not set on while inserting the Xref.  Here is the code:
  ////////////////////////////////////
// This is command 'TEST2'
void asdktest2()
{
AcDbXrefGraph graph;
 // get a graph of all the xrefs
 if (acedGetCurDwgXrefGraph (graph) == Acad::eOk)
{
  // save the number of nodes for our loop later
  int numNodes = graph.numNodes ();
  // a little test to see if it worked  
  acutPrintf (
   _T("\nNumber of nodes = %d"), numNodes);
    // loop round and extract the xref filepaths
  for (int i=0; i<numNodes; ++i)
  {
   // extract the ith node
   AcDbXrefGraphNode *node = graph.xrefNode (i);
   // if ok
   if (node != NULL)
   {
    // get the current db
    AcDbDatabase *db =
     acdbHostApplicationServices ()->workingDatabase ();
      acutPrintf (
     _T("\n\tXRef filename = %s"), node->name ());
      AcDbBlockTable *blockTable = NULL;
    // get a pointer to the block table
    Acad::ErrorStatus es =
     db->getBlockTable (blockTable, AcDb::kForRead);
    // if ok
    if (es == Acad::eOk)
    {
     AcDbBlockTableRecord *blockTableRecord = NULL;
     // now get a pointer to the model space entity records
     es = blockTable->getAt (
      node->name (), blockTableRecord, AcDb::kForRead);
     // can close the block table itself
     // as we don't need it anymore
     blockTable->close ();
     // if ok
     if (es == Acad::eOk)
     {
      TCHAR *xrefPathName = NULL;
      // now get the path
      es = blockTableRecord->pathName (xrefPathName);
      // if ok
      if (es == Acad::eOk)
      {
       acutPrintf (
        _T("\n\tXRef filepath = %s"), xrefPathName);
      }
      // now clear up
      blockTableRecord->close ();
     }
    }
   }
  }
}
}

