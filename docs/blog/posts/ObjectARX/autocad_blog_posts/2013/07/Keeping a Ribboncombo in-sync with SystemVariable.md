---
title: "Keeping a Ribboncombo in-sync with SystemVariable"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to display a ribboncombo that lists the possible values for LUNITS system variable and remains in-sync with the changes to it..."
author: Autodesk
---
# Keeping a Ribboncombo in-sync with SystemVariable

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/keeping-a-ribboncombo-in-sync-with-systemvariable.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to display a ribboncombo that lists the possible values for LUNITS system variable and remains in-sync with the changes to it. The use of LUNITS is only for demo purpose and the sample code can be modified to do the same with any other AutoCAD system variable.
// AcMgd.dll
using Autodesk.AutoCAD.Windows.Data;
// AdWindows.dll
using Autodesk.Windows;
// AcWindows.dll
using Autodesk.AutoCAD.Ribbon;
  public class ExtApp : IExtensionApplication
{
    private String[] lunitValues = new String[]
                                          { "1 - Scientific",
                                            "2 - Decimal",
                                            "3 - Engineering",
                                            "4 - Architectural",
                                            "5 - Fractional"
                                          };
      // Creates a ribbon tab, panel and a ribbon combo for LUNITS
    [CommandMethod("Test")]
    public void createLUNITSRibbonCombo()
    {
        RibbonControl ribCntrl
              = RibbonServices.RibbonPaletteSet.RibbonControl;
          RibbonTab ribTab = new RibbonTab();
        ribTab.Title = "My custom tab";
        ribTab.Name = "MyTab";
        ribTab.Id = "MY_TAB_ID";
        ribCntrl.Tabs.Add(ribTab);
          RibbonPanelSource ribSourcePanel = new RibbonPanelSource();
        ribSourcePanel.Title = "MyPanel1";
        RibbonPanel ribPanel = new RibbonPanel();
        ribPanel.Source = ribSourcePanel;
        ribTab.Panels.Add(ribPanel);
          RibbonCombo lunitsRibbonCombo = new RibbonCombo();
        lunitsRibbonCombo.Name = "LUNITSCombo";
        lunitsRibbonCombo.Id = "AdskLUNITSCombo";
        System.Windows.Data.Binding bind1
                           = new System.Windows.Data.Binding();
        bind1.Source = lunitValues;
        lunitsRibbonCombo.ShowText = true;
        lunitsRibbonCombo.Size = RibbonItemSize.Large;
        lunitsRibbonCombo.ShowImage = false;
        lunitsRibbonCombo.ItemsSourceBinding = bind1;
          System.Windows.Data.Binding bind2
                           = new System.Windows.Data.Binding();
        bind2.Path = new System.Windows.PropertyPath(".");
        lunitsRibbonCombo.ItemTemplateTextBinding = bind2;
          // Set its intial value
        Int16 index = (Int16)
        Application.UIBindings.SystemVariables["LUNITS"].Value;
          lunitsRibbonCombo.Current = lunitValues[index];
          lunitsRibbonCombo.CurrentChanged
            += new EventHandler<RibbonPropertyChangedEventArgs>
                                    (ribCombo_CurrentChanged);
          ribSourcePanel.Items.Add(lunitsRibbonCombo);
          ribTab.IsActive = true;
    }
      // Callback to track changes to LUNIT made using the combobox
    // Update the system variable based on the changes
    void ribCombo_CurrentChanged
                        (
                            object sender,
                            RibbonPropertyChangedEventArgs e
                        )
    {
        ILookup<SystemVariable> sysvars
                       = Application.UIBindings.SystemVariables;
        SystemVariable sv = sysvars["LUNITS"];
        String newValue = e.NewValue.ToString();
        int lunits = 1;
          // Set the system variable based on the combobox new value
        if (int.TryParse(newValue[0].ToString(), out lunits))
        {
            if (!lunits.ToString().Equals(
                Application.UIBindings.SystemVariables["LUNITS"]
                                            .Value.ToString()))
            {
                Application.UIBindings.SystemVariables["LUNITS"]
                                               .Value = lunits;
            }
        }
    }
      // Callback to track changes to LUNIT system variable.
    // Update the combobox value based on the changes
    void sv_PropertyChanged(
                                object sender,
                                PropertyChangedEventArgs e
                            )
    {
        SystemVariable sv = sender as SystemVariable;
        Type svType = sv.GetType();
        PropertyInfo pi = svType.GetProperty(e.PropertyName);
        object propValue = pi.GetValue(sv, null);
        String typeName = propValue.GetType().Name;
          Int16 lunits = (Int16)propValue;
          RibbonControl ribCntrl
                = RibbonServices.RibbonPaletteSet.RibbonControl;
        RibbonItem ri = ribCntrl.FindItem("AdskLUNITSCombo", false);
        RibbonCombo ribbonCombo = ri as RibbonCombo;
          if (ribbonCombo != null)
        {
            object currentItem = ribbonCombo.Current;
            if (!currentItem.ToString().Equals(
                                    lunitValues[lunits - 1]))
            {
                ribbonCombo.Current = lunitValues[lunits - 1];
            }
        }
    }
      void IExtensionApplication.Initialize()
    {
        // Register the event handler to monitor any changes
        // to the LUNITS system variable
        ILookup<SystemVariable> sysvars
                      = Application.UIBindings.SystemVariables;
        SystemVariable sv = sysvars["LUNITS"];
        sv.PropertyChanged
         += new PropertyChangedEventHandler(sv_PropertyChanged);
    }
      void IExtensionApplication.Terminate()
    {
        // Unregister the event handler
        ILookup<SystemVariable> sysvars
                      = Application.UIBindings.SystemVariables;
        SystemVariable sv = sysvars["LUNITS"];
        sv.PropertyChanged
       -= new PropertyChangedEventHandler(sv_PropertyChanged);
    }
}

## 评论

**内容**: Craig said...
Hi Balaji,
Please can you explain the purpose of the second binding?
System.Windows.Data.Binding bind2 = new System.Windows.Data.Binding();
bind2.Path = new System.Windows.PropertyPath(".");
lunitsRibbonCombo.ItemTemplateTextBinding = bind2;

Thanks
Reply
07/29/2016 at 07:01 AM

---
**内容**: Charles said...
Thanks for the post
Reply
06/28/2017 at 01:46 AM

---
