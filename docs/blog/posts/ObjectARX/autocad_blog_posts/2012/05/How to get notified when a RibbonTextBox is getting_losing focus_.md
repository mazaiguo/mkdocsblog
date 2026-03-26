---
title: "How to get notified when a RibbonTextBox is getting/losing focus?"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Unicode
description: "Here is a question submitted by an ADN developer that could be turned into an interesting post:"
author: Autodesk
---
# How to get notified when a RibbonTextBox is getting/losing focus?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-get-notified-when-a-ribbontextbox-is-gettinglosing-focus.html

## 文章内容

By Philippe Leefsma
  Here is a question submitted by an ADN developer that could be turned into an interesting post:
I created a texbox through the Ribbon runtime API, I would now want to get notified whenever the textbox is getting or losing focus, so I can perform some custom actions, like highlighting corresponding entities for example.
Solution
The RibbonTextBox derives from the "System.Windows.Controls.TextBox" object, so here is a way to retrieve keyboard focus notifications for it:
  [CommandMethod("RibbonTextBox")]
public void RibbonTextBox()
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
      MyTextBox textbox = new MyTextBox();
    textbox.Width = 100;
    textbox.IsEmptyTextValid = false;
    textbox.AcceptTextOnLostFocus = true;
    textbox.InvokesCommand = true;
    textbox.CommandHandler = new TextboxCommandHandler();
      srcPanel.Items.Add(textbox);
      Tab.IsActive = true;
}
  public class TextboxCommandHandler :
    System.Windows.Input.ICommand
{
    public bool CanExecute(object parameter)
    {
        return true;
    }
      public event EventHandler CanExecuteChanged;
      public void Execute(object parameter)
    {
        RibbonTextBox textbox = parameter as RibbonTextBox;
          if (textbox != null)
        {
            Document doc = Autodesk.AutoCAD.ApplicationServices.
                Application.DocumentManager.MdiActiveDocument;
              doc.Editor.WriteMessage("\nRibbon Textbox: "
                + textbox.TextValue + "\n");
        }
    }
}
  public class MyTextBox : RibbonTextBox
{
    public MyTextBox()
    {
        EventManager.RegisterClassHandler(
            typeof(System.Windows.Controls.TextBox),
            System.Windows.Controls.TextBox.GotKeyboardFocusEvent,
            new RoutedEventHandler(OnGotFocus));
          EventManager.RegisterClassHandler(
            typeof(System.Windows.Controls.TextBox),
            System.Windows.Controls.TextBox.LostKeyboardFocusEvent,
            new RoutedEventHandler(OnLostFocus));
    }
      void OnGotFocus(object sender, RoutedEventArgs e)
    {
        if (e.Source != null)
        {
            System.Windows.Controls.TextBox element =
                e.Source as System.Windows.Controls.TextBox;
              if (element != null)
            {
                MyTextBox ribbonItem =
                    element.DataContext as MyTextBox;
                  if (ribbonItem != null)
                {
                    Document doc = Autodesk.AutoCAD.
                        ApplicationServices.Application.
                        DocumentManager.MdiActiveDocument;
                      doc.Editor.WriteMessage(
                        "\nTextbox got focus :)\n");
                }
            }
        }
    }
      void OnLostFocus(object sender, RoutedEventArgs e)
    {
        if (e.Source != null)
        {
            System.Windows.Controls.TextBox element =
                e.Source as System.Windows.Controls.TextBox;
              if (element != null)
            {
                MyTextBox ribbonItem =
                    element.DataContext as MyTextBox;
                  if (ribbonItem != null)
                {
                    Document doc = Autodesk.AutoCAD.
                        ApplicationServices.Application.
                        DocumentManager.MdiActiveDocument;
                      doc.Editor.WriteMessage(
                        "\nTextbox lost focus :(\n");
                }
            }
        }
    }
}

