---
title: "Modify Ribbon"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - CUI
description: "I would like to modify the Ribbon content - add/remove panels, etc. How could I do it?"
author: Autodesk
---
# Modify Ribbon

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/modify-ribbon.html

## 文章内容

By Adam Nagy
I would like to modify the Ribbon content - add/remove panels, etc. How could I do it?
Solution
This is only available through the .NET API's.
There are two sets of functionalities:
1) Ribbon Runtime API - provided by AdWindows.dll under Autodesk.Windows namespace
Enables you to edit the Ribbon, but the changes will not be persisted in the CUIx file, so if AutoCAD is restarted, or even if the current workspace is changed (WSCURRENT system variable) or the menu file is reloaded then the changes will be gone and you need to redo them.
Here is a small sample that toggle's the visiblity of the Home tab:
[CommandMethod("HideShowHomeTab")]
static public void HideShowHomeTab()
{
  Autodesk.Windows.RibbonControl rc =
    Autodesk.Windows.ComponentManager.Ribbon;
    Autodesk.Windows.RibbonTab tab =
    rc.FindTab("ACAD.ID_TabHome3D");
    if (tab != null)
    tab.IsVisible = !tab.IsVisible;
}
2) CUI API - provided by AcCui.dll under Autodesk.AutoCAD.Customization namespace
You can use this to modify the user interface by modifying the CUIx file the same way as through the CUI Dialog and these changes will be persisted.
This sample as well toggles the visibility of the Home tab, but using the CUI API:
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [CommandMethod("HideShowHomeTabInCurrentWorkspace")]
static public void HideShowHomeTabInCurrentWorkspace()
{
  string menuName =
    (string)acApp.GetSystemVariable("MENUNAME");
    string curWorkspace =
    (string)acApp.GetSystemVariable("WSCURRENT");
    Autodesk.AutoCAD.Customization.CustomizationSection cs =
    new Autodesk.AutoCAD.Customization.CustomizationSection(
      menuName + ".cuix");
    Autodesk.AutoCAD.Customization.WSRibbonRoot rr =
    cs.getWorkspace(curWorkspace).WorkspaceRibbonRoot;
    Autodesk.AutoCAD.Customization.WSRibbonTabSourceReference tab =
    rr.FindTabReference("ACAD", "ID_TabHome3D");
    if (tab != null)
    tab.Show = !tab.Show;
    if (cs.IsModified)
  {
    cs.Save();
      // Reload to see the changes
    acApp.ReloadAllMenus();
  }
}
Note: The above samples only work without modification in case of using vanilla AutoCAD (where the menu group is ACAD) and inside 3D Modeling workspace (where the Home tab's id is ID_TabHome3D)

## 评论

**内容**: dryman@poczta.onet.pl said...
How can I do the same in VC++ ObjectARX2012??
Reply
10/29/2012 at 04:40 AM

---
**内容**: Adam Nagy said...
Hi there,
You need to use the .NET API for that. It has no equivalent in ARX.
Perhaps you could make your ARX mixed managed, so that it can use both the C++ ARX and the .NET API functions.
Cheers,
Adam
Reply
10/29/2012 at 06:00 AM

---
**内容**: BlackBox said...
Adam,
How does one successfully add a RibbonTab to Main CUI via Initialize(), so that it (the custom RibbonTab) is available prior to partial CUIx being loaded via Autoloader?
Multiple Autoloader plug-ins with partial CUIx targeting the same custom Alias, if the custom RibbonTab has not been added to Main CUI first, then each partial CUIx displays it's own RibbonTab instead of adding to custom RibbonTab in Main CUI.
Please advise.
Reply
04/19/2013 at 04:58 PM

---
**内容**: Fenton Webb said...
Hey BlackBox,
you should not modify the Ribbon from initialize()... that function is called too early in the startup if called to load on startup.
Best is to use the StartupCommand attribute on the Command element... This will call your own initialize command when AutoCAD has fully initialized. e.g.







Reply
04/22/2013 at 11:19 AM

---
**内容**: Fenton Webb said...
removing the less than and greater than signs (sigh)
Components Description="Any CPU DLLs"
RuntimeRequirements OS="Win32|Win64" Platform="AutoCAD|AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.0" /
ComponentEntry AppName="MyDotNetApp" Version="1.0.0" ModuleName="./Contents/Windows/R19.0/MyApp.dll"
Commands
Command Local="_MyAppStartupCmd" Global="MyAppStartupCmd" StartupCommand="True" /
/Commands
/ComponentEntry
Reply
04/22/2013 at 11:20 AM

---
**内容**: Fenton Webb said...
this is better
http://adndevblog.typepad.com/autocad/2013/04/autoloader-example-for-invoking-a-startup-command-in-autocad.html
Reply
04/22/2013 at 11:47 AM

---
**内容**: BlackBox said...
Thanks for the response, Fenton.
I'm aware that one cannot actually modify the Ribbon on Initialize()... In practice I use Initialize() to hook Application.Idle (not sure why I neglected that above, but still).
In any event, essentially (if I am understanding you correctly), Autoloader is incapable of successfully allowing for a plug-in to modify Main CUI prior to the loading of a given .bundle's CUIx partial(s) so that RibbonTab's with matching Alias can properly be merged into single tab... AutoCAD has no work around for the Main CUI dependency... And instead, I need to delay the loading of my plug-in's UI components to call SendStringToExecute (effectively, if not literally), just to get my custom ComandMethod to modify Main CUI prior to programmatically loading my .bundle's CUIx partial(s).
... Any insight on when that mess... And the 'residue' duplication of .bundle CUIx files being replicated to each-and-every-installation's ..\Support\ folder... Are going to be addressed?
Cheers
Reply
04/22/2013 at 04:15 PM

---
**内容**: rohan hirave said...
hi, can any1 upload the sample code for ribbon customization please. I am a newbie in autocad customization and i want to add a new ribbon in autocad.
Reply
02/05/2015 at 04:42 AM

---
**内容**: Balaji said in reply to rohan hirave...
Hi Rohan,
These blog post should provide samples to get started.
Using the ribbon runtime API is easier.
http://through-the-interface.typepad.com/through_the_interface/2008/04/the-new-ribbonb.html
http://adndevblog.typepad.com/autocad/2014/01/how-to-ensure-your-ribbon-runtime-items-remain-visible.html
The other way could be to create a partial CUIX directly using AutoCAD CUI dialog and load the partial cuix using code.
Regards,
Balaji
Reply
02/06/2015 at 02:42 AM

---
**内容**: Luigi said...
After running the code shown above, in order to make "MyTab" visible I must switch to AutoCAD Classic display style and then switch back in a ribbon display style (3D or 3D Modeling Basics) because the tab becomes visible, otherwise the tab ("MyTab") remains invisible.
I can not understand the reason for this behavior.
Autocad 2014, W7 x64
Thank you in advance.
Luigi
Reply
10/10/2015 at 11:04 PM

---
**内容**: Luigi said...
Hello all,
I apologize for the wrong post a few minutes ago, so:
I'm trying to display "MyTab" on the ribbon with the following instructions:
[the same code listed above]
Autodesk.AutoCAD.Customization.WSRibbonTabSourceReference MyTab =
rr.FindTabReference("MyGroup", "MyTab");
MyTab.Show = True
[the same code listed above]
After running the code shown above, in order to make "MyTab" visible I must switch to AutoCAD Classic display style and then switch back in a ribbon display style (3D or 3D Modeling Basics) because the tab becomes visible, otherwise the tab ("MyTab") remains invisible.
I cannot understand the reason for this behavior.
Autocad 2014, W7 x64
Thank you in advance.
Luigi
Reply
10/10/2015 at 11:08 PM

---
**内容**: Balaji said...
Hi Luigi,
Yes, this is a known behavior and for any cui related changes to take effect, we either need to reload the cuix. I have also seen in the past that changing WSCURRENT also helps.
Please try the "savecui" method from this blog post and see if that helps without having to change the current workspace.
http://adndevblog.typepad.com/autocad/2015/10/docking-toolbars-in-rows-using-cui-api.html
Regards,
Balaji
Reply
10/15/2015 at 10:06 PM

---
**内容**: Luigi said...
Balaji, thankyou for the support,
in the meanwhile I tried the following (.net):
Dim curWorkspace As String = _ DirectCast(Autodesk.AutoCAD.ApplicationServices.Application. _
GetSystemVariable("WSCURRENT"), String)
Dim cs As CustomizationSection = New CustomizationSection(DirectCast(Autodesk.AutoCAD. _
ApplicationServices.Application.GetSystemVariable("MENUNAME"), String))
cs.Save()
Autodesk.AutoCAD.ApplicationServices.Application.ReloadAllMenus()
And seems work fine.
The crux of the problem seems to be: Autodesk.AutoCAD.ApplicationServices.Application.ReloadAllMenus()
Reply
10/20/2015 at 12:52 AM

---
**内容**: Adam Nagy said in reply to Luigi...
Hi Luigi,
It sounds like you omitted the acApp.ReloadAllMenus() call and that caused the problem.
I assume that the problem is that I missed out the "using acApp = Autodesk.AutoCAD.ApplicationServices.Application;" statement (because that was at the top of my file) and that caused the confusion.
I'll add it to the code to make things clear.
Cheers,
Adam
Reply
10/20/2015 at 02:09 AM

---
**内容**: Albert Weber said...
Hi there,
does anyone have an example to access the customization of a partial cuix?
I tried several methods of the original post, which are working perfect for the main cuix, but always get returned null, e.g. searching the tab of my partial menu, or the QAT, or a ribbon panel.
Thanks,
Albert
Reply
10/23/2019 at 02:33 AM

---
**内容**: Madhukar Moogala said...
Hi Albert,
Can you please refer this blog, https://adndevblog.typepad.com/autocad/2014/08/using-cuix-resource-dll-with-image-transparency.html
This has a very good sample on partial CUI, download the zip file at the end of the article
Reply
10/23/2019 at 02:52 AM

---
