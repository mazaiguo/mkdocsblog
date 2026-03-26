---
title: "Accessing the External Reference's layer Information"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Layer
  - XREF
description: "To get the selected external reference's layer names you need to open the block definition of the external reference to get the path of the xRef. Y..."
author: Autodesk
---
# Accessing the External Reference's layer Information

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/accessing-the-external-references-layer-information.html

## 文章内容

By Augusto Goncalves
To get the selected external reference's layer names you need to open the block definition of the external reference to get the path of the xRef. You then open the drawing and get the layer names. You then open the layers of the xref in the current drawing and, for instance, set the IsFrozen property to true.
Note: The External reference layer names are prefix with the drawing name in the current drawing i.e "External_DrawingName|LayerName". The following sample code will freeze all the layers except layer zero of the selected Xref .
[CommandMethod("freezeXrefLayer")]
public void CmdFreezeXrefLayer()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
    // select an entity
  PromptEntityOptions pr = new PromptEntityOptions(
    "Select a xref: ");
  PromptEntityResult res = ed.GetEntity(pr);
  if (res.Status != PromptStatus.OK) return;
    // start the transaction
  using (Transaction trans =
    db.TransactionManager.StartTransaction())
  {
    BlockReference blockRef = trans.GetObject(
      res.ObjectId, OpenMode.ForRead) as BlockReference;
      // is a block reference?
    if (blockRef == null) return;
      // open the block definition?
    BlockTableRecord blockDef = trans.GetObject(
      blockRef.BlockTableRecord,
      OpenMode.ForRead) as BlockTableRecord;
      // is not from external reference, exit
    if (!blockDef.IsFromExternalReference) return;
      // open the xref database
    Database xRefDB = new Database(false, true);
    xRefDB.ReadDwgFile(blockDef.PathName,
      System.IO.FileShare.Read,
      false, string.Empty);
      using (Transaction xRefTrans =
      xRefDB.TransactionManager.StartTransaction())
    {
      // open the block definition and its model space
      BlockTable xRefBT = xRefTrans.GetObject(
        xRefDB.BlockTableId, OpenMode.ForRead) as BlockTable;
      BlockTableRecord xRefBTR = xRefTrans.GetObject(
        xRefBT[BlockTableRecord.ModelSpace], OpenMode.ForRead)
        as BlockTableRecord;
        // iterate through entities on the xref model space
      foreach (ObjectId xRefEntId in xRefBTR)
      {
        Entity ent = xRefTrans.GetObject(xRefEntId,
          OpenMode.ForRead) as Entity;
        LayerTable lt = trans.GetObject(db.LayerTableId,
          OpenMode.ForRead) as LayerTable;
          // get the drawing name
        string dwgName =
          xRefDB.OriginalFileName.Substring(
          xRefDB.OriginalFileName.LastIndexOf("\\") + 1,
          xRefDB.OriginalFileName.Length -
          xRefDB.OriginalFileName.LastIndexOf("\\") - 5);
          // now set the layer as frozen
        if (lt.Has(dwgName + "|" + ent.Layer))
        {
          ObjectId lyrId = lt[dwgName + "|" + ent.Layer];
          LayerTableRecord ltr = trans.GetObject(lyrId,
            OpenMode.ForWrite) as LayerTableRecord;
          ltr.IsFrozen = true;
        }
      }
      xRefTrans.Commit();
    }
    trans.Commit();
  }
}

## 评论

**内容**: fflix said...
hi augusto, i'm trying to use your example to get to the objectid of an xref layer, for use in a paperspace viewport's freeze method, however, without success (no exception as such but acad reports a save-error and the respective layers are not frozen). considering that objectids are non-persistent between sessions, how do viewports keep layers frozen (appropriate system settings presumed)? many thanks
Reply
09/22/2012 at 03:04 AM

---
**内容**: João Clemente said...
Olá Augusto.. td bom ?
Eu estou tentando a todo custo via programa(.NET, Python, etc...) extrair o path de um arquivo atachado ao CAD via XREF.. para poder extrair de milhoes de arquivos cujo acervo esta uma bagunça
O fato do xref estar referenciado no layer 0 faz com que o a DatabaseBlock avalie como FALSE o comando "isXref" ?
Reply
01/17/2019 at 09:04 AM

---
