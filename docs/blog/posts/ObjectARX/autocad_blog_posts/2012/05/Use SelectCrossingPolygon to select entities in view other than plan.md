---
title: "Use SelectCrossingPolygon to select entities in view other than plan"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Selection
  - UCS
description: "I am using Editor SelectCrossingWindow to select Entities. If the view is not a plan view then some of the entities inside of the window defined by..."
author: Autodesk
---
# Use SelectCrossingPolygon to select entities in view other than plan

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/use-selectcrossingpolygon-to-select-entities-in-view-other-than-plan.html

## 文章内容

By Wayne Brill
Issue
I am using Editor SelectCrossingWindow to select Entities. If the view is not a plan view then some of the entities inside of the window defined by the points are not included in the selection.
Solution
The selection area using SelectCrossingWindow() is going to be a rectangular shape in WCS that is horizontal. To see the selection area for the crossing window, in WCS (plan view) draw a rectangle using the REC command using the points used for the crossing window. Then go to the non plan view, change the UCS to view and draw another rectangle by snapping to the points used for the first rectangle. Change the UCS back to world before you run the code and you will see the entities that are inside or cross the second rectangle are selected.
Instead of using SelectCrossingWindow use SelectCrossingPolygon(). Here is an example. If the entities are visible, then this will get the entities in the area defined by the points. (Regardless of the current view). This example uses a filter to only select lines.
CommandMethod("SEL")]
public void MySelection()
{
    Document doc = Autodesk.AutoCAD
        .ApplicationServices.Application
        .DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      Point3d p1 = new Point3d(10.0, 10.0, 0.0);
    Point3d p2 = new Point3d(10.0, 11.0, 0.0);
    Point3d p3 = new Point3d(11.0, 11.0, 0.0);
    Point3d p4 = new Point3d(11.0, 10.0, 0.0);
      Point3dCollection pntCol =
                      new Point3dCollection();
    pntCol.Add(p1);
    pntCol.Add(p2);
    pntCol.Add(p3);
    pntCol.Add(p4);
      int numOfEntsFound = 0;
      PromptSelectionResult pmtSelRes = null;
      TypedValue[] typedVal = new TypedValue[1];
    typedVal[0] = new TypedValue
                 ((int)DxfCode.Start, "Line");
      SelectionFilter selFilter =
              new SelectionFilter(typedVal);
    pmtSelRes = ed.SelectCrossingPolygon
                         (pntCol, selFilter);
    // May not find entities in the UCS area
    // between p1 and p3 if not PLAN view
    // pmtSelRes =
    //    ed.SelectCrossingWindow(p1, p3, selFilter);
      if (pmtSelRes.Status == PromptStatus.OK)
    {
        foreach (ObjectId objId in
            pmtSelRes.Value.GetObjectIds())
        {
            numOfEntsFound++;
        }
        ed.WriteMessage("Entities found " +
                    numOfEntsFound.ToString());
    }
    else
        ed.WriteMessage("\nDid not find entities");
}

