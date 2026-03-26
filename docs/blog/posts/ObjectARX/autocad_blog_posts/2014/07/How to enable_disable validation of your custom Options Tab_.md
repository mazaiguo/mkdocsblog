---
title: "How to enable/disable validation of your custom Options Tab?"
date: 2014-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
  - Unicode
description: "In those following posts Kean is showing how to add your own custom tab to the AutoCAD Options dialog:"
author: Autodesk
---
# How to enable/disable validation of your custom Options Tab?

发布日期: 2014-07-01

原始链接: https://adndevblog.typepad.com/autocad/2014/07/how-to-enabledisable-validation-of-your-custom-options-tab.html

## 文章内容

By Philippe Leefsma
In those following posts Kean is showing how to add your own custom tab to the AutoCAD Options dialog:
Adding a custom tab to AutoCAD's options dialog using .NET - Part 1
Adding a custom tab to AutoCAD's options dialog using .NET - Part 2
What those samples aren’t showing, is how you can enable/disable the OK button, so the user will only be able to validate the dialog if his choices are matching your logic.
In order to achieve such a feature, a little hack relying on a couple of Win32 P/Invoked APIs is likely to be needed:
In the sample below, I am using FindWindowEx and EnableWindow to control the OK button, depending on the value provided in a textbox.
public partial class OptionsTabControl : UserControl
{
    private IntPtr _hWndOkBtn;
      [DllImport("user32.dll", SetLastError = true)]
    private static extern IntPtr FindWindowEx(
        IntPtr parentHandle,
        IntPtr childAfter,
        string className,
        string windowTitle);
      [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool EnableWindow(
        IntPtr hWnd,
        bool bEnable);
      public OptionsTabControl()
    {
        InitializeComponent();
          // Finds Options dialog
        IntPtr hWnd = FindWindowEx(IntPtr.Zero,
            IntPtr.Zero,
            "#32770",
            "Options");
          // Finds Ok button
        _hWndOkBtn = FindWindowEx(hWnd,
            IntPtr.Zero,
            "Button",
            "Ok");
          EnableWindow(_hWndOkBtn, false);
          tbValidation.Text = "Validate me ...";
    }
      private void tbValidation_TextChanged(
        object sender,
        EventArgs e)
    {
        if (tbValidation.Text.Length == 0)
            EnableWindow(_hWndOkBtn, false);
        else
        {
            bool enabled =
                (tbValidation.Text == "ADN rules!");
              EnableWindow(_hWndOkBtn, enabled);
        }
    }
}
  Complete sample also attached.
AcadOptionsDlg.zip

