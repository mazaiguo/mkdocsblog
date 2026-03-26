---
title: "How to Check if XREF Edit In Place–Is Saved or Discarded"
date: 2019-02-01
categories:
  - AutoCAD
tags:
  - XREF
description: "When user edit external reference in place, there is no way to get to know if user had saved the changes or discarded."
author: Autodesk
---
# How to Check if XREF Edit In Place–Is Saved or Discarded

发布日期: 2019-02-01

原始链接: https://adndevblog.typepad.com/autocad/2019/02/how-to-check-if-xref-edit-in-placeis-saved-or-discarded.html

## 文章内容

By Madhukar Moogala
When user edit external reference in place, there is no way to get to know if user had saved the changes or discarded.
If your application would like to capture the user intent, for example.
if (e.GlobalCommandName == /*MSG0*/"REFCLOSE")
{

if (save){
//logic 1
}
if(discard){
//logic 2
}


}
This post will show one way to find out, if Xref is saved or discarded
class XrefCheckEditor;
XrefCheckEditor* xrefEd = nullptr;
class XrefLongTranReactor;
XrefLongTranReactor* xrefTransRctr = nullptr;

Acad::ErrorStatus getSysVar(const TCHAR* varName, TCHAR* val)
{
 resbuf rb;
 if (acedGetVar(varName, &rb) == RTNORM) {
  assert(rb.restype == RTSTR);
  val = rb.resval.rstring;
  free(rb.resval.rstring);
  return(Acad::eOk);
 }
 else
  return(Acad::eInvalidInput);
}
namespace EditInPlaceXref {
 enum EditInPlaceXrefState
 {
  Discarded,
  Saved
  
 };
 EditInPlaceXrefState XrefState;
 EditInPlaceXrefState Reset() {
  XrefState = Discarded;
  return XrefState;
 }
 
}

class XrefLongTranReactor : public AcApLongTransactionReactor {

 virtual void endCheckIn(AcDbLongTransaction& lt) {
  if (lt.type() == AcDbLongTransaction::kXrefDb)
  {
   //We are good, changes have been Saved.
   EditInPlaceXref::XrefState = EditInPlaceXref::Saved;
  }
 }

};
class XrefCheckEditor : public AcEditorReactor {

 virtual void commandEnded(const TCHAR* cmdStr) {
  if (wcscmp(cmdStr, L"REFCLOSE") == 0)
  {
   
   switch (EditInPlaceXref::XrefState)
   {
   case EditInPlaceXref::Saved:
    acutPrintf(L"\n Modifications 
        To In External Reference Are Saved");
    EditInPlaceXref::Reset();
    break;
   case EditInPlaceXref::Discarded:
    acutPrintf(L"\n Modifications
        To In External Reference Are Discarded");
    break;
   default:
    break;
   }

  }
 }
};

void watch() {

 if (xrefEd == nullptr && xrefTransRctr == nullptr) {
  xrefEd = new XrefCheckEditor();
  xrefTransRctr = new XrefLongTranReactor();
 }

 acedEditor->addReactor(xrefEd);
 acapLongTransactionManager->addReactor(xrefTransRctr);
 
}
void unWatch() {
 acedEditor->removeReactor(xrefEd);
 acapLongTransactionManager->removeReactor(xrefTransRctr);
 if (xrefEd != nullptr) {
  delete xrefEd;
  xrefEd = nullptr;
 }
 if (xrefTransRctr != nullptr) {
  delete xrefTransRctr;
  xrefTransRctr = nullptr;
 }
 acutPrintf(_T("Watching Editor Reactor\n"));
}

void checkIfXrefSavedOrDiscarded()
{
 acutPrintf(_T("\nThis function checks
       if changes made to edit-in place xref are saved or discarded"));
 acutPrintf(_T("\nModifications %s"), 
   EditInPlaceXref::XrefState ? _T("Saved") : _T("Discarded"));
}

## 评论

**内容**: Alexander Rivilis said...
Thank you, Madhukar!
That is my port to AutoCAD .NET API:
[code]
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.EditorInput;
// This line is not mandatory, but improves loading performances
[assembly: CommandClass(typeof(Rivilis.XrefLongTrans))]
namespace Rivilis
{
public class XrefLongTrans
{
enum EditInPlaceXrefState
{
Discarded,
Saved
};
static EditInPlaceXrefState state =
EditInPlaceXrefState.Discarded;
[CommandMethod("WatchXref")]
public void WatchXref()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
LongTransactionManager longTranMan = Application.LongTransactionManager;
longTranMan.CheckedIn += TrMan_CheckedIn;
longTranMan.Aborted += TrMan_Aborted;
doc.CommandEnded += Doc_CommandEnded;
}
[CommandMethod("UnWatchXref")]
public void UnWatchXref()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
LongTransactionManager longTranMan = Application.LongTransactionManager;
longTranMan.CheckedIn -= TrMan_CheckedIn;
longTranMan.Aborted -= TrMan_Aborted;
doc.CommandEnded -= Doc_CommandEnded;
}

private void TrMan_Aborted(object sender, LongTransactionEventArgs e)
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
if (e.Transaction.Type == LongTransactionType.XRefDb)
{
ed.WriteMessage("\nLong transaction {0} aborted\n", e.Transaction.LongTransactionName);
state = EditInPlaceXrefState.Discarded;
}
}
private void TrMan_CheckedIn(object sender, LongTransactionEventArgs e)
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
if (e.Transaction.Type == LongTransactionType.XRefDb)
{
ed.WriteMessage("\nLong transaction {0} commited\n", e.Transaction.LongTransactionName);
state = EditInPlaceXrefState.Saved;
}
}
private void Doc_CommandEnded(object sender, CommandEventArgs e)
{
if (e.GlobalCommandName.ToUpper() == "REFCLOSE")
{
Document doc = Application.DocumentManager.MdiActiveDocument;
if (doc == null) return;
Editor ed = doc.Editor;
ed.WriteMessage("\nModification of XREF {0}\n",
(state == EditInPlaceXrefState.Saved) ?
"Saved": "Discarded");
}
}
}
}
[/code]
Reply
02/27/2019 at 06:41 AM

---
**内容**: Kenny said...
It is very helpful!!
Reply
03/01/2019 at 06:17 PM

---
**内容**: santiago said...
Great help!
What approach can you take if you need to know if the changes made during a '-BEDIT' command were saved or discarded?
Thank you!
Reply
08/03/2023 at 08:15 PM

---
