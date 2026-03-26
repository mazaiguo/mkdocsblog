---
title: "Removing buttons from QuickAccessToolbar crashes AutoCAD"
date: 2014-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "If you are adding ribbon buttons to the AutoCAD QuickAccessToobar (QAT), please ensure that you have provided a unique Id to the ribbon button. If ..."
author: Autodesk
---
# Removing buttons from QuickAccessToolbar crashes AutoCAD

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/removing-buttons-from-quickaccesstoolbar-crashes-autocad.html

## 文章内容

By Balaji Ramamoorthy
If you are adding ribbon buttons to the AutoCAD QuickAccessToobar (QAT), please ensure that you have provided a unique Id to the ribbon button. If the ribbon button is not provided an Id, AutoCAD can crash when hiding / removing any other standard QAT button.
Here is a code snippet :
 Autodesk.Windows.ToolBars.QuickAccessToolBarSource  qat 
     = Autodesk.Windows.ComponentManager .QuickAccessToolBar;
   if  (qat != null )
 {
     RibbonButton  rbButton = new  RibbonButton ();
       // Important to provide a unique id 
     // to avoid the crash 
     rbButton.Id = "MYBUTTON" ;
       rbButton.Text = "Circle" ;
     rbButton.Description = "Circle" ;
       rbButton.Image = GetIcon("Circle_16.ico" );
     rbButton.LargeImage = GetIcon("Circle_32.ico" );
       // Attach the handler to fire out command 
     rbButton.CommandHandler
         = new  AutoCADCommandHandler ("_.Circle" );
       // Add it to the Quick Access Toolbar 
     qat.AddStandardItem(rbButton);
 }

