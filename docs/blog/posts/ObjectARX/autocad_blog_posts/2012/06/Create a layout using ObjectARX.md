---
title: "Create a layout using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
  - Plot
description: "The following code creates a layout and sets the plot configuration to default settings. The AcDbPlotSettingsValidator class functions is an ideal ..."
author: Autodesk
---
# Create a layout using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/create-a-layout-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
The following code creates a layout and sets the plot configuration to default settings. The AcDbPlotSettingsValidator class functions is an ideal way which helps to alter default settings.
AcDbDatabase *curDocDB
            = acdbHostApplicationServices()->workingDatabase();
   AcApLayoutManager *pLayoutMngr
     = dynamic_cast<AcApLayoutManager *>
        (
            acdbHostApplicationServices()->layoutManager()
        );
   if(pLayoutMngr != NULL)
 {
     ACHAR* nextLayoutName
                    = pLayoutMngr->getNextNewLayoutName(NULL);
       AcDbObjectId layoutId = AcDbObjectId::kNull;
     AcDbObjectId btrId = AcDbObjectId::kNull;
       pLayoutMngr->createLayout(nextLayoutName, layoutId, btrId);
       // initialises AcDbLayout with appropriate defaults
     pLayoutMngr->setDefaultPlotConfig(btrId);
       // setting as current layout
     pLayoutMngr->setCurrentLayout(nextLayoutName);
       pLayoutMngr->updateLayoutTabs();
 }

## 评论

**内容**: Nick G. said...
Hi, Balaji.
Ooops. The same is here :) http://adn.autodesk.com/adn/servlet/devnote?siteID=4814862&id=5407257&linkID=4900509
What about imagination? it's boring copying a functions from ADN "as is". What if I want to set layout's name? Little modifications can make source code much more interesting to blog readers :)
bool addLayout(ACHAR * wantedLayoutName)
{
if (acdbCurDwg()->tilemode() != 1)
{
acutPrintf(_T("\n*** Sorry, just from model space ***"));
return false;
}
Acad::ErrorStatus es;
ACHAR layoutName[256];
_tcscpy(layoutName,wantedLayoutName);
int curIndex = 1;
acDocManager->lockDocument(acDocManager->curDocument(), AcAp::kWrite);
AcApLayoutManager *layManager = (AcApLayoutManager *) acdbHostApplicationServices()->layoutManager();
if (!layManager) return false;
AcDbObjectId lauoutId;
AcDbObjectId blockTableRecId;
AcDbEntity *pEnt;
Adesk::Boolean viewPorts = layManager->createViewports();
layManager->setCreateViewports(true);
LAYCREATE:
es = layManager->createLayout(layoutName,lauoutId,blockTableRecId); // try to create a layout
if (es != Acad::eOk)
{
if (es = Acad::eDuplicateKey)
{
_stprintf(layoutName,_T("%s_%d"),wantedLayoutName,curIndex++);
goto LAYCREATE;
}
else
acedAlert(_T("Sorry, can't do this.\nFunction aborted."));
acDocManager->unlockDocument(acDocManager->curDocument());
return false;
}
layManager->setCurrentLayoutId(lauoutId); // сделали текущим
layManager->setShowPaperMargins(Adesk::kTrue); // kill preinter border
layManager->setCreateViewports(viewPorts);
AcDbLayout *curLayout = layManager->findLayoutNamed(layoutName,TRUE); // layout is ready for modifying

if (curLayout)
{
// ... here all modifications.
// for example, set printer an paper size, e.t.c.
layManager->updateCurrentPaper(Adesk::kTrue);
layManager->updateLayoutTabs();
acDocManager->unlockDocument(acDocManager->curDocument());
return true;
}
acDocManager->unlockDocument(acDocManager->curDocument());
return false;
}
Reply
06/19/2012 at 12:01 AM

---
**内容**: Balaji said in reply to Nick G....
Yes, It is also available as a ADN Devnote.
Probably you should read this post :
http://adndevblog.typepad.com/autocad/2012/05/devnote-migration.html
Sure, there are a few posts that are not existing Devnotes, but we dont mark them differently.
Reply
06/19/2012 at 12:07 AM

---
**内容**: nizar said...
hi
what is tilemode?
Reply
01/14/2013 at 01:04 PM

---
**内容**: Balaji said in reply to nizar...
This doc should help :
http://docs.autodesk.com/ACD/2010/ENU/AutoCAD%202010%20User%20Documentation/index.html?url=WS1a9193826455f5ffa23ce210c4a30acaf-4e46.htm,topicNumber=d0e357602
Reply
01/15/2013 at 02:34 AM

---
**内容**: nizar said in reply to Balaji...
thank you very much.
i need your help in another mater:
i need to plot several objects in the drawing each into pdf file size A4 automaticlly.
with or without creating layout.
how can i do that
right now i can plot a pdf for the extended dwg.
thanks for your help
nizar
Reply
02/08/2013 at 01:26 PM

---
**内容**: harsha said...
Hello sir, Are you there ?/
I need help about ObjectArx but 2024...
[CommandMethod("InsertViewsToLayout")]
public static void InsertViewsToLayout()
{
Document acDoc = Application.DocumentManager.MdiActiveDocument;
Database acCurDb = acDoc.Database;
using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
{
BlockTable acBlkTbl;
acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
BlockTableRecord acBlkTblRec;
acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace], OpenMode.ForWrite) as BlockTableRecord;
// Switch to the previous Paper space layout
Application.SetSystemVariable("TILEMODE", 0);
acDoc.Editor.SwitchToPaperSpace();
// Get the current layout
LayoutManager acLayoutMgr = LayoutManager.Current;
Layout acLayout = acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForWrite) as Layout;
Point3d[] viewPositions = {
new Point3d(2.5, 5.5, 0),
new Point3d(2.5, 2.5, 0),
new Point3d(5.5, 5.5, 0),
new Point3d(5.5, 2.5, 0),
new Point3d(8.5, 5.5, 0),
new Point3d(8.5, 2.5, 0)
};
Vector3d[] viewDirections = {
new Vector3d(0, 0, -1),
new Vector3d(0, 0, 1),
new Vector3d(-1, 0, 0),
new Vector3d(1, 0, 0),
new Vector3d(0, -1, 0),
new Vector3d(0, 1, 0)
};
for (int i = 0; i < viewPositions.Length; i++)
{
using (Autodesk.AutoCAD.DatabaseServices.Viewport acVport = new Autodesk.AutoCAD.DatabaseServices.Viewport())
{
acVport.CenterPoint = viewPositions[i];
acVport.Width = 2.5;
acVport.Height = 2.5;
// Add the new viewport to the layout's block table record
acBlkTblRec.AppendEntity(acVport);
acTrans.AddNewlyCreatedDBObject(acVport, true);
// Set the view direction
acVport.ViewDirection = viewDirections[i];
// Set the visual style
StyleViewport(acVport);
// Enable the viewport
acVport.On = true;
}
}
acTrans.Commit();
acDoc.Editor.Regen();
}
}
private static void StyleViewport(Autodesk.AutoCAD.DatabaseServices.Viewport viewport)
{
using (Database db = HostApplicationServices.WorkingDatabase)
{
using (Transaction tr = db.TransactionManager.StartTransaction())
{
// "Hidden" is the name of the visual style you want
viewport.VisualStyleId = GetVisualStyleId(db, "Hidden");
// Set other properties if needed
viewport.Color = Autodesk.AutoCAD.Colors.Color.FromRgb(0, 0, 0);
tr.Commit();
}
}
}

Reply
11/30/2023 at 09:16 PM

---
**内容**: harsha said in reply to harsha...
GetVisualStyleId
Severity Code Description Project File Line Suppression State
Error CS0103 The name 'GetVisualStyleId' does not exist in the current context AutoCad C:\Users\BVRIT\source\repos\AutoCad\AutoCad\Commands.cs 268 Active

My desired output is to generate a layout with 6 views (top bottom front back left right)
where model fits the respective viewports and be rendered with hidden visual style and edges are black in color. Export the layout as pdf.
Reply
11/30/2023 at 09:20 PM

---
