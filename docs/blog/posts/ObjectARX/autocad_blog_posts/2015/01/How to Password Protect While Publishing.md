---
title: "How to Password Protect While Publishing"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - API
  - DWG
description: "In this blog I will be discussing how can we allows users to password protect while publishing documents programmatically , as there is no direct A..."
author: Autodesk
---
# How to Password Protect While Publishing

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/how-to-password-protect-while-publishing.html

## 文章内容

By Madhukar Moogala
In this blog I will be discussing how can we allows users to password protect while publishing documents programmatically , as there is no direct API to allow user to enter password ,we need to rely on some other means , for this I have two workarounds,
First and foremost is to edit the DSD file [ASCII compatible],find for the strings “PromptForPwd = FALSE” and “PwdProtectPublishedDWF = FALSE” and replace strings with TRUE attribute, something like this, here is only a snippet but you can find fully usage in this forum which I’ve written. PasswordProtect , those who are not aware of programmatically execute publish DSD please find helpful resource 
/*DsdFile */
string dsdFile = dsdData.ProjectPath + dwgFileName + ".dsd";
dsdData.WriteDsd(dsdFile);
System.IO.StreamReader sr = new System.IO.StreamReader(dsdFile);
string str = sr.ReadToEnd();
sr.Close();
str = str.Replace("PromptForDwfName=TRUE",
                   "PromptForDwfName=FALSE");
/*Prompts User to Enter Password and Reconfirms*/
str = str.Replace("PromptForPwd=FALSE",
                   "PromptForPwd=TRUE");
str = str.Replace("PwdProtectPublishedDWF=FALSE",
                   "PwdProtectPublishedDWF=TRUE");
  Second, is to use WPF PasswordBoxx API, I’ve was not aware of WPF earlier but this task led me to learn WPF and it was interesting to have this in my bucket, WPF experts looking at this blog are welcome to put suggestions and improvements.
There are few pundits suggesting web developers not to use PasswordBox as storing password in text form is prone to security risks,but I feel this would be significant in complex MVVM projects.And there are tricks like PBDataBinding to use this API with out loosing MVVM pattern architecture, as Password property of the API is not a dependency object we may lost pattern design,anyway we should not be bothering much about this fact in our case.
So, retrieve password from user  and assign it to our DsdData.Password API. WPF PasswordBox API allows us to mask characters while entering and which is most desired.
Sample XAML:
  <Window x:Class="PWDProtectionPlot.PasswordWindow"
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
Title="PasswordWindow" Height="88.746" Width="300">
<StackPanel>
<Label Content="Password:" />
<PasswordBox x:Name="passwordBox"
             Width="130"
             MaxLength="8"
             Focusable="True"
             GotFocus="passwordBox_GotFocus"
             KeyDown="passwordBox_KeyDown">
<PasswordBox.ToolTip>
<ToolTip ToolTipService.ShowDuration="20">
<StackPanel>
<TextBlock FontWeight="Light">
Eight (8)" characters.Press Enter to OK
</TextBlock>
</StackPanel>
</ToolTip>
</PasswordBox.ToolTip>
</PasswordBox>        
</StackPanel>
</Window>
Sample associated C# code:
public partial class PasswordWindow : Window
{
public PasswordWindow()
{
InitializeComponent();
}
/*Password Changed Handler*/
private void passwordBox_PasswordChanged(object sender, RoutedEventArgs e)
{
if (passwordBox.Password.Length == 8)
passwordBox.PasswordChanged -= passwordBox_PasswordChanged;
}
/*We 'll close our password window when Enter key is pressed */
private void passwordBox_KeyDown(object sender, KeyEventArgs e)
{
if (e.Key == Key.Enter) if (passwordBox.Password.Length < 8)
MessageBox.Show("Password Should be of \"Eight\"(8) Characters");
else
{
e.Handled = true;
this.Close();
}
}
/*We'll trigger password changed handler when we get focus*/
private void passwordBox_GotFocus(object sender, RoutedEventArgs e)
{
passwordBox.PasswordChanged += passwordBox_PasswordChanged;
}
}
}
  Our WPF widget looks like,
  Full source code can be downloaded.
Demo video is available at.

