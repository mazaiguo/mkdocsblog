---
title: "Add Ribbon tab to Contextual Tab Selector Rule using CUI API"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
  - Unicode
description: "I'd like to programmatically add my Ribbon tab to the Contextual Tab Selector rule that I created. How could I do it?"
author: Autodesk
---
# Add Ribbon tab to Contextual Tab Selector Rule using CUI API

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/add-ribbon-tab-to-contextual-tab-selector-rule-using-cui-api.html

## 文章内容

By Adam Nagy
I'd like to programmatically add my Ribbon tab to the Contextual Tab Selector rule that I created. How could I do it?
Solution
Here is a sample code that shows how to do it using the CUI API. In this case we'll add the Annotation Ribbon tab to the AcArcSelected rule which is part of the AcContextualTabSelectorRules.xaml file.
Once you run the below command, whenever you select an arc in the drawing the Annotation tab will show up.
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Customization;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using System.Collections.Generic;
  [assembly: CommandClass(typeof(ContextualTab.AEN1Commands))]
  namespace ContextualTab
{
  public class AEN1Commands
  {
    [CommandMethod("MyCommand")]
    static public void Cmd1()
    {
      // Part of AcContextualTabSelectorRules.xaml
      const string kRuleId = "AcArcSelected";
        // Id of Annotation tab
      const string kTabId = "ID_TabAnnotate";
        // Get customization section
        string menuName = (string)acApp.GetSystemVariable("MENUNAME");
      CustomizationSection cs =
        new CustomizationSection(menuName + ".cuix");
        // Check if the rule is already used
        RibbonRoot rr = cs.MenuGroup.RibbonRoot;
      RibbonTabSelector ts = null;
        foreach (RibbonTabSelector tsIter in rr.RibbonTabSelectors)
        if (tsIter.Rule == kRuleId)
        {
          ts = tsIter;
          break;
        }
        // If it's not used then create it
        if (ts == null)
      {
        ts = (RibbonTabSelector)System.Activator.CreateInstance(
               typeof(RibbonTabSelector), true
             );
          ts.Rule = kRuleId;
        rr.RibbonTabSelectors.Add(ts);
      }
        // Add the tab we want to make appear
        if (!new List<string>(ts.Tabs).Contains(kTabId))
        ts.Append(kTabId);
        // Save modifications and reload
        if (cs.IsModified)
      {
        cs.Save();
          acApp.ReloadAllMenus();
      }
    }
  }
}

