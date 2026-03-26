---
title: "Getting text fragments from Mtext object"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Unicode
description: "Use API “ExplodeFragments” as shown in below code to break the Mtext text string into fragments. The callback provided as input to “ExplodeFragment..."
author: Autodesk
---
# Getting text fragments from Mtext object

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/getting-fragment-from-mtext-object.html

## 文章内容

By Virupaksha Aithal
Use API “ExplodeFragments” as shown in below code to break the Mtext text string into fragments. The callback provided as input to “ExplodeFragments” is called for every Fragment of Mtext object.
static public MTextFragmentCallbackStatus
                        Fragments(MTextFragment Param, object data)
{
    string strText = Param.Text;
      //show the Fragmentted text.
    Application.ShowAlertDialog(strText);
    return MTextFragmentCallbackStatus.Continue;
}
  [CommandMethod("ExplodeFragments")]
static public void ExplodeFragments()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
               new PromptEntityOptions("\nSelect a Mtext");
    options.SetRejectMessage("\nSelect only Mtext");
    options.AddAllowedClass(typeof(MText), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
          try
        {
            MText text = tr.GetObject(acSSPrompt.ObjectId,
                                          OpenMode.ForRead) as MText;
            text.ExplodeFragments(Fragments, "Test");
            tr.Commit();
        }
        catch
        {
            tr.Abort();
        }
    }
}

