---
title: "The arrow of the Dialog Launcher button on my Ribbon panel does not show"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I set the DialogLauncher property of my RibbonPanelSource, but the icon does not appear on it:"
author: Autodesk
---
# The arrow of the Dialog Launcher button on my Ribbon panel does not show

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/the-arrow-of-the-dialog-launcher-button-on-my-ribbon-panel-does-not-show.html

## 文章内容

By Adam Nagy
I set the DialogLauncher property of my RibbonPanelSource, but the icon does not appear on it:
static RibbonPanel AddOnePanel()
{
  RibbonButton rb;
  RibbonPanelSource rps = new RibbonPanelSource();
  rps.Title = "Test One";
  RibbonPanel rp = new RibbonPanel();
  rp.Source = rps;
    rb = new RibbonButton();
  rb.Name = "Test Button";
  rb.ShowText = true;
  rb.Text = "Test Button";
  // Add the Button to the Tab
  rps.Items.Add(rb);
    // Create a Command Item that the Dialog Launcher can use,
  // for this test it is just a place holder.
  RibbonCommandItem rci = new RibbonCommandItem();
  rci.Name = "TestCommand";
    // Assign the Command Item to the DialogLauncher which auto-enables
  // the little button at the lower right of a Panel, but where's
  // the arrow you see in the stock Ribbons?
  rps.DialogLauncher = rci;
    return rp;
}
If I tried to set the image myself, that did not work either:
BitmapImage myBitMapImage = new BitmapImage();
// BitmapImage.UriSource must be in a BeginInit/EndInit block.
myBitMapImage.BeginInit();
// Change this string to a bmp file on your system
myBitMapImage.UriSource = new Uri("C:/temp.png",
                       UriKind.RelativeOrAbsolute);
  myBitMapImage.EndInit();
  rci.Image = myBitMapImage;
rci.LargeImage = myBitMapImage;
Solution
You need to use a RibbonButton and assign that to the DialogLauncher:
RibbonButton dialogLauncherButton = new RibbonButton();
dialogLauncherButton.Name = "TestCommand";
rps.DialogLauncher = dialogLauncherButton;

## 评论

**内容**: Steve Hill said...
Very helpful post... a couple of questions though.
What size should this image be? I would assume 16x16 but I've had issues even with regular button images at 16x16. What's the best way to create these images? Thanks.
Reply
05/29/2012 at 07:53 AM

---
**内容**: Sebastian said...
Quite some time since.... but with Revit 2019/2020/2021 is doesn't seem to work that way.
Reply
06/27/2021 at 03:19 AM

---
