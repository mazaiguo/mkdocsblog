---
title: "Extracting XML data of selected objects from current drawing using .NET"
date: 2016-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "Here is a blog by Kean Walmsley, which demonstrates Extracting XML data from drawings."
author: Autodesk
---
# Extracting XML data of selected objects from current drawing using .NET

发布日期: 2016-10-01

原始链接: https://adndevblog.typepad.com/autocad/2016/10/extracting-xml-data-of-selected-objects-from-current-drawing-using-net.html

## 文章内容

By Deepak Nadig
Here is a blog by Kean Walmsley, which demonstrates Extracting XML data from drawings.
To extract data from the selected objects of current drawing, following modification to the code in the Kean's blog is required :
1) Current drawing name and path can be used in place of that of the external file.
2) Create a List<Handle> of selected objects.
2) The List<Handle> of selected objects to be assigned to the API "IDxDrawingDataExtractor.Settings.SelectedObjects"
Here is the modified code: 
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.EditorInput;
using System.Collections;
using System.Collections.Specialized;
using System.Collections.Generic;
using Autodesk.AutoCAD.DataExtraction;
using System.IO;
namespace DataExtraction
{
// This class is instantiated by AutoCAD for each document when
 // a command is called by the user the first time in the context
 // of a given document. In other words, non static data in this class
 // is implicitly per-document!
 public class MyCommands
 {
 const string outputXmlFile =
 @"c:\temp\ExtAttr.xml";
[CommandMethod("extd")]
 public void extractData()
 {
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
 string fileName = Path.GetFileName(doc.Name); 
 string path = Path.GetDirectoryName(doc.Name) + "\\";
try
 {
 if (!System.IO.File.Exists(path + fileName))
 {
 ed.WriteMessage("\nFile does not exist.");
 return;
 }
//List to get handle of all the selected objects
 List<Handle> selObjsHandle = new List<Handle>();
PromptSelectionResult selectionRes = ed.SelectImplied();
 // If there's no pickfirst set available...
 if (selectionRes.Status == PromptStatus.Error)
 {
 // ... ask the user to select entities
 PromptSelectionOptions selectionOpts = new PromptSelectionOptions();
 selectionOpts.MessageForAdding = "\nSelect objects to extract data: ";
 selectionRes = ed.GetSelection(selectionOpts);
 }
 else
 {
 // If there was a pickfirst set, clear it
 ed.SetImpliedSelection(new ObjectId[0]);
 }
// If the user has not cancelled...
 if (selectionRes.Status == PromptStatus.OK)
 {
 // ... take the selected objects one by one
 Transaction tr =
 doc.TransactionManager.StartTransaction();
 try
 {
 ObjectId[] objIds =
 selectionRes.Value.GetObjectIds();
 foreach (ObjectId objId in objIds)
 {
DBObject obj =
 tr.GetObject(objId, OpenMode.ForRead);
 Entity ent = (Entity)obj;
 // This time access the properties directly
 ed.WriteMessage("\n Handle: " + ent.Handle.ToString());
 selObjsHandle.Add(ent.Handle);
 obj.Dispose();
 }
 // Although no changes were made, use Commit()
 // as this is much quicker than rolling back
 tr.Commit();
 }
 catch (Autodesk.AutoCAD.Runtime.Exception ex)
 {
 ed.WriteMessage(ex.Message);
 tr.Abort();
 }
 }
// Create some settings for the extraction
IDxExtractionSettings es =
 new DxExtractionSettings();
IDxDrawingDataExtractor de =
 es.DrawingDataExtractor;
de.Settings.ExtractFlags =
 ExtractFlags.ModelSpaceOnly |
 ExtractFlags.XrefDependent |
 ExtractFlags.Nested;
// Add a single file to the settings
IDxFileReference fr =
 new DxFileReference(path, path + fileName);
de.Settings.DrawingList.AddFile(fr);
//selected objects handle list assigned to IDxDrawingDataExtractor
 de.Settings.SelectedObjects = selObjsHandle;
// Scan the drawing for object types & their properties
 de.DiscoverTypesAndProperties(path);
List<IDxTypeDescriptor> types = de.DiscoveredTypesAndProperties;
// Select all the types and properties for extraction
 // by adding them one-by-one to these two lists
List<string> selTypes = new List<string>();
 List<string> selProps = new List<string>();
foreach (IDxTypeDescriptor type in types)
 {
 selTypes.Add(type.GlobalName);
 foreach (
 IDxPropertyDescriptor pr in type.Properties
 )
 {
 if (!selProps.Contains(pr.GlobalName))
 selProps.Add(pr.GlobalName);
 }
 }
// Pass this information to the extractor
 de.Settings.SetSelectedTypesAndProperties(
 types,
 selTypes,
 selProps
 );
// Now perform the extraction itself
 de.ExtractData(path);
// Get the results of the extraction
 System.Data.DataTable dataTable =
 de.ExtractedData;
// Output the extracted data to an XML file
if (dataTable.Rows.Count > 0)
 {
 dataTable.TableName = "My_Data_Extract";
 dataTable.WriteXml(outputXmlFile);
 }
}
 catch (Autodesk.AutoCAD.Runtime.Exception ex)
 {
 ed.WriteMessage(ex.Message);
 }
 }
}
}

