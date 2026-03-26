---
title: "Displaying a contextual tab upon entity selection using Ribbon runtime API"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - API
  - Selection
  - Unicode
description: "The AutoCAD API provides a way to display a specific contextual tab upon entity selection, but the approach involves creating a custom xaml file an..."
author: Autodesk
---
# Displaying a contextual tab upon entity selection using Ribbon runtime API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/displaying-a-contextual-tab-upon-entity-selection-using-ribbon-runtime-api.html

## 文章内容

By Philippe Leefsma
  The AutoCAD API provides a way to display a specific contextual tab upon entity selection, but the approach involves creating a custom xaml file and .Net assembly, place them in AutoCAD install directory and finally modify the CUI file to make it aware of the new tab selector rule we created. The technical details of that functionality are described in one of our DevNote article available only for ADN members at the moment.
The approach I am exposing here is more flexible and straightforward to put in place as it only relies on the Ribbon runtime API: it sets up a couple of event handlers and will display dynamically a contextual tab upon an entity selection, with ability to perform advanced logic whether or not to display you tab.
Note: Running “CtxTabUponSelect” command multiple times in the same document will have the effect of setting multiple event handlers for “ImpliedSelectionChanged”. Though the effect won’t be noticed from the user interface, you may want to take some precautions not to listen twice to an event when you use that in production code.
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Use: Displays a contextual tab upon entity selection,
//      using Ribbon runtime API.
//
// Author: Philippe Leefsma, April 2012
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
Autodesk.Windows.RibbonTab _ctxTab = null;
  [CommandMethod("CtxTabUponSelect")]
public void CtxTabUponSelect()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
      //Set up event for selection changed
    doc.ImpliedSelectionChanged +=
        new EventHandler(doc_ImpliedSelectionChanged);
}
  void doc_ImpliedSelectionChanged(object sender, EventArgs e)
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    PromptSelectionResult psr = doc.Editor.SelectImplied();
      //if no entities are selected, we hide our context tab
    if (psr.Value == null)
    {
        HideTab();
        return;
    }
      //In this example we only display the tab if only circles are
    // selected. You may want to change this condition of course.
    foreach (SelectedObject selObj in psr.Value)
    {
        if (selObj.ObjectId.ObjectClass.DxfName.ToLower()
            != "circle")
        {
            HideTab();
            return;
        }
    }
      //We will use the Application.Idle event to safely display our tab
    if (_ctxTab == null || !_ctxTab.IsVisible)
    {
        Autodesk.AutoCAD.ApplicationServices.Application.Idle +=
            new EventHandler(OnIdle);
    }
}
  void OnIdle(object sender, EventArgs e)
{
    //Make sure ribbon manager is available
    if (Autodesk.Windows.ComponentManager.Ribbon != null)
    {
        //Create tab if it doesn't exist
        if (_ctxTab == null)
            CreateCtxTab();
          //Otherwise make it visible
        if(!_ctxTab.IsVisible)
        {
            Autodesk.Windows.RibbonControl ribbonCtrl =
                Autodesk.Windows.ComponentManager.Ribbon;
              ribbonCtrl.ShowContextualTab(_ctxTab, false, true);
              _ctxTab.IsActive = true;
        }
          if(!_ctxTab.IsActive)
            _ctxTab.IsActive = true;
    }
}
  //Tab creation method
void CreateCtxTab()
{
    Autodesk.Windows.RibbonControl ribbonCtrl =
        Autodesk.Windows.ComponentManager.Ribbon;
      _ctxTab = new RibbonTab();
      _ctxTab.Name = "MyTab";
    _ctxTab.Id = "MY_CTX_TAB_ID";
    _ctxTab.IsVisible = true;
    _ctxTab.Title = _ctxTab.Name;
    _ctxTab.IsContextualTab = true;
      ribbonCtrl.Tabs.Add(_ctxTab);
}
  void HideTab()
{
    Autodesk.AutoCAD.ApplicationServices.Application.Idle
        -= new EventHandler(OnIdle);
      if (_ctxTab != null)
    {
        Autodesk.Windows.RibbonControl ribbonCtrl =
            Autodesk.Windows.ComponentManager.Ribbon;
          ribbonCtrl.HideContextualTab(_ctxTab);
        _ctxTab.IsVisible = false;
        _ctxTab = null;
    }
}

## 评论

**内容**: Carl said...
just wondering if I'm missing the remove handler call somewhere? I'm not c# fluent but still...
Reply
12/01/2013 at 03:06 PM

---
**内容**: Philippe said in reply to Carl...
Hi Carl,
Are you talking about removing "ImpliedSelectionChanged"...? That would be up to you if you want to remove that event handler or not...
Reply
12/01/2013 at 04:05 PM

---
