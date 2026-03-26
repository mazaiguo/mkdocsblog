---
title: "Adding Icon Next To Custom Command"
date: 2016-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Plugin
description: "The motivation behind bringing this blog is a query from a Forum user."
author: Autodesk
---
# Adding Icon Next To Custom Command

发布日期: 2016-03-01

原始链接: https://adndevblog.typepad.com/autocad/2016/03/adding-icon-next-to-custom-command.html

## 文章内容

By Madhukar Moogala
The motivation behind bringing this blog is a query from a Forum user.
We can add any desired Icon next to our custom command.
First, load our custom command to AutoCAD domain.
Next create a CUI ribbon command button.
Create ribbon button macro with necessary image files and other data, image file that we wish to see across our custom command.
Associate macro with custom command.
When association is made between custom command and CUI ribbon macro, application can retrieve image data from command macro and displayed across command in command line or editor.
Image:
Or from Command Line:
Source code sample:
I created a sample cuix which associated macro with custom command.
To play around, configure following code into your enviroment,compile and run CreatTestCuix and load generated .cuix file to AutoCAD using CUILOAD.
See the magic
namespace IconToCustomCommand
    {
    /*Helper Methods*/
    public static class CustomizationExtensions
        {
        public static RibbonTabSource AddNewTab(
        this CustomizationSection instance,
        string name,
        string text = null)
            {
            if (text == null)
                text = name;
              var ribbonRoot = instance.MenuGroup.RibbonRoot;
            var id = "tab" + name;
            var ribbonTabSource = new RibbonTabSource(ribbonRoot);
              ribbonTabSource.Name = name;
            ribbonTabSource.Text = text;
            ribbonTabSource.Id = id;
            ribbonTabSource.ElementID = id;
              ribbonRoot.RibbonTabSources.Add(ribbonTabSource);
              return ribbonTabSource;
            }
          public static RibbonPanelSource AddNewPanel(
        this RibbonTabSource instance,
        string name,
        string text = null)
            {
            if (text == null)
                text = name;
              var ribbonRoot = instance.CustomizationSection.MenuGroup.RibbonRoot;
            var panels = ribbonRoot.RibbonPanelSources;
            var id = "pnl" + name;
            var ribbonPanelSource = new RibbonPanelSource(ribbonRoot);
              ribbonPanelSource.Name = name;
            ribbonPanelSource.Text = text;
            ribbonPanelSource.Id = id;
            ribbonPanelSource.ElementID = id;
              panels.Add(ribbonPanelSource);
              var ribbonPanelSourceReference = new RibbonPanelSourceReference(instance);
              ribbonPanelSourceReference.PanelId = ribbonPanelSource.ElementID;
              instance.Items.Add(ribbonPanelSourceReference);
              return ribbonPanelSource;
            }
          public static RibbonRow AddNewRibbonRow(this RibbonPanelSource instance)
            {
            var row = new RibbonRow(instance);
              instance.Items.Add(row);
              return row;
            }
          public static RibbonRow AddNewRibbonRow(this RibbonRowPanel instance)
            {
            var row = new RibbonRow(instance);
              instance.Items.Add(row);
              return row;
            }
          public static RibbonRowPanel AddNewPanel(this RibbonRow instance)
            {
            var row = new RibbonRowPanel(instance);
              instance.Items.Add(row);
              return row;
            }
          public static RibbonCommandButton AddNewButton(
        this RibbonRow instance,
        string text,
        string commandFriendlyName,
        string command,
        string commandDescription,
        string smallImagePath,
        string largeImagePath,
        RibbonButtonStyle style)
            {
              var customizationSection = instance.CustomizationSection;
            var macroGroups = customizationSection.MenuGroup.MacroGroups;
              MacroGroup macroGroup;
              if (macroGroups.Count == 0)
                macroGroup = new MacroGroup("MacroGroup", customizationSection.MenuGroup);
            else
                macroGroup = macroGroups[0];
              var button = new RibbonCommandButton(instance);
            button.Text = text;
              var commandMacro = "^C^C_" + command;
            var commandId = "ID_" + command;
            var buttonId = "btn" + command;
            var labelId = "lbl" + command;
              var menuMacro = macroGroup.CreateMenuMacro(commandFriendlyName,
            commandMacro,
            commandId,
            commandDescription,
            MacroType.Any,
            smallImagePath,
            largeImagePath,
            labelId);
            var macro = menuMacro.macro;
            /*Associate custom command to ribbonbutton macro*/
            macro.CLICommand = command;
              button.MacroID = menuMacro.ElementID;
            button.ButtonStyle = style;
            instance.Items.Add(button);
              return button;
            }
                }
    public class CreateTestCuix
        {
        [CommandMethod("CreateTestCuix1")]
        public static void CreateTestCuix1()
            {
            var editor = Application.DocumentManager.MdiActiveDocument.Editor;
              try
                {
                var debugFolder = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                var customizationSection = new CustomizationSection();
                var menuGroup = customizationSection.MenuGroup;
                var tab = customizationSection.AddNewTab("CuiTestTab");
                var panel = tab.AddNewPanel("Panel");
                var row = panel.AddNewRibbonRow();
                  menuGroup.Name = "CuiTest1";
                  row.AddNewButton(
                "Smile",
                "Smile",
                "KeepSmiling",
                "How to add BMP icon to Custom Command",
                debugFolder + "\\smile_16.bmp",
                debugFolder + "\\smile_32.bmp",
                RibbonButtonStyle.LargeWithText);
                    var fileName = Path.Combine(debugFolder, "CuiTest1.cuix");
                  File.Delete(fileName);
                  customizationSection.SaveAs(fileName);
                }
            catch (System.Exception ex)
                {
                editor.WriteMessage(Environment.NewLine + ex.Message);
                }
            }
        [CommandMethod("KeepSmiling")]
        public void KeepSmiling()
            {
            Application.ShowAlertDialog("KeepSmiling :D");
            }
          }
    }
Sample Transparent Images:
Project Source

## 评论

**内容**: Pierre de la Verre said...
Hi Madhukar
for the old-school Lisp-guys it would be fine if you would upload the mentioned sample Cuix.
Thanks ;)
Reply
03/29/2016 at 12:21 PM

---
**内容**: Madhukar Moogala said in reply to Pierre de la Verre...
Hi Pierre,
Thanks for stopping by at my post :)
I have update the blog with source, you can find .CUIX in debug folder when download and unzip.
Reply
03/30/2016 at 01:18 AM

---
**内容**: Pierre de la Verre said in reply to Pierre de la Verre...
Thanks - I have it. :-)
Reply
03/30/2016 at 02:09 AM

---
**内容**: Pierre de la Verre said...
BTW: For the posting above (the first in this thread) I tried to use the following content, but the "Preview" was closed automatically after half a second and this edit field was empty again.
Now it seem to be OK with the Preview ... ???
-----
Hi Madhukar
for the old-school Lisp-guys it would be fine if you would upload the mentioned sample Cuix.
Thanks ;) http://adndevblog.typepad.com/.a/6a0167607c2431970b01b7c82adbdd970b-pi
Reply
03/29/2016 at 12:25 PM

---
**内容**: Mark Dark said...
very interesting technology
Reply
09/12/2023 at 02:34 AM

---
