---
title: "Using custom contextual ribbon tabs"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Selection
  - Unicode
description: "In AutoCAD when you start editing an MTEXT, then a Text Editor contextual tab appears in the Ribbon. How could I do something similar myself? E.g. ..."
author: Autodesk
---
# Using custom contextual ribbon tabs

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/using-custom-contextual-ribbon-tabs.html

## 文章内容

By Adam Nagy
In AutoCAD when you start editing an MTEXT, then a Text Editor contextual tab appears in the Ribbon. How could I do something similar myself? E.g. when the user selects my custom entity then my own contextual tab would appear.
Solution
If you already have a contextual tab and you want to hook it up, so that it is shown under certain conditions then this is what you have to do.
1) You have to create a contextual selection rule xaml file.
You need to name it in a way that it ends with ContextualTabSelectorRules.xaml and starts with something that makes it unique. The best thing is to use your Registered Developer Symbol for that purpose
[RDS - Registered Developer Symbol: visit http://www.autodesk.com/developer and select Symbol Registration]
So mine would be AEN1ContextualTabSelectorRules.xaml
You can have a look at the [AutoCAD install folder]\AcContextualTabSelectorRules.xaml file for ideas on what our xaml needs to contain.
On Vista and Windows 7 be careful if you copy and edit the AcContextualTabSelectorRules.xaml file. In that case take care about disabling the UAC when editing the copied file: with UAC enabled the copy operation works (requests administrator rights) but the editing writes transparently into the VirtualStore (because of limited rights), i.e. the original file is still just the copy and the subsequent changes are in a different place and only visible to the editor.
2) In the rule you create you can either use already available functions like Selection.ContainsOnly("Arc") or create your own assembly with some utility functions and use them from the selector rules file. That's what we'll do in this sample.
As you can see we will create an assembly called Aen1Helper with a Functions class that has a static function called ShowMyTab and then we can use it in the Aen1ContextualTabSelectorRules.xaml file the following way:
<?xml version="1.0" encoding="utf-8"?>
  <TabSelectorRules 
    xmlns="clr-namespace:Autodesk.AutoCAD.Ribbon;assembly=AcWindows"
    Ordering="0"
    >
    <TabSelectorRules.References>
        <AssemblyReference Namespace="Aen1Helper" Assembly="Aen1Helper"/>
    </TabSelectorRules.References>
      <Rule Uid="Aen1SelctionRule" DisplayName="Aen1 Selecion Rule"
        Theme="Green" Trigger="Selection"
        >
        <![CDATA[
             Aen1Helper.Functions.ShowMyTab(Selection)
        ]]>
    </Rule>
</TabSelectorRules>
3) Then create a simple Class Library in Visual Studio which references acmgd.dll, acdbmgd.dll and WindowsBase assemblies [make sure that Copy Local is set to false for all of them]. You could implement any logic for controlling the appearance of your tab, but we'll do something simple. Our rule will be based on the type of entity being selected and the name of the current document.
using System;
  using Autodesk.AutoCAD.Windows.Data;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.ApplicationServices;
  namespace Aen1Helper
{
  public class Functions
  {
    public static bool ShowMyTab(object selObj)
    {
      Selection sel = (Selection)selObj;
      if (sel.Count < 1 || !sel.ContainsOnly(new string[] {"Line"}))
        return false;
        if (Application.DocumentManager.MdiActiveDocument.
        Name.EndsWith("Drawing1.dwg"))
        return true;
        return false;
    }
  }
}
4) Once both AEN1ContextualTabSelectorRules.xaml and Aen1Helper.dll have been placed in the AutoCAD install folder you can start AutoCAD and go into the CUI dialog to associate your rule with your contextual tab. Mine is called Aen1Tab.
Just drag Ribbon > Tabs > Aen1Tab onto Ribbon > Contextual Tab States > Aen1 Selection Rule and click OK
Now when you select a line in a document whose name ends with Drawing1.dwg then Aen1 Tab will appear

## 评论

**内容**: Jonathan said...
Hi,
Thank you for this good post.
Is there a way to embed the ContextualTabSelectorRules.xaml and Helper.dll files in the CUIx? It is not always easy to put into the installation folder...
Regards,
Jonathan
Reply
03/21/2013 at 07:23 AM

---
**内容**: Adam Nagy said...
Hi Jonathan,
Sorry about the late reply and also about the fact that what you outlined cannot be done :(
Cheers,
Adam
Reply
04/11/2013 at 08:51 AM

---
**内容**: dba said...
Hello Adam,
has the reference Assembly to be placed in the Programfoder?
In my scenario I have an Autoloaded plugin including a cuix for my Tabs (Since custom WPF-Controls I had to go the way, althought I didn't want to use CUI...). Currently I load them by impliedselectionchanged event (certain Blockref's selected -> Tab visible). It could be easier (and maybe more safe - object editing in an active Event...) to activate the Tabs Contextually by rules. But if I read this correctly, I had to place my whole Plugin in the Programfolder, which I'm not comfortable with.
Best Regards,
Daniel
Currently working on ACA2012 x64 - Plugin
Reply
12/09/2013 at 05:44 AM

---
**内容**: dba said in reply to dba...
Tested, no need of the dll being in the Programfolder :)

BR,
Daniel
Reply
12/09/2013 at 06:17 AM

---
**内容**: Adam Nagy said in reply to dba...
Thanks Daniel for testing.
I would have not known the answer off the top of my head. Haven't played with this thing for quite some time. :)
Cheers,
Adam
Reply
12/09/2013 at 08:27 AM

---
**内容**: dba said...
Anyway, I found

as helpful, since my Tab only activated when this was set.
BR,
Daniel
Reply
12/09/2013 at 07:29 AM

---
**内容**: dba said in reply to dba...
ok, missed the line of interest (because of malformed tags)
< Rule Activate=True ... />
Reply
12/09/2013 at 10:37 AM

---
**内容**: dba said...
Glad to share useful info :-)
BR,
Daniel
Reply
12/09/2013 at 10:34 AM

---
**内容**: Lavie526 said...
Hi,
I am using AutoCAD Architure, and develop an plugin basing on ACD, is it possible to place the xaml and dll with all the our plugin dlls under the "%appdata%/Autodesk/ApplicationPlugins/...", I have tried, seems not works.
Is there anything wrong?
thanks
Lavie
Reply
05/08/2014 at 03:35 AM

---
