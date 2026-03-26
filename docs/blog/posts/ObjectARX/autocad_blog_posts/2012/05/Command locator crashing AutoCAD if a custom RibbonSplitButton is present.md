---
title: "Command locator crashing AutoCAD if a custom RibbonSplitButton is present"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoCAD
  - C#
  - Unicode
description: "Here is an issue that was reported by an ADN developer:"
author: Autodesk
---
# Command locator crashing AutoCAD if a custom RibbonSplitButton is present

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/command-locator-crashing-autocad-if-a-custom-ribbonsplitbutton-is-present.html

## 文章内容

By Philippe Leefsma
  Here is an issue that was reported by an ADN developer:
After creating a "RibbonSplitButton" with the runtime API, simply looking for any keyword in the command reference locator (the search field accessible from the BigA menu) will crash AutoCAD. Is there a workaround for preventing the crash?
Solution
The crash can be avoided by simply affecting the “RibbonSplitButton.Text” property to some dummy string, as this text isn’t display in the UI anyway.
Here is a C# sample that illustrates a safe way to create a RibbonSplitButton:
  [CommandMethod("RibbonSplitButton")]
public void RibbonSplitButton()
{
    Autodesk.Windows.RibbonControl ribbonControl =
        Autodesk.Windows.ComponentManager.Ribbon;
      RibbonTab Tab = new RibbonTab();
    Tab.Title = "Test Ribbon";
    Tab.Id = "TESTRIBBON_TAB_ID";
      ribbonControl.Tabs.Add(Tab);
      Autodesk.Windows.RibbonPanelSource srcPanel =
        new RibbonPanelSource();
      srcPanel.Title = "Panel1";
      RibbonPanel Panel = new RibbonPanel();
    Panel.Source = srcPanel;
    Tab.Panels.Add(Panel);
      Autodesk.Windows.RibbonButton button1 =
        new RibbonButton();
      button1.Text = "Button1";
    button1.ShowText = true;
    button1.CommandHandler = new SplitCmdHandler();
      Autodesk.Windows.RibbonButton button2 =
        new RibbonButton();
      button2.Text = "Button2";
    button2.ShowText = true;
    button2.CommandHandler = new SplitCmdHandler();
      RibbonSplitButton ribSplitButton = new RibbonSplitButton();
      //Required not to crash AutoCAD when using cmd locator
    ribSplitButton.Text = "RibbonSplitButton";
    ribSplitButton.ShowText = true;
      ribSplitButton.Items.Add(button1);
    ribSplitButton.Items.Add(button2);
      srcPanel.Items.Add(ribSplitButton);
      Tab.IsActive = true;
}
  public class SplitCmdHandler : System.Windows.Input.ICommand
{
    public bool CanExecute(object parameter)
    {
        return true;
    }
      public event EventHandler CanExecuteChanged;
      public void Execute(object parameter)
    {
        Document doc = Application.DocumentManager.MdiActiveDocument;
          if (parameter is RibbonButton)
        {
            RibbonButton button = parameter as RibbonButton;
              doc.Editor.WriteMessage(
                "\nRibbonButton Executed: " + button.Text);
        }
    }
}

