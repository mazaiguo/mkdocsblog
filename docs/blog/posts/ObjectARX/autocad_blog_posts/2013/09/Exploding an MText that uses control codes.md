---
title: "Exploding an MText that uses control codes"
date: 2013-09-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "To explode an MText entity to identify its fragment text, the "ExplodeFragments" method can be used. Please refer to the following blog post if you..."
author: Autodesk
---
# Exploding an MText that uses control codes

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/exploding-an-mtext-that-uses-control-codes.html

## 文章内容

By Balaji Ramamoorthy
To explode an MText entity to identify its fragment text, the "ExplodeFragments" method can be used. Please refer to the following blog post if you need a sample code :
Getting text fragments from Mtext object
When this method is used to explode an MText entity that makes use of control codes such as "%%c", "%%d" then the fragment text in the callback method will contain the control code and not the special character that it represents. A simple workaround to get the text fragment is to create a MText and sets its content based on the fragment text. Here is a sample code snippet :
public MTextFragmentCallbackStatus MTextCallback
                        (MTextFragment frag, object userData)
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      String fragText = frag.Text;
      ed.WriteMessage(String.Format("{0} Fragment : {1}",
                            Environment.NewLine, fragText));
      using (MText mt = new MText())
    {
        mt.SetDatabaseDefaults();
        mt.Contents = fragText;
        String mtText = mt.Text;
          ed.WriteMessage(String.Format("{0} Fragment : {1}",
                                Environment.NewLine, mtText));
    }
      return MTextFragmentCallbackStatus.Continue;
}
  [CommandMethod("TestMText")]
public void TestMText()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    PromptEntityResult per
                = ed.GetEntity("Select MText to explode :");
      if (per.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        MText mtext =
            (MText)Tx.GetObject(per.ObjectId, OpenMode.ForRead);
        mtext.ExplodeFragments(
                    new MTextFragmentCallback(MTextCallback));
        Tx.Commit();
    }
}
Here is the output of the code snippet on a sample MText that uses %%c and %%d :

