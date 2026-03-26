---
title: "How to use Toggle Button Ribbon API"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - CUI
description: "Recently I have received a request from an ADN partner on how to create a Toggle Button which has toggle state IsChecked."
author: Autodesk
---
# How to use Toggle Button Ribbon API

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/how-to-use-toggle-button-ribbon-api.html

## 文章内容

By Madhukar Moogala
Recently I have received a request from an ADN partner on how to create a Toggle Button which has toggle state IsChecked.
I will discuss about Windows runtime API only not CUI,if want to explore CUI you can refer this nice blog.
One example of existing Toggle Button on AutoCAD UI is
Home\Groups
Code is self explanatory.
[CommandMethod("ToggleButton")]
public void ToggleButton()
{
Autodesk.Windows.RibbonControl ribbonControl
    = Autodesk.Windows.ComponentManager.Ribbon;
  RibbonTab Tab = new RibbonTab();
Tab.Title = "Test Ribbon";
Tab.Id = "TESTRIBBON_TAB_ID";
  ribbonControl.Tabs.Add(Tab);
  Autodesk.Windows.RibbonPanelSource srcPanel
    = new Autodesk.Windows.RibbonPanelSource();
srcPanel.Title = "Panel1";
  RibbonPanel Panel = new RibbonPanel();
Panel.Source = srcPanel;
Tab.Panels.Add(Panel);
  Autodesk.Windows.RibbonToggleButton button
    = new Autodesk.Windows.RibbonToggleButton();
  button.Text = "Toggle Button";
button.Size = RibbonItemSize.Large;
/*
Embedding Image resource to your project
1.On the Project menu, choose Add Existing Item.
2.Navigate to the image you want to add to your project.
* Click the Open button to add the image to your project's file list.
3.Right-click the image in your project's file list and choose Properties.
* The Properties window appears.
4.Find the Build Action property in the Properties window.
* Change its value to Embedded Resource.
*
Then opens a stream on the embedded image.
* The name used to refer to the image takes this form:
<namespace>.<image name>.<format>
*/
  button.Image = getBitmap("TestCmd2015.Koala.jpg", 16, 16);
button.LargeImage = getBitmap("TestCmd2015.Koala.jpg", 32, 32);
button.ShowText = true;
button.CommandParameter = "";
button.CommandHandler = new ToggleButtonCmdHandler();
  srcPanel.Items.Add(button);
  Tab.IsActive = true;
}
  public class ToggleButtonCmdHandler : System.Windows.Input.ICommand
{
public bool CanExecute(object parameter)
{
return true;
}
  public event EventHandler CanExecuteChanged;
  public void Execute(object parameter)
{
Document doc =
Application.DocumentManager.MdiActiveDocument;
  Autodesk.Windows.RibbonToggleButton button
    = parameter as Autodesk.Windows.RibbonToggleButton;
  doc.Editor.WriteMessage(
"\nRibbonButton Executed: " +
button.Text +
" (IsChecked: " + button.IsChecked.ToString() + ")");
}
}
  public BitmapImage getBitmap(string imageName, int Height, int Width)
{
BitmapImage image = new BitmapImage();
  image.BeginInit();
image.StreamSource
    = Assembly.GetExecutingAssembly().GetManifestResourceStream(imageName);
// image.UriSource = new Uri(imageName);
image.DecodePixelHeight = Height;
image.DecodePixelWidth = Width;
image.EndInit();
  return image;
}

## 评论

**内容**: Pierre de la Verre said...
Hi
are there also some examples on Lisp?
Reply
11/06/2017 at 08:45 AM

---
