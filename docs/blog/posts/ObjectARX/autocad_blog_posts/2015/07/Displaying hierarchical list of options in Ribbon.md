---
title: "Displaying hierarchical list of options in Ribbon"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you only need a list of options to be displayed, the RibbonSplitButton should do. Here is a blog post on that. But if you need further sub items..."
author: Autodesk
---
# Displaying hierarchical list of options in Ribbon

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/displaying-hierarchical-list-of-options-in-ribbon.html

## 文章内容

By Balaji Ramamoorthy
If you only need a list of options to be displayed, the RibbonSplitButton should do. Here is a blog post on that. But if you need further sub items for any one of those options, the RibbonMenuButton is suitable. Here is a sample code to display the options as shown in the below screenshot :
 // Requires reference to AdWindows.dll 
 using  Autodesk.Windows;
 using  System.Drawing.Imaging;
   [CommandMethod("RibbonMenuButton" )]
 public  void  RibbonMenuButton()
 {
     RibbonControl ribbonControl 
         = ComponentManager.Ribbon;
       RibbonTab Tab = new  RibbonTab();
     Tab.Title = "Test Ribbon" ;
     Tab.Id = "TESTRIBBON_TAB_ID" ;
       ribbonControl.Tabs.Add(Tab);
       RibbonPanelSource srcPanel 
         = new  RibbonPanelSource();
     srcPanel.Title = "Panel1" ;
       RibbonPanel Panel = new  RibbonPanel();
     Panel.Source = srcPanel;
     Tab.Panels.Add(Panel);
       RibbonMenuItem button1 
         = new  RibbonMenuItem();
     button1.Text = "Button1" ;
     button1.ShowText = true ;
     button1.LargeImage 
         = getBitmap(Resources.Resource1.Image1, 32, 32);
     button1.Image 
         = getBitmap(Resources.Resource1.Image1, 16, 16);
     button1.CommandHandler = new  MenuButtonCmdHandler();
       RibbonMenuItem subButton1 = new  RibbonMenuItem();
     subButton1.Text = "SubButton1" ;
     subButton1.ShowText = true ;
     subButton1.LargeImage 
         = getBitmap(Resources.Resource1.Image1, 32, 32);
     subButton1.Image 
         = getBitmap(Resources.Resource1.Image1, 16, 16);
     subButton1.CommandHandler 
         = new  MenuButtonCmdHandler();
       RibbonMenuItem subButton2 = new  RibbonMenuItem();
     subButton2.Text = "SubButton2" ;
     subButton2.ShowText = true ;
     subButton2.LargeImage 
         = getBitmap(Resources.Resource1.Image1, 32, 32);
     subButton2.Image 
         = getBitmap(Resources.Resource1.Image1, 16, 16);
     subButton2.CommandHandler 
         = new  MenuButtonCmdHandler();
       button1.Items.Add(subButton1);
     button1.Items.Add(subButton2);
       RibbonMenuItem button2 = new  RibbonMenuItem();
     button2.Text = "Button2" ;
     button2.ShowText = true ;
     button2.LargeImage 
         = getBitmap(Resources.Resource1.Image1, 32, 32);
     button2.Image 
         = getBitmap(Resources.Resource1.Image1, 16, 16);
     button2.CommandHandler = new  MenuButtonCmdHandler();
       RibbonMenuButton ribMenuButton 
         = new  RibbonMenuButton();
       ribMenuButton.Id = "ADN.RibbonMenuButton.1" ;
       ribMenuButton.Text = "RibbonMenuButton" ;
     ribMenuButton.ShowText = true ;
     ribMenuButton.Size = RibbonItemSize.Large;
     ribMenuButton.LargeImage 
         = getBitmap(Resources.Resource1.Image1, 32, 32);
     ribMenuButton.Image 
         = getBitmap(Resources.Resource1.Image1, 16, 16);
     ribMenuButton.ShowImage = true ;
     ribMenuButton.MaxHeight = double .PositiveInfinity;
     ribMenuButton.MinHeight = 0;
     ribMenuButton.IsSplit = true ;
     ribMenuButton.IsSynchronizedWithCurrentItem = true ;
       ribMenuButton.Items.Add(button1);
     ribMenuButton.Items.Add(button2);
       srcPanel.Items.Add(ribMenuButton);
       Tab.IsActive = true ;
 }
   BitmapImage getBitmap(Bitmap bitmap, int  height, int  width)
 {
     MemoryStream stream = new  MemoryStream();
     bitmap.Save(stream, ImageFormat.Png);
       BitmapImage bmp = new  BitmapImage();
     bmp.BeginInit();
     bmp.StreamSource = new  MemoryStream(stream.ToArray());
     bmp.DecodePixelHeight = height;
     bmp.DecodePixelWidth = width;
     bmp.EndInit();
       return  bmp;
 }
   public  class  MenuButtonCmdHandler 
     : System.Windows.Input.ICommand
 {
     public  bool  CanExecute(object  parameter)
     {
         return  true ;
     }
       public  event  EventHandler CanExecuteChanged;
       public  void  Execute(object  parameter)
     {
         Document doc 
             = Application.DocumentManager.MdiActiveDocument;
           if  (parameter is  RibbonMenuItem)
         {
             RibbonMenuItem menuItem 
                 = parameter as  RibbonMenuItem;
             if  (menuItem != null )
             {
                 doc.Editor.WriteMessage(
                     "\\nMenu Item Executed: "  
                     + menuItem.Text);
             }
         }
     }
 }

