---
title: "Displaying Ribbon Control in the palette"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Palette
description: "I want to show a separate ribbon control. Can you show me how to create and display it ?"
author: Autodesk
---
# Displaying Ribbon Control in the palette

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/displaying-ribbon-control-in-the-palette.html

## 文章内容

By Balaji Ramamoorthy
Issue
I want to show a separate ribbon control. Can you show me how to create and display it ?
Solution
The RibbonControl is a class that inherits “System.Windows.Controls.Control” and so requires a WPF host (Ex: WPF User control) to display it.
The WPF User control can be associated with the AutoCAD palette.
Only the pertinent code is shown here. Please download the attachment for the sample project.
if(_ps == null)
{
    _ps = new PaletteSet("WPF Palette");
    _ps.Size = new Size(400, 600);
    _ps.DockEnabled
            = (DockSides)((int)DockSides.Left + (int)DockSides.Right);
    MyWPFUserControl uc = new MyWPFUserControl();
      Autodesk.Windows.RibbonControl ribControl
                        = new Autodesk.Windows.RibbonControl();
      RibbonTab ribTab = new RibbonTab();
    ribTab.Title = "Test";
    ribTab.Id = "Test";
    ribControl.Tabs.Add(ribTab);
      RibbonPanelSource ribSourcePanel = new RibbonPanelSource();
    ribSourcePanel.Title = "My Tools";
    ribSourcePanel.DialogLauncher =  new RibbonCommandItem();
    ribSourcePanel.DialogLauncher.CommandHandler
                                    = new AdskCommandHandler();
      //Add a Panel
    RibbonPanel ribPanel = new RibbonPanel();
    ribPanel.Source = ribSourcePanel;
    ribTab.Panels.Add(ribPanel);
      //Create button
    RibbonButton ribButton1 = new RibbonButton();
    ribButton1.Text = "Line" + "\n" + "Generator";
    ribButton1.CommandParameter = "Line ";
    ribButton1.ShowText = true;
    ribButton1.LargeImage
        = Images.getBitmap((Bitmap)_resourceManager.GetObject("LineImage"));
    ribButton1.Image
        = Images.getBitmap((Bitmap)_resourceManager.GetObject("LineImage"));
    ribButton1.Size = RibbonItemSize.Large;
    ribButton1.Orientation = System.Windows.Controls.Orientation.Vertical;
    ribButton1.ShowImage = true;
    ribButton1.ShowText = true;
    ribButton1.CommandHandler = new AdskCommandHandler();
    ribSourcePanel.Items.Add(ribButton1);
      uc.Content = ribControl;
      _ps.AddVisual("Test", uc);
}
  _ps.KeepFocus = true;
_ps.Visible = true;
Here is a screenshot of the ribbon displayed in a palette :

Download Wpfpalette0

## 评论

**内容**: Wolfgang said...
Hi,
adding a Ribbon Control to a palette works fine (WPF). One question: I want to get the actual height of the ribbon control (changes through cycling from full ribbon/minimized to panels/minimzed to tabs) to place some controls directly and dynamically below the ribbon control.
- Wolfgang
Reply
05/06/2013 at 07:52 AM

---
**内容**: Balaji said in reply to Wolfgang...
Hi Wolfgang,
Using a WPF ContentControl in the user control and settings its Content to the RibbonControl will automatically consider the resizing.
Here is a sample code snippet assuming that the name of the content control is "MyCC" :
System.Windows.Controls.ContentControl myCC = uc.FindName("MyCC") as System.Windows.Controls.ContentControl;
myCC.Content = ribControl;
Regards,
Balaji
Reply
05/07/2013 at 06:52 AM

---
**内容**: imvivs said...
Hi, I have some query ,I want to know, what are the benefits or reason of developing the tool palettes in .Net? What are the points that makes us to use .net for developing it?
As we can simply use Tool Palettes features in AutoCAD's Menu, then what are the extra thing that can be done pragmatically for Tool Palettes.?
Reply
10/22/2013 at 12:15 AM

---
**内容**: Balaji said in reply to imvivs...
Hi,
I have replied to your query in the other post :
http://adndevblog.typepad.com/autocad/2013/06/working-with-toolpalette-groups-using-net.html#comment-6a0167607c2431970b019b00348e56970d
Reply
10/22/2013 at 12:21 AM

---
