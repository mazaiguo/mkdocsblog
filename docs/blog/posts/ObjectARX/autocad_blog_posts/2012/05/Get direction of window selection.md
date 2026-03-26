---
title: "Get direction of window selection"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
description: "If you want to know in which direction the user stretched the selection window then you can take advantage of the information provided by the Selec..."
author: Autodesk
---
# Get direction of window selection

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/get-direction-of-window-selection.html

## 文章内容

By Adam Nagy
If you want to know in which direction the user stretched the selection window then you can take advantage of the information provided by the SelectedObject class.
If you only need to know if the selection window was stretched from left-to-right (= window selection) or right-to-left (= crossing selection), then you can use the above class' SelectionMethod property. (1st part)
The window/crossing selection specific information, e.g. the points of the selection window, can be retrieved from CrossingOrWindowSelectedObject class. (2nd part)
If you also need to know which corner was picked first and which one second, then you could use the Editor.PromptedForPoint event.
using System;
  using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.DatabaseServices;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly:CommandClass(typeof(TestProject.Commands))]
  namespace TestProject
{
  public class Commands
  {
    [CommandMethod("MyWindowSelect")]
    public void MyWindowSelect()
    {
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        PromptSelectionOptions pso = new PromptSelectionOptions();
      pso.MessageForAdding = "Select entities with window selection";
      pso.MessageForRemoval = "Deselect entities";
        // (3rd part)
      // You can use this event to monitor
      // the points the user is selecting
      ed.PromptedForPoint +=
        new PromptPointResultEventHandler(ed_PromptedForPoint);
      PromptSelectionResult psr = ed.GetSelection(pso);
      ed.PromptedForPoint -=
        new PromptPointResultEventHandler(ed_PromptedForPoint);
        if (psr.Status != PromptStatus.OK)
        return;
        foreach (SelectedObject sel in psr.Value)
      {
        if (sel.SelectionMethod == SelectionMethod.Window ||
            sel.SelectionMethod == SelectionMethod.Crossing)
        {
          // (1st part)
          if (sel.SelectionMethod == SelectionMethod.Window)
            ed.WriteMessage("\nUser selected from left to right");
          else
            ed.WriteMessage("\nUser selected from right to left");
            CrossingOrWindowSelectedObject cowso =
            (CrossingOrWindowSelectedObject)sel;
            // (2nd part)
          // The points of the selection window are always
          // listed in this order:
          // Top-Left, Top-Right, Bottom-Right, Bottom-Left
          // So it does not provide information about the direction
          // in which the user selected the window's points
          foreach (PickPointDescriptor ppd in cowso.GetPickPoints())
          {
            ed.WriteMessage(
              "\nPoint: " + ppd.PointOnLine.ToString() +
              "  Direction: " + ppd.Direction.ToString());
          }
        }
      }
    }
      void ed_PromptedForPoint(
      object sender, PromptPointResultEventArgs e)
    {
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        if (e.Result.Status == PromptStatus.OK)
        ed.WriteMessage("\n" + e.Result.Value.ToString()); 
    }
  }
}

## 评论

**内容**: Medya Uzmanı said...
Thank you
Reply
03/06/2023 at 07:36 PM

---
