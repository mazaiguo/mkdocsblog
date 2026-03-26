---
title: "Using Autoloader to setup contextual ribbon tab"
date: 2014-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - CUI
  - Unicode
description: "For details on displaying contextual ribbon tab, please refer to this blog post. In this blog post, we will look at using the Autoloader to deploy ..."
author: Autodesk
---
# Using Autoloader to setup contextual ribbon tab

发布日期: 2014-06-01

原始链接: https://adndevblog.typepad.com/autocad/2014/06/using-autoloader-to-setup-contextual-ribbon-tab.html

## 文章内容

By Balaji Ramamoorthy
For details on displaying contextual ribbon tab, please refer to this blog post. In this blog post, we will look at using the Autoloader to deploy the contextual ribbon tab xaml file and the custom dll that it uses. In this example, the bundle implements a command to insert a smiley. The smiley is a block reference with XData to distinguish it from any other block reference. When the smiley is selected, a contextual ribbon tab defined in the CUIX is displayed. Here are the steps to get this working using the Autoloader.
Step 1 : Create the contextual tab selector rule xaml file.
   <?xml version="1.0"  encoding="utf-8"?>
   <TabSelectorRules 
 xmlns="clr-namespace:Autodesk.AutoCAD.Ribbon;assembly=AcWindows" 
 Ordering="0">
   <TabSelectorRules.References>
 <AssemblyReference Namespace ="Aen1ContextualTabSelectorHelper" 
                     Assembly ="Aen1ContextualTabSelectorHelper"/>
 </TabSelectorRules.References>
   <Rule Uid="Aen1SelectionRule"  DisplayName="Aen1 Selection Rule" 
                             Theme="Green" Trigger="Selection">
     <![CDATA[
     Aen1ContextualTabSelectorHelper.Methods.ShowMyTab(Selection)
     ]]>
 </Rule>
   </TabSelectorRules>
  Step 2 : Create a custom dll that our contextual tab selector rule will use to determine if the contextual tab is to be displayed. In this example, we look for block references that contain a specific XData.
namespace Aen1ContextualTabSelectorHelper
 {
         Public  Class  Methods
     {
         public  static  bool ShowMyTab(object selObj)
         {
             bool showTab = false ;
               Selection sel = (Selection)selObj;
             if  (sel.Count != 1 || !sel.ContainsOnly
                     (new string [] { "BlockReference" }))
                 return  showTab;
               IDataItem item = sel[0] as  IDataItem;
             if (item == null)
                 return  showTab;
               IDataItemTransaction trans 
                     = item.StartTransaction(OpenMode.ForRead);
             if  (trans != null)
             {
                 BlockReference bref 
                             = trans.Item as  BlockReference;
                   if  (bref != null)
                 {
                     ResultBuffer resBuf 
                         = bref.GetXDataForApplication("SMILEY");
                       if  (resBuf != null)
                     {
                         // Show tab if  the block reference
                         // has our XData
                         showTab = true ;
                         resBuf.Dispose();
                     }
                 }
                 trans.Commit();
             }
               return  showTab;
         }
     }
 }
  Step 3 : Modify the PackageContents.xml of your Autoloader bundle to load the Contextual tab selector rule xaml and its custom dll during startup.
<ComponentEntry 
AppName="MyTestPlugin1" 
AppDescription="Aen1 Contextual Tab Rule" 
ModuleName="./Contents/Windows/Aen1ContextualTabSelectorRules.xaml" 
XamlType="ContextualTabRule"/>
<ComponentEntry 
AppName="MyTestPlugin1" 
AppDescription="Aen1 Contextual Tab Rule" 
ModuleName="./Contents/Windows/Aen1ContextualTabSelectorHelper.dll" 
LoadOnAutoCADStartup="True"/>
The complete Autoloader bundle can be downloaded here :
Download MyTestPlugin.bundle
To try the bundle, run the "InsertSmiley" command and place a smiley. Zoom to extents if necessary. Select the smiley and a contextual tab should appear as shown in the screenshot.

