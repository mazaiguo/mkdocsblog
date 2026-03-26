---
title: "Differences between AutoCAD 2013 and AutoCAD OEM 2013"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - OEM
description: "Differences in Features and Utilities"
author: Autodesk
---
# Differences between AutoCAD 2013 and AutoCAD OEM 2013

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/differences-between-autocad-2013-and-autocad-oem-2013.html

## 文章内容

by Fenton Webb
Differences in Features and Utilities
AutoCAD OEM does not support the following features:
Autodesk Exchange Apps
InfoCenter
Welcome Screen
Customization and Drawing Sync
AutoCAD WS
Content Explorer
Inventor Fusion
Model Documentation
Batch Plotting utility
VBA for 64-bit version
Express Tools
Differences in Commands and System Variables
Most AutoCAD commands and system variables are available for use in your product, including the ETRANSMIT, RENDER, and DBCONNECT commands (see the bottom of this post for a full listing). You must bind any ObjectARX, AutoLISP ® , and .NET applications that are used by your AutoCAD OEM product, including those that define commands.
The interface to system variables and the ability to change them depends on what you want to “publish” to the end user. Some system variables are published by default, based on their inclusion in various dialog boxes. However, as the AutoCAD OEM product vendor, you determine whether to publish the commands that call the dialog boxes.
For example, by default the DIMSTYLE command provides a user interface for changing dimension variables. If your product doesn't support dimensioning, or if you wish to set all dimension variables internally in your product, you should not publish the DIMSTYLE command.
Any system variables that you want to be available to end users from the menu, toolbar, or keyboard must be listed as allowed commands.
Command Difference in AutoCAD OEM 2013
The following AutoCAD OEM 2013 command is different from the AutoCAD 2013 command:
OPTIONS
This configuration dialog box is simplified for AutoCAD OEM. A major difference is that the Profiles tab is not provided.
The following AutoCAD OEM 2013 system variable is different from the corresponding AutoCAD 2013 system variable:
REPORTERROR
If set to 1, an error report can be generated, but it is not sent to Autodesk. If set to 0, AutoCAD OEM defers to the operating system to take action during an unhandled exception.
ACADLSPASDOC
It is listed in the MakeWizard and needs to be enabled to work. Its value is not persisted in the registry. It controls whether the aoem.lsp file is loaded into every drawing or just the first drawing opened in a session.
An AutoCAD OEM product can use most of the standard AutoCAD system variables; however, the following system variables are not supported:
ACADVER
ACADPREFIX
LOGINNAME
MENUCNTL
POPUPS
SCREENBOXES
SCREENMODE
Use (getenv "Support") from the Visual LISP ® console to access the same information provided by ACADPREFIX. The argument to (getenv) is case sensitive. For more information about (getenv), see the AutoLISP Reference.
Differences in the User Interfaces
AutoCAD OEM Command Line
The AutoCAD OEM command line supports input from keyboard, script files, pasted text, and even the Windows SendMessage() API. Like the AutoCAD command line, the AutoCAD OEM command line also supports transparent commands that interrupt the command currently running. However, an AutoCAD OEM command or system variable works in an AutoCAD OEM stamped product only if the product is configured to support it.
Because the AutoCAD OEM Make Wizard allows you to toggle support for individual commands, you can present to the user only those commands required by your product, and you can provide the documentation needed for only those commands.
You can customize the command line interface to suit your product's needs. For example, to simplify navigation for the user, you may want to present only three of the eleven different options of the ZOOM command. You do this with the Redefine option in the AutoCAD OEM Make Wizard.
To implement this ZOOM command redefinition, you could include the following example:
(command "UNDEFINE" "ZOOM")
(defun C:ZOOM ( / zinput )
   (initget 1 "All Extents Previous")
   (setq zinput (getkword "\nZoom to (All/Extents/Previous): "))
   (command ".ZOOM" zinput)
   (princ)
)  
For the ZOOM command, you would specify Redefine on the AutoCAD OEM Commands page of the AutoCAD OEM Make Wizard. When the user invokes the ZOOM command in your product, your redefined command is called.
You can also turn off the command line in your product. If you do so, users will be able to invoke commands only from the menu or a toolbar.
Text Window in AutoCAD OEM
AutoCAD OEM lets you disable the AutoCAD text window.
AutoCAD OEM Menus
With AutoCAD OEM, you can have multiple menus. AutoCAD OEM uses all AutoCAD menu sections except the Screen menu section. AutoCAD OEM also does not support LISP in menus. The only other limitations are those imposed by command and system variable changes for AutoCAD OEM (see Differences in Commands and System Variables above). The AutoCAD Customization Guide and Command Reference provide information about menu customization. With AutoCAD OEM you can also enable menu customization for the end user by supporting the CUI command.
In a stamped AutoCAD OEM product, if you support the CUI command, the user can load an alternate menu. You can also support the CUILOAD and CUIUNLOAD commands so that users can manage partial menus.
AutoCAD OEM Toolbars
You can provide the CUI and QuickCUI commands so that users can customize toolbars. They launch the Customize User Interface dialog box, with which users can create, modify, or delete toolbars. When the CUI command is supported, end users can create new buttons, change button bitmaps, or modify the command that a button calls.
AutoCAD OEM maintains toolbar state identically to AutoCAD. Changes to toolbars are written to the customization file, and the location and status of the toolbars are saved in the Windows system registry. Partial menu load information is also saved in the registry. AutoCAD OEM automatically reloads all visible toolbars.
Differences in the Help Files
AutoCAD OEM supports only HTMLHelp. AutoLISP applications can use the help function to call the Help file. If an end user presses F1, the <program name>.chm file is called.
ObjectARX applications can use the acedHelp() function to call a Help file. For more information, see the ObjectARX Reference.
To ensure that the appropriate Help topic is called when the user opens Help using the F1 key, the Help menu, the command line, or an AutoCAD OEM dialog box, you must use the proper topic ID for that topic in the Help file.
See this blog entry for information on how to create Help for OEM
Differences in ObjectARX Interaction
The following sections explain differences in the behavior of ObjectARX applications in the AutoCAD OEM development environment.
Automatic Loading of ObjectARX Applications
You can use the following methods to load an ObjectARX application into your AutoCAD OEM product:
ARX command with the Load option
<program name>.rx file containing a list of applications to load at startup
Demand loading by registry settings
aoem.lsp file
Launch your product from a Windows command prompt using the /ld startup switch
Required option in the AutoCAD OEM Make Wizard
The demand loading feature in AutoCAD OEM automatically attempts to load a non-memory-resident ObjectARX application when it is needed. Implement demand loading for applications that are not used in every session. For more information about demand loading, see “Demand Loading” in the ObjectARX Developer's Guide.
To load an ObjectARX application when starting your AutoCAD OEM product, you can use demand loading, or you can add the application to the <program name>doc.lsp file or to a <program name>.rx file. Sample autoloading code is provided in the aoemdoc.lsp file for you to use or to edit to suit your requirements. You may add new commands or delete the existing commands included in the example. The (autoload) and (autoxload) functions are defined in the aoemdoc.lsp file. See “Using AutoLISP Applications” in the AutoCAD Customization Guide.
Warning You must place startup commands within the S::STARTUP() section of <program name>doc.lsp. The S::STARTUP() function is used by AutoCAD OEM to store the functions that must be run before users can do anything but after the AutoCAD OEM engine is ready to accept commands. You cannot have a command in <program name>doc.lsp that is executed before the S::STARTUP() function is executed, because AutoCAD OEM will fail.
If you already have a startup AutoLISP file, you can create a <program name>doc.lsp file that has only an S::STARTUP function that loads the startup file. This way, you do not have to make substantial changes to the startup file.
Disabling of Drawing Save
AutoCAD OEM provides the following ObjectARX function:
void
acedDisableDbMod(     Adesk::Boolean disable,     Adesk::Boolean clearDBMOD);  
This function is available only in AutoCAD OEM. It lets you control the use of the DBMOD system variable, which indicates whether the drawing has been changed. You can use this function to reset DBMOD and to force the AutoCAD OEM engine to disregard DBMOD.
The first argument to this function is a Boolean, indicating whether the AutoCAD OEM engine will check the state of the DBMOD system variable. Setting it to Adesk::kFalse enables checking, and setting it to Adesk::kTrue disables checking.
The second argument to this function resets the value of DBMOD. Setting it to Adesk::kTrue resets DBMOD to zero, indicating that the drawing has not been modified. Setting it to Adesk::kFalse leaves DBMOD unchanged.
The primary use of this function is to keep the AutoCAD OEM engine from prompting end users to save drawings. You might want to do this when the drawing information is not important, such as in a demonstration program, or when the information has been saved in a format other than the standard AutoCAD drawing format. If the AutoCAD OEM product is a demonstration program and you are disabling the save features, you can disable DBMOD checking by calling acedDisableDbMod(Adesk::kTrue, Adesk::kFalse).
If you are implementing custom save functions, check the DBMOD variable to see if there is information that needs to be saved, and save it in your desired format. You can then call acedDisableDbMod(Adesk::kFalse, Adesk::kTrue), which specifies to the AutoCAD OEM engine that all the necessary information has been saved.
Note: To use the acedDisableDbMod() function, you must declare it in your source code because the function does not appear in any of the AutoCAD OEM header files. You can supply any default values for the arguments, but the following declaration is recommended:
void acedDisableDbMod(Adesk::Boolean disable, Adesk::Boolean clearDBMOD = Adesk::kTrue);
Differences in Visual LISP Interaction
AutoCAD OEM developers can use the Visual LISP IDE to develop AutoLISP applications that can be used within a stamped pure AutoCAD OEM product (aoem.exe). AutoCAD OEM developers have access to the full feature set of Visual LISP, with a few exceptions noted. Some restrictions have been placed on the use of AutoLISP applications by end users of AutoCAD OEM products.
Visual LISP for Developers
The Visual LISP IDE is available to AutoCAD OEM developers, with some exceptions.
Specifically, although bound FAS files are supported in AutoCAD OEM, you cannot create or use VLX files (Visual LISP packed applications). Moreover, you cannot use Visual LISP functions related to ActiveX ® , including vl‑load-com, vlax-* and vlr-* functions.
AutoLISP for Stamped Products
The following restrictions on the use of AutoLISP applications apply to all stamped AutoCAD OEM products:
Stamped AutoCAD OEM products allow loading of only compiled AutoLISP files that are bound to the specific AutoCAD OEM product. FAS and FSL files can be loaded, but VLX files cannot.
End users cannot enter AutoLISP expressions using the keyboard, menu, or script files.
Stamped AutoCAD OEM products cannot access the debug-enabled, run-time expression evaluator.
The AutoCAD OEM Make Wizard can be configured to bind an AutoLISP file so it runs only with the specified AutoCAD OEM product. You can also use the bindlisp program for this purpose.
Differences in Command Line Switches
AutoCAD OEM supports the following command line switches for startup:
Command line switches supported by AutoCAD OEM
/c - Specifies the location in which AutoCAD OEM searches for the startup configuration file
/t - Creates a new drawing based on the specified template file (This switch is not supported when the Initial Drawing Mode feature is turned off.)
/nologo  - Starts AutoCAD OEM without displaying the splash screen
/v - Designates a particular view of the drawing for display at startup
/b - Starts AutoCAD OEM with a script file when the command line is enabled
/s - Starts AutoCAD OEM with a specific support directory path specified
/set - Opens AutoCAD OEM with the specified sheet set
/nossm - Suppresses the Sheet Set dialog box from being displayed at AutoCAD OEM startup when no sheet set is specified
/ld - Loads a specified ObjectARX or ObjectDBX application
/pl - Performs a background plot of the specified DSD file
Normally, AutoCAD OEM places the configuration file (<program name><release>.cfg) in the executable directory. You can use the /c switch to specify a different location for the file. For example, from Windows Explorer, you can create a new program shortcut and enter the following command:
c:\Program Files\Autodesk\AutoCAD OEM 2013\aoem /c c:\tmp
This causes the configuration file to be placed in the c:\tmp directory. The new configuration directory must exist and be writable.
The /pl switch is the command line background plot switch. It accepts the name of a DSD (Drawing Set Descriptions) file, and publishes the specified file without displaying the AutoCAD OEM application window. You use the following format to specify the file name:
<path>\<drawing set descriptions file>.DSD
The following switches are not supported in AutoCAD OEM:
/r
/p
For more information about command line switches, see the AutoCAD User's Guide.
Difference Regarding Personalization
AutoCAD OEM does not support personalization and serialization of end-user program executables.
AutoCAD OEM Native Commands and System Variables
This section describes commands and system variables that are unique to AutoCAD OEM. These commands and system variables do not exist in AutoCAD.
Commands Specific to AutoCAD OEM
The following commands are specific to AutoCAD OEM:
..SYSSTATUS
Writes status and system information to a <program name>.slg file. This is useful for product support and troubleshooting. (The two dots at the beginning of ..SYSSTATUS are part of the command name.) You can add this command to your product by first adding any ObjectARX module to your product, and then, on the Your Module Settings page of the AutoCAD OEM Make Wizard, adding “.SYSSTATUS” to the ObjectARX module. Note that in this case, there is just one preceding period.
LISTCOMMANDS
Lists commands you have enabled in your product. Commands that are the same for global and local are shown as global, and prefixed with an underscore. (For more information about global and local commands, see AutoCAD OEM Commands Page .) Built-in command names are described as “internal,” and non-built-in commands as “external.”Below is an example of such an output:
Command: listcommands
_+VIEW external
_+OPTIONS internal
_+DSETTINGS external
_+CUSTOMIZE internal
_+PUBLISH external
_+VPORTS internal
_+UCSMAN internal
_-HYPERLINK external
_-PUBLISH external
_-SHADERMODE external
_-RENDER external
_-TEXT internal
PKFSTGROUP (PICKFIRST GROUP)
Provides an alternate means of accessing the group feature. The group feature for AutoCAD OEM comes in two versions. The first is identical to the GROUP command in AutoCAD, where a dialog box is displayed and a user can select objects. The second version of the group feature allows end users to make a pickfirst selection set, and then issue the PKFSTGROUP command.
System Variables Specific to AutoCAD OEM
The following system variables are specific to AutoCAD OEM:
BANNER
Read-only system variable that returns the text of the developer-specified banner. Each line is separated by a newline character (\n), and multiple white-space characters are reduced to one space. This string is truncated at 500 -characters.
Using BANNER, you can retrieve the banner lines from the <program name>res2.dll file, where <program name> represents the first four letters of your AutoCAD OEM program's name.
CLIPBOARD
Read-only system variable that indicates the status of the Windows® Clipboard. Returns the sum of one or more of the following bit values:
0 Nothing available
1 ASCII text available
4 AutoCAD format data available
5 Windows metafile data available
You can use the CLIPBOARD system variable to enable or disable Clipboard commands on your menu. For example, the following DIESEL expression disables the Paste Special menu item when the Clipboard is empty:
[$(If,$(getvar, clipboard),,~)/Paste &Special...]
^C^C_pastespec
For more information about DIESEL string functions and customizing menus, see the AutoCAD Customization Guide.
EXEDIR
Executable directory.
PROGRAM
Read-only hidden system variable that returns the program name.
PRODUCT
Read-only hidden system variable that returns the product name.
VERSION
Read-only system variable that returns the version of the AutoCAD OEM engine. Replaces ACADVER.
Listing of available commands for AutoCAD OEM 2013
Full listing of available commands for AutoCAD OEM 2013 - A to D
Full listing of available commands for AutoCAD OEM 2013 - E to L
Full listing of available commands for AutoCAD OEM 2013 - M to S
Full listing of available commands for AutoCAD OEM 2013 - T to Z
For further information regarding Autodesk OEM products
Please contact TechSoft3d

## 评论

**内容**: Loic Jourdan said...
Hi Fenton,
What about viewbase command?
it seems that this command wasn't available in AcadOEM 2012 make wizard although it exist in Acad full, has it been activated in oem 2013? (as well as new viewsection command)
Thank you
Loic Jourdan
Reply
12/18/2012 at 11:50 PM

---
**内容**: Loic Jourdan said in reply to Loic Jourdan...
Me again, I forgot a point: if I remember correctly, the "start" command was available in acad but not in acad oem.
Loic
Reply
12/19/2012 at 12:07 AM

---
**内容**: Fenton Webb said...
Hey Loic!
please see the updated blog entry, I have listed all of the commands in OEM 2013 for you.
Reply
12/19/2012 at 02:00 PM

---
**内容**: Alexander Rivlis said...
Hi, Fenton!
I've found a typo: not ACADLSPACDOC but ACADLSPASDOC
Reply
01/17/2013 at 05:33 AM

---
**内容**: Fenton Webb said...
Thanks Alexander, fixed.
Reply
01/17/2013 at 09:03 AM

---
**内容**: Jeroen said...
Have there been any changes in v2014, or is it pretty much the same?
Reply
05/14/2013 at 07:18 AM

---
**内容**: Fenton Webb said...
Hey Jeroen
I've just scanned the 2014 OEM Developer Guide and it seems exactly the same as 2013
Reply
05/14/2013 at 10:09 AM

---
**内容**: Craig said...
Hello Fenton,
I need to work through the command lists to identify which to remove etc from our OEM product. I'm wondering if the commands are grouped in some way so I could quickly remove a set of commands?
Any thoughts?
Cheers
Reply
08/21/2013 at 02:08 AM

---
