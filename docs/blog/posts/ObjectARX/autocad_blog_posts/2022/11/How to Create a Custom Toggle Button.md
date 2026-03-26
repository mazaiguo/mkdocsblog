---
title: "How to Create a Custom Toggle Button"
date: 2022-11-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "Here in this blog I have shown how to create a Ribbon Toggle Button using AutoCAD Ribbon Runtime API."
author: Autodesk
---
# How to Create a Custom Toggle Button

发布日期: 2022-11-01

原始链接: https://adndevblog.typepad.com/autocad/2022/11/how-to-create-a-custom-toggle-button.html

## 文章内容

By Madhukar Moogala
Here in this blog I have shown how to create a Ribbon Toggle Button using AutoCAD Ribbon Runtime API.
https://adndevblog.typepad.com/autocad/2015/03/how-to-use-toggle-button-ribbon-api.html
This code sample shows how can we register a custom ribbon control on AutoCAD Ribbon bar, to illustrate I created a simple toggle button, but however this logic can be extended to any other fancy controls.
Logic:
Create a ResourceDictionary to hold resources and controls in XAML
Implement the binding logic to manage the state of ToggleButton.
Create a SystemVariable to hold the state of ToggleButton
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            return IsChecked(value);
        }
    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            bool isOn = (bool)value;
            if (isOn && !string.IsNullOrEmpty(OnMacro))
                RunMacro(OnMacro);
            else if (!isOn && !string.IsNullOrEmpty(OffMacro))
                RunMacro(OffMacro);
            return DataBindings.DoNothing;
        }

    
Load this XAML in to AutoCAD Runtime, so this custom dictionary gets merged in to the AutoCAD main resource dictionary and you will see a unfied UX.
If you are preparing CUIX using CUI editor, make sure, the key of ToggleButton should be same as the Id of ToggleButton in CUI. For example "XyzToggleButton"
     string menuName = (string)Application.GetSystemVariable("MENUNAME");           
            CustomizationSection cs = new CustomizationSection(menuName + ".cuix");
            var ribbonRoot = cs.MenuGroup.RibbonRoot;
            var homeTab = ribbonRoot.FindTab("ID_TabHome");
            var elementId = "ID_TogglePanel";
            var ribbonPanelSourceReference = homeTab.Find(elementId);
            if(ribbonPanelSourceReference is null)
            {
                var panel = homeTab.AddNewPanel(elementId, "TogglePanel");
                var row = panel.AddNewRibbonRow();
                row.AddNewToggleButton("XyzToggleButton", "XYZSTATE\nToggle", null, RibbonButtonStyle.LargeWithText);
                cs.Save();
            }
<adw:RibbonToggleButton 
        x:Uid="RibbonToggleButton-Xyz" 
        x:Key="XyzToggleButton"
        Name="XYZ Toggle"
        Tag="XYZSTATE">
        <adw:RibbonToggleButton.IsCheckedBinding>
            <Binding Source="{x:Static acmgd:Application.UIBindings}" Path="SystemVariables[XYZSTATE].Value" Converter="{StaticResource XyzToggleButtonConverter}"/>
        </adw:RibbonToggleButton.IsCheckedBinding>
        <adw:RibbonToggleButton.Image>
            <BitmapImage x:Uid="BitmapImage_1" UriSource="Resources/Toggle.bmp" />
        </adw:RibbonToggleButton.Image>
        <adw:RibbonToggleButton.LargeImage>
            <BitmapImage x:Uid="BitmapImage_2" UriSource="Resources/Toggle.bmp"/>
        </adw:RibbonToggleButton.LargeImage>
    </adw:RibbonToggleButton>
Complete sample with source code is available at Github : SimpleToggleButton

## 评论

**内容**: duck life said...
The details are very unique, so I must adhere to you.
Reply
11/20/2022 at 10:58 PM

---
**内容**: territorial io said...
I always enjoy reading the articles that are posted here. You are doing a great work
Reply
12/27/2022 at 08:41 PM

---
**内容**: capybara clicker said...
Thanks for your information, it was really very helpfull.
Reply
02/09/2023 at 07:08 PM

---
**内容**: redactle said...
I have read this article. I think You put a lot of effort into creating this article. I appreciate your work.
Reply
02/10/2023 at 01:36 AM

---
**内容**: Tyrone Pitts said...
It has limited compatibility with which version of the machine to perform button switching geometry dash lite.
Reply
03/12/2023 at 07:19 PM

---
**内容**: bensonclark said...
Thanks for sharing this best stuff with us! Keep sharing! I am new in blog writing. All types of blogs and posts are not helpful for the readers. Here the author is giving good thoughts and suggestions to each and every reader through this article. pay to write my assignment literature-essay Quality of the content is the main element of the blog and this is the way of writing and presenting.
Reply
06/06/2023 at 02:33 AM

---
**内容**: spanish dictionary, spanish to english said...
What's going on I'm new to this, I just discovered this by accident. I found It very helpful and it helped me a lot. I hope to contribute and help other users like it helped me. You did a great job.
Reply
06/15/2023 at 02:37 AM

---
**内容**: doodle cricket said...
That is very thorough and straightforward for us to understand.
Reply
10/08/2023 at 07:15 PM

---
**内容**: mapquest driving directions said...
This is, in my opinion, one of the best posts that you have made. Your work is quite outstanding in both quality and quantity. I am grateful to you for it.
Reply
11/08/2023 at 12:53 AM

---
