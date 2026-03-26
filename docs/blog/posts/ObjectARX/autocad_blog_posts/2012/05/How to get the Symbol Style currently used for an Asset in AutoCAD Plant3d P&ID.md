---
title: "How to get the Symbol Style currently used for an Asset in AutoCAD Plant3d P&ID"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "I saw this post on the newsgroups and I thought I should document it here for our subscribers to see…"
author: Autodesk
---
# How to get the Symbol Style currently used for an Asset in AutoCAD Plant3d P&ID

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-get-the-symbol-style-currently-used-for-an-asset-in-autocad-plant3d-pid.html

## 文章内容

by Fenton Webb
I saw this post on the newsgroups and I thought I should document it here for our subscribers to see…
Thanks to Jorge Lopez and a very keen forums contributor programmer Anthony Perks for their efforts with this post.
Here is the code which displays an Asset’s style name…
// display a selected Asset's style name, by Jorge Lopez, 8/May/2012
[CommandMethod("LISTSTYLE", CommandFlags.Modal)]
public static void ListStyle()
{
  Editor oEditor = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    PromptEntityOptions oPromptOptions = new PromptEntityOptions("Select an object");
  PromptEntityResult oPromptResult = oEditor.GetEntity(oPromptOptions);
    if (oPromptResult.Status != PromptStatus.OK)
  {
    return;
  }
    Database oDB = AcadApp.DocumentManager.MdiActiveDocument.Database;
  TransactionManager oTxMgr = oDB.TransactionManager;
    using (Transaction oTx = oTxMgr.StartTransaction())
  {
    DBObject obj = oTx.GetObject(oPromptResult.ObjectId, OpenMode.ForRead);
      Asset oAsset = obj as Asset;
      /* Get the style's object id */
    ObjectId styleId = oAsset.StyleId;
      if (!styleId.IsNull)
    {
      /* Display the style's name */
      Style oStyle = (Style)oTx.GetObject(styleId, OpenMode.ForRead);
        string strMsg = "\n" + oStyle.Name;
      oEditor.WriteMessage(strMsg);
        /* If it is an asset style then display the block name */
      AssetStyle oAssetStyle = oStyle as AssetStyle;
      if (oAssetStyle != null)
      {
        ObjectId btrId = oAssetStyle.BlockTableRecord;
        BlockTableRecord oBTR = (BlockTableRecord)oTx.GetObject(btrId, OpenMode.ForRead);
          strMsg = "\n" + oBTR.Name;
        oEditor.WriteMessage(strMsg);
      }
    }
      oTx.Commit();
  }
}

