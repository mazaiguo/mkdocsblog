---
title: "Adding highlight overrules to selected entities only and set color"
date: 2016-07-01
categories:
  - AutoCAD
tags:
  - Plugin
  - Selection
description: "Here is a method to add highlight overrules to selected objects only. Interactively on highlighting the objects to which overrules are added,color ..."
author: Autodesk
---
# Adding highlight overrules to selected entities only and set color

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/adding-highlight-overrules-to-selected-entities-only-and-set-color.html

## 文章内容

By Deepak Nadig
Here is a method to add highlight overrules to selected objects only. Interactively on highlighting the objects to which overrules are added,color needs to change
The code sample below adds the HighlightOverrrule to selected objects and also enables to set highlight color to each object after adding the overrule
To test:  
1) First, run the 'SelectObjectsToAddOverrule' command, to select the required objects.
_hlOverRule.SetIdFilter(ids.ToArray()) will restrict addition of overrule to the selected objects only. Color of the selected objects will be changed to red during and after selection(_colorIndex =1) 
2) Set the colorIndex value  by running the command ' ChangeHighlightColor' . Now, interactively highlight any selected object to see color change
(Note : Interactively, highlighting  objects which were not selected,will have no effect as overrule is not added to them) 
  public class MyHighlightOverrule : HighlightOverrule
 {
 private int _colorIndex = 1;
 private int _oldColorIndex;
public MyHighlightOverrule()
 {
 AddOverrule(RXClass.GetClass(typeof(Entity)), this, true);
 }
 public int ColorIndex
 {
 set { _colorIndex = value; }
 get { return _colorIndex; }
 }
 public override void Highlight(Entity entity, FullSubentityPath subId, bool highlightAll)
 {
 Database db = entity.Database;
 Document dwg = Application.DocumentManager.MdiActiveDocument;
using (DocumentLock dl = dwg.LockDocument())
 {
 using (Transaction tran = db.TransactionManager.StartTransaction())
 {
 entity.UpgradeOpen();
 _oldColorIndex = entity.ColorIndex;
 entity.ColorIndex = _colorIndex;
 entity.DowngradeOpen();
 }
 }
 base.Highlight(entity, subId, highlightAll);
 }
 }
 public class Commands
 {
 private static MyHighlightOverrule _hlOverRule = null;
 [CommandMethod("SelectObjectsToAddOverrule")]
 public void SelectObjectsToAddOverrule()
 {
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Editor ed = doc.Editor;
 Transaction tr = doc.TransactionManager.StartTransaction();
 using (tr)
 {
 if (_hlOverRule == null)
 {
 _hlOverRule = new MyHighlightOverrule();
 }
 // Loop until or completed
 List<ObjectId> ids = new List<ObjectId>();
 List<FullSubentityPath> paths = new List<FullSubentityPath>();
 PromptNestedEntityResult rs;
 do
 {
 rs = ed.GetNestedEntity(String.Format("\nSelect entity to highlight color"));
 if (rs.Status == PromptStatus.OK)
 {
 ids.Add(rs.ObjectId);
 FullSubentityPath path = FullSubentityPath.Null;
 path = GetSubEntityPath(rs);
 if (path != FullSubentityPath.Null)
 paths.Add(path);
 }
 } while (rs.Status == PromptStatus.OK);
 _hlOverRule.SetIdFilter(ids.ToArray());
 tr.Commit();
 }
 ed.Regen();
 }
 private static FullSubentityPath GetSubEntityPath(PromptNestedEntityResult rs)
 {
 // Extract relevant information from the prompt object
 ObjectId selId = rs.ObjectId;
 List<ObjectId> objIds = new List<ObjectId>(rs.GetContainers());
 // Reverse the "containers" list
 objIds.Reverse();
 // Now append the selected entity
 objIds.Add(selId);
 // Retrieve the sub-entity path for this entity
 SubentityId subEnt = new SubentityId(SubentityType.Null, System.IntPtr.Zero);
 FullSubentityPath path = new FullSubentityPath(objIds.ToArray(), subEnt);
 // Open the outermost container, relying on the open transaction...
 Entity ent = objIds[0].GetObject(OpenMode.ForRead) as Entity;
 // ... and highlight the nested entity
 if (ent == null)
 return FullSubentityPath.Null;
 // Return the sub-entity path 
 return path;
 }
 [CommandMethod("ChangeHighlightColor")]
 public void ChangeHighlightColor()
 {
 Document dwg = Autodesk.AutoCAD.ApplicationServices.
 Application.DocumentManager.MdiActiveDocument;
 Editor ed = dwg.Editor;
 PromptIntegerOptions opt = new PromptIntegerOptions(
 "\nEnter color index (a number form 0 to 7):");
 PromptIntegerResult res = ed.GetInteger(opt);
 if (res.Status == PromptStatus.OK)
 {
 _hlOverRule.ColorIndex = res.Value;
 }
 }
 }
Screencast of the code testing is below :

