---
title: "Editor.Snap Method to change the snap mode of point"
date: 2020-06-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "In your workflow of using Editor.GetEntity you may sometimes want to retrieve"
author: Autodesk
---
# Editor.Snap Method to change the snap mode of point

发布日期: 2020-06-01

原始链接: https://adndevblog.typepad.com/autocad/2020/06/editorsnap-method-to-change-the-snap-mode-of-point.html

## 文章内容

By Deepak Nadig
In your workflow of using Editor.GetEntity you may sometimes want to retrieve
all the co-ordinates of pickpoint used to select the entity.
For example consider the following case by constructing a circle at point (0,0,5) and radius 5 on WCS XY-plane with top view.
On selecting a point on circle using Editor.GetEntity, PromptEntityResult.PickedPoint returns : (3.50064192661003 , 3.35618169844321 , 0)
To get all the co-ordinates,it may be useful to change the point to nearest snap mode using Editor.Snap that returns the Z co-ordinate as well. 
Code:
[CommandMethod("getEntityPickPoint")]
public static void getEntityPickPoint()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    PromptEntityOptions peo = new PromptEntityOptions("\nSelect Entity");
    PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status == PromptStatus.OK)
    {
        Point3d pickedPoint = per.PickedPoint;
        Point3d pickedPtOsnap = ed.Snap("_near", pickedPoint);

        ed.WriteMessage("\n Selected pick point: {0}", pickedPoint.ToString());
        ed.WriteMessage("\n Selected Picked Point Osnap near: {0}", pickedPtOsnap);
    }
}
Result:
Command: GETENTITYPICKPOINT
Select Entity:
Selected pick point: (3.50064192661003,3.35618169844321,0)
Selected Picked Point Osnap near: (3.60921996485993,3.46027907043009,5)
  More about object osnaps :
https://knowledge.autodesk.com/de/search-result/caas/CloudHelp/cloudhelp/2017/DEU/AutoCAD-AutoLISP/files/GUID-4EEE5488-01D8-454F-9386-79E493E55D6E-htm.html

## 评论

**内容**: JeromeA said...
@Deepak,
I have a newbie question: Where do you find the string constants to use with Editor.Snap string OsMode parameter?
Thanks,
JeromeA
Reply
10/08/2020 at 05:46 AM

---
