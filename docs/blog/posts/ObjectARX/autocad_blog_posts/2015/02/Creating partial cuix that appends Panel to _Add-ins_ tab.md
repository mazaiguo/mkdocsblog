---
title: "Creating partial cuix that appends Panel to "Add-ins" tab"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Plugin
description: "Here is a sample code to create a partial cuix at runtime. It creates a ribbon panel with a command button. After the cuix is loaded in AutoCAD usi..."
author: Autodesk
---
# Creating partial cuix that appends Panel to "Add-ins" tab

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/creating-partial-cuix-that-appends-panel-to-add-ins-tab.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a partial cuix at runtime. It creates a ribbon panel with a command button. After the cuix is loaded in AutoCAD using cuiload, the panel should appear in the "Add-ins" tab.
 CustomizationSection csNew = new  CustomizationSection();
 csNew.MenuGroupName = "myMenuGroup" ;
   // Create a new menu macro 
 MacroGroup myMacGroup = 
     new  MacroGroup("myMacroGroup" , 
     csNew.MenuGroup);
   MenuMacro macroLine = myMacGroup.CreateMenuMacro(
         "TestLine" , 
         "^C^C_Line " , 
         "ID_MyLineCmd" , 
         "My Line help" , 
         MacroType.Any, 
         "RCDATA_16_LINE" , 
         "RCDATA_32_LINE" , 
         "My Test Line" );
   RibbonRoot ribbonRoot = csNew.MenuGroup.RibbonRoot;
   // Create a panel 
 RibbonPanelSource ribPanelSource
                 = new  RibbonPanelSource(ribbonRoot);
 ribPanelSource.Text = "MyPanel" ;
   // Create a ribbon row 
 RibbonRow ribRow = new  RibbonRow();
 ribPanelSource.Items.Add((RibbonItem)ribRow);
   //Create a Ribbon Command Button 
 RibbonCommandButton ribCommandButton 
                    = new  RibbonCommandButton(ribRow);
 ribCommandButton.Text = "MyTestLineButton" ;
 ribCommandButton.MacroID = macroLine.ElementID;
   //Add the ribbon command button to the ribbon row  
 ribRow.Items.Add((RibbonItem)ribCommandButton);
   //Get the panels from the RibbonRoot  
 RibbonPanelSourceCollection panels 
                 = ribbonRoot.RibbonPanelSources;
   // Add the Ribbon Panel Source to the Ribbon Panels  
 panels.Add(ribPanelSource);
   RibbonTabSourceCollection tabs 
                     = ribbonRoot.RibbonTabSources;
   // Create a new Ribbon Tab Source  
 RibbonTabSource tabSrc 
                 = new  RibbonTabSource(ribbonRoot);
 tabSrc.Name = "MyTab" ;
 tabSrc.Text = "MyTab" ;
 tabSrc.ElementID = "MyTabElementID" ;
 tabSrc.Aliases.Add("ID_ADDINSTAB" );
 tabSrc.WorkspaceBehavior 
             = TabWorkspaceBehavior.MergeOrAddTab;
 tabs.Add(tabSrc);
   if  (tabSrc != null )
 {
     //Add the Panel to the Tab  
     RibbonPanelSourceReference ribPanelSourceRef 
             = new  RibbonPanelSourceReference(tabSrc);
     ribPanelSourceRef.PanelId 
             = ribPanelSource.ElementID;
     ribPanelSourceRef.ElementID = "MyPanelID" ;
     tabSrc.Items.Add(ribPanelSourceRef);
 }
   csNew.SaveAs(strCuiFile);

## 评论

**内容**: Jörg Weber said...
Hi,
that sounds very interetsing.
But i'm not a programmer and I ask my what must I do with the code.
Do I copy and paste it in VB MArcos or save the code in an external file and load it in AutoCAD.
Perhaps you can help me understanding
thanks a lot
Reply
03/07/2015 at 06:58 AM

---
**内容**: Balaji said in reply to Jörg Weber...
Hi Jorg,
The code is in this blog post requires compiling using Visual Studio. If you are not a programmer and would like to include your ribbon tab in the Addins tab, it is possible to do that by creating a partial cuix using CUI dialog inside AutoCAD. This video should help :
http://download.autodesk.com/media/adn/DevTV_Creating_a_Partial_CUI/DevTV_Creating_a_Partial_CUI.html
Regards,
Balaji
Reply
03/08/2015 at 09:37 PM

---
**内容**: Health Tourism said...
This is great news! Finally, someone with some spunk is perhaps showing some interest in Dzhokhar’s innocence.
Reply
03/09/2015 at 08:04 AM

---
**内容**: YASSER MAHMOUD said...
Thanks, finally i found
Reply
10/23/2015 at 03:12 AM

---
**内容**: Dale Bartlett said...
I receive a warning in AutoCAD 2014 on this line:
RibbonRow ribRow = new RibbonRow();
which advises:
Autodesk.AutoCAD.Customization.RibbonRow.RibbonRow()' is obsolete: 'This constructor is for internal use only and may not be available in a later release.
I have not been able to find any information regarding this. Thanks, Dale
Reply
03/08/2016 at 05:12 AM

---
