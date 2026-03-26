---
title: "RibbonSplitButton with icons / images"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I'm creating a RibbonSplitButton, but the RibbonButtons I add to it do not show their icons. What could be the problem?"
author: Autodesk
---
# RibbonSplitButton with icons / images

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/ribbonsplitbutton-with-icons-images.html

## 文章内容

By Adam Nagy
I'm creating a RibbonSplitButton, but the RibbonButtons I add to it do not show their icons. What could be the problem?
Solution
Probably you are just missing the line where you set RibbonButton.ShowImage = true;
In case something else is missing attached is a project which creates the following split button on the ribbon using png images included in the assembly as resources:
Here is the source code of the project:
using System;
using System.Windows.Media.Imaging;
using System.Reflection;
  using Autodesk.Windows;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  namespace MySplitButton
{
  public class Commands
  {
    BitmapImage getBitmap(string fileName)
    {
      BitmapImage bmp = new BitmapImage();
      // BitmapImage.UriSource must be in a BeginInit/EndInit block.             
      bmp.BeginInit();
      bmp.UriSource = new Uri(string.Format(
        "pack://application:,,,/{0};component/{1}",
        Assembly.GetExecutingAssembly().GetName().Name,
        fileName));
      bmp.EndInit();
        return bmp;
    }
      [CommandMethod("RibbonSplitButton")]
    public void RibbonSplitButton()
    {
      Autodesk.Windows.RibbonControl ribbonControl =
        Autodesk.Windows.ComponentManager.Ribbon;
        /////////////////////////////////////
      // create Ribbon tab
      RibbonTab Tab = new RibbonTab();
      Tab.Title = "Test Ribbon";
      Tab.Id = "TESTRIBBON_TAB_ID";
        ribbonControl.Tabs.Add(Tab);
        /////////////////////////////////////
      // create Ribbon panel
      Autodesk.Windows.RibbonPanelSource srcPanel =
        new RibbonPanelSource();
      srcPanel.Title = "Panel1";
        RibbonPanel Panel = new RibbonPanel();
      Panel.Source = srcPanel;
      Tab.Panels.Add(Panel);
        //////////////////////////////////////////////////
      // create the buttons listed in the split button
      Autodesk.Windows.RibbonButton button1 = new RibbonButton();
      button1.Text = "Button1";
      button1.ShowText = true;
      button1.ShowImage = true;
      button1.LargeImage = getBitmap("a_large.png");
      button1.Image = getBitmap("a_small.png");
      button1.CommandHandler = new MyCmdHandler();
        Autodesk.Windows.RibbonButton button2 = new RibbonButton();
      button2.Text = "Button2";
      button2.ShowText = true;
      button2.ShowImage = true;
      button2.LargeImage = getBitmap("b_large.png");
      button2.Image = getBitmap("b_small.png");
      button2.CommandHandler = new MyCmdHandler();
        ////////////////////////
      // create split button
      RibbonSplitButton ribSplitButton = new RibbonSplitButton();
      // Required to avoid upsetting AutoCAD when using cmd locator
      ribSplitButton.Text = "RibbonSplitButton";
      ribSplitButton.ShowText = true;
        ribSplitButton.Items.Add(button1);
      ribSplitButton.Items.Add(button2);
        srcPanel.Items.Add(ribSplitButton);
        Tab.IsActive = true;
    }
      public class MyCmdHandler : System.Windows.Input.ICommand
    {
      public bool CanExecute(object parameter)
      {
        return true;
      }
        public event EventHandler CanExecuteChanged;
        public void Execute(object parameter)
      {
        Document doc = acApp.DocumentManager.MdiActiveDocument;
          if (parameter is RibbonButton)
        {
          RibbonButton button = parameter as RibbonButton;
            doc.Editor.WriteMessage(
            "\nRibbonButton Executed: " + button.Text + "\n");
        }
      }
    }
  }
}
If you want your button to look like this instead, then add the below lines to the above code.
ribSplitButton.IsSplit = true;
ribSplitButton.Size = RibbonItemSize.Large;
ribSplitButton.IsSynchronizedWithCurrentItem = true;
Here is the project:  Download Mysplitbutton

## 评论

**内容**: Martin said...
HI there,
how can you change the actual label of the Ribbon split button? Mine always inherit the name of the first button.
Ta,
Martin.
Reply
12/14/2012 at 04:06 AM

---
**内容**: Adam Nagy said...
Happy New Year, Martin.
The button text and image is synchronized with the last selected button from the list because of the IsSynchronizedWithCurrentItem = true property. I guess by default it is synchronised with the first item and then changed when one of the buttons from the popup is clicked. Maybe you can override that somehow if that's what you want.
Reply
01/05/2013 at 08:28 AM

---
**内容**: Patrick said...
Hello from france,
Is it possible to have a static text with RibbonSplitButton, like it is with the cui editor. I'm using AutoCAD 2012 to 2014.
Thank you.
Reply
09/04/2013 at 12:33 AM

---
**内容**: Balaji said in reply to Patrick...
Hi Patrick,
Have you tried setting "IsSynchronizedWithCurrentItem" property of the Ribbon split button to false ?
This will ensure that the split button always displays the same text regardless of what was selected.
Regards,
Balaji
Reply
09/10/2013 at 12:36 AM

---
**内容**: zeus said...
Hi Adam,
This is a nice post! :-) I just wondered if I have long name on my button, how do I control the length of text displayed?? and how can integrate it to a new custom cuix.
Thanks,
Zeus
Reply
09/22/2013 at 06:03 AM

---
