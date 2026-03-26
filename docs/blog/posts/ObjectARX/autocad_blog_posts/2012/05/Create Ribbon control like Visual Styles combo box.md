---
title: "Create Ribbon control like Visual Styles combo box"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can use the RibbonGallery control to achieve that:"
author: Autodesk
---
# Create Ribbon control like Visual Styles combo box

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/create-ribbon-control-like-visual-styles-combo-box.html

## 文章内容

By Adam Nagy
You can use the RibbonGallery control to achieve that:
using System;
  using Autodesk.AutoCAD.Runtime;
using Autodesk.Windows;
  [assembly:CommandClass(typeof(TestProject.Commands))]
  namespace TestProject
{
  public class Commands
  {
    [CommandMethod("CreateMyGallery")]
    public void CreateMyGallery()
    {
      RibbonControl ribbon = ComponentManager.Ribbon;
        RibbonTab tab = new RibbonTab();
      tab.Name = "MyTab";
      tab.Title = "My Tab";
      tab.Id = "MyTabId";
      ribbon.Tabs.Add(tab);
        RibbonPanelSource panelSrc = new RibbonPanelSource();
      panelSrc.Name = "MyPanel";
      panelSrc.Title = "My Panel";
      panelSrc.Id = "MyPanelId";
        RibbonGallery gallery = new RibbonGallery();
      gallery.Name = "MyGallery";
      gallery.Id = "MyGalleryId";
        RibbonButton button1 = new RibbonButton();
      button1.Name = "MyButton";
      button1.Text = "My Button";
      button1.Id = "MyButtonId";
      gallery.Items.Add(button1);
        RibbonButton button2 = new RibbonButton();
      button2.Name = "MyOtherButton";
      button2.Text = "My Other Button";
      button2.Id = "MyOtherButtonId";
      gallery.Items.Add(button2);
        gallery.DisplayMode = GalleryDisplayMode.ComboBox;
        panelSrc.Items.Add(gallery); 
        RibbonPanel panel = new RibbonPanel();
      panel.Source = panelSrc;
        tab.Panels.Add(panel);
    }
  }
}

## 评论

**内容**: Anton said...
The ribbon variable should be tested for NULL to prevent AutoCAD 2013 to crash
RibbonControl ribbon = ComponentManager.Ribbon;
if (ribbon == null)
{
ed.WriteMessage("\nNo Ribbon");
return;
}
Reply
05/15/2012 at 03:23 AM

---
**内容**: Adam Nagy said...
Thank you for the commment, Anton!
Reply
05/15/2012 at 05:09 AM

---
**内容**: Veli V. said...
How can I populate RibbonCombo with text values using .NET API?
I have not find working example yet...
Private Sub InitRibbonCombo(ByRef cbo As Autodesk.Windows.RibbonCombo, ByVal lst As List(Of String))
If cbo Is Nothing Then Return
cbo.Items.Clear()
If Not lst Is Nothing OrElse lst.Count > 0 Then
For Each sName As String In lst
cbo.Items.Add(CreateRibCboItem(sName, cbo.Items.Count))
Next sName
End If
End Sub
Private Function CreateRibCboItem(ByVal sItem As String, ByVal iIndex As Integer) As Autodesk.Windows.RibbonButton
Dim ribCboBut01 As New Autodesk.Windows.RibbonButton
ribCboBut01.Text = sItem
ribCboBut01.Id = "Id_RibCboItem" + CStr(iIndex)
ribCboBut01.ShowText = True
Return ribCboBut01
End Function
Reply
01/10/2013 at 05:44 AM

---
**内容**: Adam Nagy said...
Hi there,
As you can see in the above example you actually need to create a RibbonGallery with ComboBox display mode to create a control that looks and behave like a combo box. I seem to remember that it's not suggested to use the ComboBox class, but I could be wrong.
Any reason why you do not want to use the RibbonGallery control?
Adam
Reply
01/10/2013 at 06:14 AM

---
**内容**: Veli V. said...
Reason was that I try to put text value rows in RibbonCombo control using .NET API but I couldn´t find the way to do that. With ObjectARX I can do that using COM API but not using .NET API. I can also be wrong about that cause I have not yet found the way. =)
-Veli
Reply
01/10/2013 at 10:28 PM

---
**内容**: dba said...
Hello Adam,
I created some WPF Usercontrols (based on Fenton Webb's Performance Gauges) and added successfully to my Project.
In fact I need the tabs as sort of "contextual", by using the impliedselectionchanged event (had no better idea to filter selection...) showing/hiding them
The CUI-Loading in my case is suboptimal (although I have no other option by now)
So the question is, how to get the registered Ribboncomponent (HKLM...\Ribboncontrols) programatically.
Tried (with others):
dim rci as new Ribboncompositeitem ("keyname as in resDic")
dim dt as windows.datatemplate (gettype (myUSERcontrol))
ci.content= dt.loadcontent
...
this ci I was able to add to a PanelSource...
actually I tried to rebuild the "XAML" construct. with no luck (not surprised)
OK, I think the control shall be "loaded" anyway by the time I want to access it via my plugin so I needed to find a collection, where I could grab it from, or so.
I may be complete wrong on this...:(
I guess Acad is somewhere aware of the Components (since I can access them via CUI-Editor) I just did not find out the right way, to use them programatically (Fenton wrote in his Au-Paper (CP114-5, 2009) that "x:UID" shall used to get the control, but I had no luck so far).
My goal was to create some Ribbontabs, containing Usercontrols which I can manipulate then in the way your Code does here with "standard items" (meaning objects provided by autodesk.Windows namespace)
Thanks in advance!
Daniel
Reply
11/21/2013 at 08:12 AM

---
**内容**: Balaji said in reply to dba...
Hi Daniel,
Sorry for the delay. There was an issue posting comments in the blog.
If you have access to the xaml file, then it can be directly loaded in the ribbon panel as one of the item.
Here is a sample code :

Uri uri = new Uri("/RibbonCustCtrlDataBinding;component/MyRibbonControl.xaml", System.UriKind.Relative);
ResourceDictionary resDict = (ResourceDictionary)System.Windows.Application.LoadComponent(uri);
ribSourcePanel.Items.Add((RibbonItem)resDict["ribbonCompositeItemKey"]);
In this code the "ribbonCompositeItemKey" is the value specified in your xaml file as x:Key.
You can refer to the xaml file from the WPF webcast by my colleague Fenton Webb.
Also, you may be interested in this Devblog post that explains the way to create a contextual ribbon tab using the ribbon runtime API.
http://adndevblog.typepad.com/autocad/2012/04/displaying-a-contextual-tab-upon-entity-selection-using-ribbon-runtime-api.html
Regards,
Balaji
Reply
11/26/2013 at 09:38 PM

---
**内容**: Balaji said...
Hi Daniel,
Iam looking into this query and will get back to you soon.
Regards,
Balaji
Reply
11/24/2013 at 03:25 PM

---
