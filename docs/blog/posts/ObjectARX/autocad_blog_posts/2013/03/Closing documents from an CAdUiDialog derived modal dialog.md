---
title: "Closing documents from an CAdUiDialog derived modal dialog"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
  - Unicode
description: "I can't close documents using the closeDocument API from an CAdUiDialog derived dialog because AutoCAD reports that the documents are busy. Why doe..."
author: Autodesk
---
# Closing documents from an CAdUiDialog derived modal dialog

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/closing-documents-from-an-caduidialog-derived-modal-dialog.html

## 文章内容

Issue
I can't close documents using the closeDocument API from an CAdUiDialog derived dialog because AutoCAD reports that the documents are busy. Why does this occur?
Solution
Make sure that you call the closeDocument API from the application context (see the executeInApplicationContext API). Once you do that, you must also enable document activation (enableDocumentActivation API). CAdUiDialog disables
document activation in its DoModal override. As a result, AutoCAD cannot close documents when document activation is disabled.
The reason CAcUiDialog does this is that when you prompt for user input from your dialog then you re-enable the main frame thus giving a chance to the user to change the active document... CAcUiDialog tries to prevent this scenario.

## 评论

**内容**: Chenghao LI said...
sir,i have a problem when close actived document in ExecuteInApplicationContext,need you help.under is my program:
[CommandMethod("asbuilt2")]
public void asbuilt2()
{
if (keyima() == false || isDrawingPath() == true)
return;
object[] parmsDraw;
FormBuilt ff = new FormBuilt();
System.Windows.Forms.DialogResult dr=Application.ShowModalDialog(ff);
if (dr == System.Windows.Forms.DialogResult.OK)
{
parmsDraw = ff.rets;
ff.Close();
ff.Dispose();
myin.StopeEvent();
string dwgFilePath="";
if ((bool)parmsDraw[3] == true && PGVs.IsUseXref==true)//isLayout?
{
MageComCanShu mcc = new MageComCanShu();
Polyline plzx = mcc.GetPolylineCanShu(MageComCanShu.Canshu.pl_zx);
if (plzx == null)
return;
AboutEntity.ClearModelSpace(plzx);
Document doc = Application.DocumentManager.MdiActiveDocument;
using (DocumentLock docLock = doc.LockDocument())
{
doc.Database.EraseEmptyObjects(2);
dwgFilePath = doc.Name;
doc.Database.SaveAs(GetXX.GetOpenDWGpath() + "\\" + PGVs.NameMapXref,
true, DwgVersion.Current, doc.Database.SecurityParameters);
}
}
Document doc2 = Application.DocumentManager.MdiActiveDocument;
using (DocumentLock docLock = doc2.LockDocument())
{
PipeLineDrawDWG pdd = new PipeLineDrawDWG(pipeDBase, (double)parmsDraw[0], (double)parmsDraw[1]);
pdd.DrawAllDWG(parmsDraw[2].ToString(), (bool)parmsDraw[3], (bool)parmsDraw[4], (PipeLineDrawDWG.DrawStyle)parmsDraw[5]);
}
myin.ConnectEvent();
Application.DocumentManager.ExecuteInApplicationContext(ApplicationContextFinalProcess, doc2.Name);
}
else
{
ff.Close();
ff.Dispose();
}
}
///
/// 回调函数
///
///
static void ApplicationContextFinalProcess(object data)
{
Document d= Application.DocumentManager.Add("");
Application.DocumentManager.MdiActiveDocument = d;
foreach (Document doc in Application.DocumentManager)
if (doc.Name == data.ToString())
{
doc.CloseAndDiscard();
}
}
Reply
11/11/2015 at 05:10 PM

---
**内容**: Chenghao LI said...
the error is document busy.
static void ApplicationContextFinalProcess(object data)
{
Application.DocumentManager.MdiActiveDocument.CloseAndDiscard();
}
Application.DocumentManager.MdiActiveDocument.CloseAndDiscard() also not work
Reply
11/11/2015 at 05:13 PM

---
