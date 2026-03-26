---
title: "Associating F1 help with ribbon button"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I want to display a custom chm file when F1 is pressed while the ribbon button tooltip displays "Press F1 for more help". Can you provide me an exa..."
author: Autodesk
---
# Associating F1 help with ribbon button

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/associating-f1-help-with-ribbon-button.html

## 文章内容

By Balaji Ramamoorthy
Issue
I want to display a custom chm file when F1 is pressed while the ribbon button tooltip displays "Press F1 for more help". Can you provide me an example ?
Solution
The "HelpSource" and "HelpTopic" properties of the RibbonItem class have to be set for AutoCAD to display your chm file. "HelpSource" is the Uri to the chm file and the "HelpTopic" is the topic id of the page in the chm file.
Here is the code snippet. You may need to modify the "HelpSource" and "HelpTopic" strings to point to the chm file in your system and to a topic id in it. Also, add the "AdWindows.dll" to the references in your project
// From AdWindows.dll
using Autodesk.Windows;
public class MyCommands
{
    [CommandMethod("CRB")]
    public void createRibbonButton()
    {
        Autodesk.Windows.RibbonControl ribCntrl =
        Autodesk.AutoCAD.Ribbon.RibbonServices.RibbonPaletteSet.RibbonControl;
        //add the tab
        RibbonTab ribTab = new RibbonTab();
        ribTab.Title = "My custom tab";
        ribTab.Id = "MY_TAB_ID";
        ribCntrl.Tabs.Add(ribTab);
        //create the panel source
        Autodesk.Windows.RibbonPanelSource ribSourcePanel
                                    = new RibbonPanelSource();
        ribSourcePanel.Title = "Controls";
        //now the panel
        RibbonPanel ribPanel = new RibbonPanel();
        ribPanel.Source = ribSourcePanel;
        ribTab.Panels.Add(ribPanel);
        Autodesk.Windows.RibbonToolTip ribToolTip
                                        = new RibbonToolTip();
        ribToolTip.Command = "My Command";
        ribToolTip.Title = "My Title";
        ribToolTip.Content = "My Content";
        ribToolTip.ExpandedContent = "My Expanded Content !";
          // Without this "Press F1 for help" does not appear in the tooltip
        ribToolTip.IsHelpEnabled = true;
        Autodesk.Windows.RibbonButton ribButton
                                        = new RibbonButton();
        ribButton.Text = "PLINE";
        ribButton.ShowText = true;
        ribButton.CommandParameter = "\x1b\x1b_PLINE ";
        ribButton.CommandHandler = new AdskCommandHandler();
        ribButton.HelpSource
            = new System.Uri(
                                @"C:\Temp\ToolTipDemo.chm",
                                UriKind.RelativeOrAbsolute
                            );
        ribButton.HelpTopic = "CreateLayer";
        ribButton.IsToolTipEnabled = true;
        ribButton.ToolTip = ribToolTip;
        ribSourcePanel.Items.Add(ribButton);
        ribTab.IsActive = true;
    }
}
public class AdskCommandHandler : System.Windows.Input.ICommand
{
    public bool CanExecute(object parameter)
    {
        return true;
    }
    public event EventHandler CanExecuteChanged;
    public void Execute(object parameter)
    {
        RibbonButton ribBtn = parameter as RibbonButton;
        if (ribBtn != null)
        {
            Application.DocumentManager.MdiActiveDocument.SendStringToExecute
                (
                    (String)ribBtn.CommandParameter, true, false, true
                );
        }
    }
}

## 评论

**内容**: Modis said...
Hi. I have made reference to many functions in a single .chm file. How do to open a particular page of help
Sorry for my English - used an online translator
Reply
09/05/2012 at 02:53 PM

---
**内容**: Owen Wengerd said in reply to Modis...
Try appending the path to the page like this "C:\Temp\ToolTipDemo.chm::/page.htm". This is just a guess; it works this way when opening a chm in internet explorer, so I'll bet it works the same way here.
Reply
09/05/2012 at 06:30 PM

---
**内容**: Andrey said in reply to Modis...
Look constructors of CommandMethod attribute (open ObjectARX SDK).
Quote from SDK:
public CommandMethodAttribute(
string groupName,
string globalName,
string localizedNameId,
CommandFlags flags,
Type contextMenuExtensionType,
string helpFileName,
string helpTopic
);
string helpTopic - Input help topic string.
Reply
09/05/2012 at 11:26 PM

---
**内容**: Andrey said in reply to Modis...
My simply example:
[AcRtm.CommandMethod("myNS", "myCMD", "myCMD_localizedId", AcRtm.CommandFlags.Modal, null, "myHelp.chm", @"plotting_layouts")]
Pay attention:
Full name of help page such:
mk:@MSITStore:C:\Documents%20and%20Settings\developer\Рабочий%20стол\myHelp.chm::/plotting_layouts.htm
but in last parameter I set file name only, without extention.
Reply
09/05/2012 at 11:38 PM

---
**内容**: Adriano said...
this function works for the starting AutoCAD 2012
ribButton.HelpTopic = "CreateLayer";
but for AutoCAD 2010 and 2011 as I proceed
Reply
03/15/2013 at 05:50 AM

---
**内容**: Balaji said in reply to Adriano...
Hi Adriano,
In AutoCAD 2011, when F1 is pressed with mouse hovering over the ribbon button, the custom help from the CHM does get invoked but along with the AutoCAD’s default help.
This behavior was fixed in AutoCAD 2012. Sorry, I am not aware of any workaround for this to work correctly in AutoCAD 2011.
Reply
03/18/2013 at 02:34 AM

---
