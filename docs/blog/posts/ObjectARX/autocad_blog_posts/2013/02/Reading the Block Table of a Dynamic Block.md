---
title: "Reading the Block Table of a Dynamic Block"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - API
  - Block
description: "For a dynamic block we can create a Block Properties Table, which defines and controls values for parameters and properties. This is available when..."
author: Autodesk
---
# Reading the Block Table of a Dynamic Block

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/reading-the-block-table-of-a-dynamic-block.html

## 文章内容

By Augusto Goncalves
For a dynamic block we can create a Block Properties Table, which defines and controls values for parameters and properties. This is available when BEDIT’ing a dynamic block, as shown below.
From the API perspective, this data is stored under a DBDictionary called ACAD_ENHANCEDBLOCK. To access it, we need to use some ‘Internal’ APIs, which means that there is no documentation and it may change.
The following code sample show how to access it for a given selected BlockReference object. Minimal error check were done for simplicity.
[CommandMethod("readBlockTable")]
static public void CmdReadBlockTable()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
    // select a block reference
  PromptEntityOptions peo = new PromptEntityOptions(
    "Select a dynamic block reference: ");
  peo.SetRejectMessage("Only block reference");
  peo.AddAllowedClass(typeof(BlockReference), false);
  PromptEntityResult per = ed.GetEntity(peo);
  if (per.Status != PromptStatus.OK) return;
  ObjectId blockRefId = per.ObjectId;
    // get the database and start a transaction
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
  using (Transaction trans = db.
    TransactionManager.StartTransaction())
  {
    // open the dynamic block reference
    BlockReference blockRef = trans.GetObject(
      blockRefId, OpenMode.ForRead) as BlockReference;
    if (!blockRef.IsDynamicBlock) return;
      // get the dynamic block table definition
    BlockTableRecord blockDef = trans.GetObject(
      blockRef.DynamicBlockTableRecord,
      OpenMode.ForRead) as BlockTableRecord;
      // open the extension dictionary
    if (blockDef.ExtensionDictionary.IsNull) return;
    DBDictionary extDic = trans.GetObject(
      blockDef.ExtensionDictionary, OpenMode.ForRead)
      as DBDictionary;
      // open the ENHANCEDBLOCK dictionary
    Autodesk.AutoCAD.Internal.DatabaseServices.EvalGraph graph =
      trans.GetObject(extDic.GetAt("ACAD_ENHANCEDBLOCK"),
      OpenMode.ForRead) as EvalGraph;
      int[] nodeIds = graph.GetAllNodes();
    foreach (uint nodeId in nodeIds)
    {
      // open the node ID
      DBObject node = graph.GetNode(nodeId,
        OpenMode.ForRead, trans);
      // check is if the correct type
      if (!(node is BlockPropertiesTable)) continue;
      // convert the object
      BlockPropertiesTable table =
        node as BlockPropertiesTable;
        // ok, we have the data, let's show it...
        // get the number of columns
      int columns = table.Columns.Count;
      int currentRow = 0;
      foreach (
        BlockPropertiesTableRow row
        in table.Rows)
      {
        ed.WriteMessage("\n[{0}]:\t", currentRow);
        for (
          int currentColumn = 0;
          currentColumn < columns;
          currentColumn++)
        {
          // get the colum value for the
          // current row. May be more multiple
          TypedValue[] columnValue =
            row[currentColumn].AsArray();
          foreach (TypedValue tpVal in columnValue)
          {
            ed.WriteMessage("{0}; ", tpVal.Value);
          }
          ed.WriteMessage("|");
        }
        currentRow++;
      }
    }
  }
}

## 评论

**内容**: Alexander Rivilis said...
Am I right that in native ObjectARX no public class corresponding BlockPropertiesTable in AutoCAD .NET API? I found AcDbBlockPropertiesTable in acdbXX.lib but found none of the corresponding .h-files.
Reply
03/04/2013 at 05:52 AM

---
**内容**: Augusto Goncalves said in reply to Alexander Rivilis...
Hi Alexander,
Indeed this is not exposed on the ARX SDK headers, although defined on the acdbXX.dll
Have you considered call the .NET version from C++?
Regards,
Augusto Goncalves
Reply
03/05/2013 at 09:26 AM

---
**内容**: Alexander Rivilis said in reply to Augusto Goncalves...
Hi, Augusto! Do you mean call from mixed/managed C++? OK. It is possible. While I prefer "pure" ObjectARX. Calling from native ObjectARX have to be wish-listed! :-)
Reply
03/05/2013 at 12:24 PM

---
**内容**: Augusto Goncalves said in reply to Alexander Rivilis...
Already added, thanks for spotting it.
Reply
03/05/2013 at 12:26 PM

---
**内容**: Jürgen said...
Hi,
is it possible to get the geometry data of a parameter from a dynamic block? For instance the x and the y-value.
Regards Jürgen
Reply
09/29/2013 at 03:05 AM

---
**内容**: Augusto Goncalves said in reply to Jürgen...
Jürgen,
Are you referring to dynamic block parameters? If so, there are some posts about it at this blog...
Regards,
Augusto Goncalves
Reply
10/02/2013 at 01:40 PM

---
**内容**: Eric said...
Is this still available in 2018? Works fine for me in 2016 but when I try to use it in 2018 I get a "Method not found" error referencing EvalGraph.GetNode.
Reply
01/10/2020 at 11:09 AM

---
**内容**: Eric said in reply to Eric...
Nevermind, issue was on my end. This continues to work in 2018.
Reply
01/10/2020 at 02:58 PM

---
**内容**: اِحسان بَحرانی said in reply to Eric...
hi there!
would you explain how do you get rid of this error? plz.
Reply
06/06/2022 at 03:35 AM

---
**内容**: Peter Elliott said...
How to get the name of the table columns?
Reply
03/04/2021 at 01:33 PM

---
**内容**: Peter Elliott said in reply to Peter Elliott...
Figured it out - Column.Parameter.Name
Reply
04/07/2021 at 06:24 AM

---
