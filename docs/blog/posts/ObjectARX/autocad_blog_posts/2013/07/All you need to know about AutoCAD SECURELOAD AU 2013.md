---
title: "All you need to know about AutoCAD SECURELOAD AU 2013"
date: 2013-07-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "I’m presenting a class on the new security features inside of AutoCAD 2014 at this years AU – classes DV3456 (Lecture) and DV3459-R (Round table af..."
author: Autodesk
---
# All you need to know about AutoCAD SECURELOAD AU 2013

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/all-you-need-to-know-about-autocad-secureload-au.html

## 文章内容

by Fenton Webb
I’m presenting a class on the new security features inside of AutoCAD 2014 at this years AU – classes DV3456 (Lecture) and DV3459-R (Round table after-lecture discussion). I thought you might like to see my handout document in advance, let me know if you don’t follow anything and I’ll try to explain/update the document for you…
The Original Security Problem
Back in the AutoCAD 2012 time frame a problem AutoCAD arose with people exploiting the LISP auto loading mechanism used by acad.lsp acaddoc.lsp/fas/vlx files to infect user’s machines with viruses. We published a Technical Solution to address a variation of the virus  http://usa.autodesk.com/getdoc/id=TS13717811
At that time, AutoCAD would autoload the first acad/acaddoc/acad20xx/acad20xxdoc. lsp/fas/vlx or acad.dvb file it encountered in its AutoCAD Support File Search path. All the AutoCAD viruses out there were exploiting this single feature.  We decided to provide an option to disable this feature since most, if not all, users use only a single acad.lsp, acaddoc.lsp or acad.dvb.
Most of these viruses used to get to a user by slipping the lisp files into a zip file containing legitimate drawings. When a user unzips the zip file and double clicks on a drawing file to open it, the lisp files get loaded and infect the machine. 
There are 3 different groups of these types of user created startup files:
1.    acad.lsp/fas/vlx
2.    acaddoc.lsp/fas/vlx
3.    acad.dvb
FAS & VLX filetypes are compiled LSP files.  DVB is a Visual Basic for Applications macro file.
In addition, we sometimes used to ship acad20xx.lsp and acad20xxdoc.lsp files (xx represents the release year). These files are “reserved” for AutoCAD use only.
Only 1 of each group is loaded. 
If acad.lsp, acad.fas and acad.vlx are all present in the same directory, only acad.vlx is loaded and acad.fas and acad.lsp is ignored.
If all 7 files are present, only acad.vlx, acaddoc.vlx and acad.dvb are loaded.  But it depends on which directory these files are found.  Each of these files are loaded from the first place AutoCAD finds them as it works through its search path.
The search path isn’t just what is defined in the Options Files tab; it also includes the current folder (usually the start-in folder defined in the program shortcut) and the current drawing’s folder.
The current folder is searched first, then the drawing folder, then the rest of the search path. So if acad.lsp is found first, it will get loaded even if an acad.fas/vlx exists.  (At any time only 1 of the files acad.lsp, acad.vlx or acad.fas are loaded, even when the files are located in different directories. If AutoCAD finds and loads one of these files, it stops looking for the other 2).
The Search order for these files is:
1.    Acad.VLX
2.    Acad.FAS
3.    Acad.LSP
But if all 3 (or 2) of the files are present in a directory, AutoCAD first checks if the .lsp file is newer than the .VLX or the .FAS file. If it is, then AutoCAD loads the .LSP file.
Acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx or acad.dvb are not shipped with AutoCAD, and are created by users.
The reserved acad20xx.lsp and acad20xxdoc.lsp files were installed in the <installdir>\support folder.  (As of AutoCAD 2013, the acad20xxdoc.lsp file is installed into a localized sub-folder such as en-us). acad20xx.lsp and acad20xxdoc.lsp were supposed to be for AutoCAD internal use only, so users should not have been creating/editing them. We clearly documented this in the Help documentation. But we were treating these files like acad.lsp and acaddoc.lsp (i.e. the first file found in the search path is autoloaded).
One of our CAD bloggers documents the order in which these files are loaded- Section B in http://www.blog.cadnauseam.com/2008/09/01/what-is-loaded-at-autocad-startup-and-when/ If all these files are found, AutoCAD will load all of them. (The only exception is when all 3 versions (i.e acad.lsp, acad.vlx and acad.fas are found in a directory, only acad.lsp is loaded – the other 2 are ignored).
References
How to detect and remove the Acad.vlx virus:  http://usa.autodesk.com/adsk/servlet/ps/dl/item?siteID=123112&id=13717811&linkID=9240617
Comparing the acad*.lsp files:  http://usa.autodesk.com/adsk/servlet/ps/dl/item?siteID=123112&id=2897258&linkID=9240617
What is loaded at AutoCAD startup, and when?:  http://www.blog.cadnauseam.com/2008/09/01/what-is-loaded-at-autocad-startup-and-when/
Comparing the acad*.lsp files:  http://usa.autodesk.com/adsk/servlet/ps/dl/item?siteID=123112&id=2897258&linkID=9240617
  Additional Information from the Help docs
Help->Customization Guide-> The ACAD.LSP File
You can create an acad.lsp file if you regularly use specific AutoLISP routines. When you start AutoCAD, it searches the support file search path for an acad.lsp file. If an acad.lsp file is found, it is loaded into memory.
Warning: Do not modify the reserved acad2012.lsp file. Autodesk provides the acad2012.lsp file, which contains AutoLISP defined functions that are required by AutoCAD. This file is loaded into memory immediately before the acad.lsp file is loaded.
Help->Customization Guide-> The ACADDOC.LSP File
Most users will have a single acaddoc.lsp file for all document-based AutoLISP routines. AutoCAD searches for anacaddoc.lsp file in the order defined by the library path; therefore, with this feature, you can have a different acaddoc.lspfile in each drawing directory, which would load specific AutoLISP routines for certain types of drawings or jobs.
Warning: Do not modify the reserved acad2012doc.lsp file. Autodesk provides the acad2012doc.lsp file, which contains AutoLISP-defined functions that are required by AutoCAD. This file is loaded into memory immediately before the acaddoc.lsp file is loaded.
Help->Customization Guide-> Automatically Load and Execute VBA Projects
The acad.dvb file is useful if you want to load a specific VBA project that contains macros you want each time you start AutoCAD. Each time you start a new AutoCAD drawing session, AutoCAD searches for the acad.dvb file and loads it.
  The Solution – AutoCAD 2012 sp1
The solution includes updates to 3 areas:
New command line startup switch
New system variables
Change load rules for acad20xx.lsp and acad20xxdoc.lsp
  New Command Line Startup Switch
Introduce a new command line switch called “/nolisp”.
Starting AutoCAD with this switch disables Lisp in AutoCAD (includes LSP, FAS, VLX). This breaks some menu items, express tools, etc. but this is meant for emergency use when a system is infected and the user is afraid of launching AutoCAD. 
NOTE: This startup switch also provides the user the ability to change the AUTOLOAD & AUTOLOADPATH settings. Also, just like other start up switches, this state is only for the current session, and the state is not saved between sessions.
(New switch matches naming convention of some existing similar switches such as /nologo, /nohardware, /nossm.)
When the “nolisp” command line switch is used, it sets the new LISPENABLED system variable to 0.
New System Variables
We added a new read-only sysvar (LISPENABLED) which corresponds to the new command line switch.
  Item
Description
Name
LISPENABLED
Description
Controls whether LISP is enabled for the AutoCAD session (includes LSP, FAS, VLX)
Data Type
Integer
Values
0 –LISP is disabled
1 –LISP is enabled
Initial Value
1
Stored in
Not Saved- Current Session only
Accessed from
CLI, SETVAR command, startup switch “/nolisp”
  We have also added 2 new read/write sysvars (AUTOLOAD, AUTOLOADPATH) which enables the user to determine whether or not AutoCAD automatically loads acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files, and where it loads them from.
Users can still load other LISP files.  AutoCAD 2012 sp1 still loads the reserved acad20xx.lsp and acad20xxdoc.lsp files (from the Support directory- see ‘Change load rules’ section below).
This setting only affects the auto-loading of user-defined startup files (acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb).
Item
Description
Name
AUTOLOAD
Description
Controls whether or not AutoCAD autoloads LSP, FAS, VLX, DVB files
Data Type
Integer
Values
0  (Off)– Does not autoload acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files.
1  (On) – Autoloads acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files.
Initial Value
1
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command
  Item
Description
Name
AUTOLOADPATH
Description
Controls where AutoCAD autoloads acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files from
Data Type
Text
Values
 “<folder path>” or multiple folder paths separated by commas.  AutoCAD only loads acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files it finds in the specified folders (and no other locations including the current drawing location).
“” (empty)  same as legacy behavior.  AutoCAD loads acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx, acad.dvb files it finds in the Support File Search path (including the current drawing location.
Initial Value
“” empty
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command
  The AUTOLOADPATH system variable is saved in the same Registry location as the AutoCAD Support File Search Path (ACAD):
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Profiles\<profilename>\General
  Options dialog
The existing “Load acad.lsp with every drawing” in the System tab in Options dialog is disabled when AUTOLOAD disables this feature [AUTOLOAD=0). Also disabled when LISPENABLED=0.
The checked/unchecked value is still determined by the existing ACADLSPASDOC system variable.
Changed load rules for acad20xx.lsp and acad20xxdoc.lsp
Before, we treated acad20xx.lsp and acad20xxdoc.lsp similar to acad.lsp and acaddoc.lsp (i.e. the first file found in the search path is autoloaded). This is no longer the case, we now only load the files found in the Install Support directory.  For example: C:\Program Files\Autodesk\AutoCAD 2013\Support
These files are meant for internal AutoCAD use and the users should not be creating them on their own.
AutoCAD verticals
This functionality behaves exactly the same as in AutoCAD.
AutoCAD for Mac
This functionality behaves nearly identical to AutoCAD for Windows. 
NOTE: AutoCAD for Mac supports LSP & FAS files, but not VLX files.
AutoCAD LT/AutoCAD OEM
This functionality and related system variables are not be available in LT.  LT doesn’t have this problem because Lisp files cannot be run in AutoCAD LT.
  The Solution – AutoCAD 2014
Basically, the AutoCAD 2012 SP1 solution was incomplete (it was only limited to Lisp), therefore we needed 2014 Security changes to provide a much more comprehensive barrier to all executable code files that could potentially be malicious.
The solution includes updates to the following areas:
Expanding filetypes that are detected by SECURELOAD
Added new settings to Options dialog which correspond to the AUTOLOAD & AUTOLOADPATH sysvars added via the AutoCAD 2012 sp1(now called SECURELOAD & TRUSTEDPATHS)
Split AUTOLOADPATH into 2 sysvars (TRUSTEDPATHS, TRUSTEDDOMAINS)
Implicitly “trust” digitally signed executable files (DLL, EXE, ARX, DBX, etc.)
Define trusted install location for some folders & files
“/safemode” startup switch, SAFEMODE & SAFEMODEAPPS system variables
New warning dialog to warn users when executable files are detected that are not included in TRUSTEDPATHS & TRUSTEDDOMAINS
Change Loading for CUIx/MNL files
Add warning message to warn users when writable locations are specified in TRUSTEDPATHS
New LISP function (findtrustedfile)  as opposed to (findfile)
Add new settings to Deployment Wizard
All Filetypes detected by SECURELOAD
The AUTOLOAD settings introduced in the 2012 sp1 have been updated in 2014 and also expands the type of files we automatically load from the narrow list of user-defined startup files (acad.lsp/fas/vlx, acaddoc.lsp/fas/vlx & acad.dvb) that we targeted in the 2012 sp1 to all ARX, Lisp, .NET assemblies, VBA, Javascript & DLL files.
In the AutoCAD 2012 sp1, the AUTOLOAD settings were 0 (Off) and 1 (On).  For AutoCAD 2014, the name of the sysvar changes to SECURELOAD and the values are different (see below).  The AUTOLOAD values are changed from the 2012 SP1, because the “/safemode” startup switch makes the AUTOLOAD =0 (Disabled) setting unnecessary.
If SECURELOAD =1, AutoCAD prompts the user if it tries to load any executable code files (if not located in the Trusted locations and not digitally signed):  The list of executable file types includes, but is not limited to:
ARX/DBX/CRX
LSP/FAS/VLX/MNL
.NET assemblies
VBA macros, acad.rx, acVBA.arx, acad.dvb
Javascript
DLL
SCR files (located on network) 
For 2014, we now implicitly “trust” all digitally signed executable files (DLL, EXE, ARX, DBX, etc) - they do not need to be in one of the “Trusted Locations”. 
acad.rx isn’t an executable file, it’s a text-based manifest of references to .arx and .dbx files to be loaded. acad.rx files are just another place AutoCAD looks to find out what executable files it should load (along with the Registry, the Startup Suite, the Autoloader, etc.).
Item
Description
Name
SECURELOAD
Description
Controls whether or not AutoCAD autoloads executable files it finds in the regular search path (start-in folder, Drawing folder, Support File Search Path, Install folder)
Data Type
Integer
Values
0 –Load without warning (Legacy Behavior).
  1 –Load without warning if the file is also in TRUSTEDPATHS & TRUSTEDDOMAINS.  If not in TRUSTEDPATHS & TRUSTEDDOMAINS, display warning dialog before loading.   Applies to autoloading & manual loading.
  2 –Load without warning if the file is also in TRUSTEDPATHS & TRUSTEDDOMAINS.  If not in TRUSTEDPATHS & TRUSTEDDOMAINS, do not display warning dialog.   Applies to autoloading & manual loading. 
  If a file found is not trusted, the command line displays the same error message as selecting “Do Not Load” in the File Loading - Security Concern task dialog.
“File load canceled: <path\filename>"
Initial Value
1
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command
  Note:   SECURELOAD=0 restores the Legacy behavior. 
  TRUSTEDPATHS
The AUTOLOADPATH system variable introduced in AutoCAD 2012 SP1 has been renamed to TRUSTEDPATHS.
  We always recursively trust the acad.exe directory and the ApplicationPlugins folders (used by Exchange Apps).
Item
Description
Name
TRUSTEDPATHS
Description
Specifies the folders from where AutoCAD can load and execute files that contain code.
Used in conjunction with SECURELOAD= 1 or 2
Data Type
Text
Values
Multiple folders separated by semi-colons. 
Initial Value
“” (empty)
Note:  We always recursively trust the acad.exe directory and the two Application Plugins folders:
All Users:  C:\ProgramData\Autodesk\ApplicationPlugins
Roaming User:  C:\Users\<login>\AppData\Roaming\Autodesk\ApplicationPlugins
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command, Options dialog- Files tab
  Users can load a file from Trusted Locations (without it being on the regular search path), as long as they specify the full path (same as current behavior).  We only “search’ the regular search path, and make trust decisions based on “Trusted locations”. 
The location of the Express Tools folder does NOT need to be moved from Support File Search Path to TRUSTEDPATHS.
  The Exchange App Plug-ins do NOT need to be added to TRUSTEDPATHS.  They continue to write to the Support File Search Path, as they were in 2013.
  TRUSTEDDOMAINS
  This is a new system variable introduced in AutoCAD 2014 to handle the autoloading of Javascript files.
    Item
Description
Name
TRUSTEDDOMAINS
Description
Specifies the domain names or URLs from which AutoCAD can run JavaScript code.
Data Type
Text
Values
Multiple locations separated by semi-colons.
Initial Value
TBD by SWD
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command
  Users can specify multiple URLs for Javascript servers.
The URLs support wildcards.  eg:
*.autodesk.com/*                                // trust anything from Autodesk
*.autocadws.com/*                             // trust anything from AutoCAD WS
*.codeplex.com/site/MyProject/*        // trust anything from a subdomain
https://144.111.123.123/*                    // trust only https protocol from a specific IP address
  Options dialog changes
One new branch has been added to the Files tab in the Options dialog (“Trusted Locations”).  This corresponds to the TRUSTEDPATHS system variable. 
The dialog entry is changed from “Trusted File Search Path” to “Trusted Locations”, since we are no longer searching Trusted locations.
Note:  We are not adding the “Trusted Domain Locations” to the Options dialog (this is only for Deployment).
These paths are the designated “trusted sites” for executable code files.  Files in these locations are loaded without prompting (same as legacy behavior).  For that reason, it is recommended that only read-only folders are specified in TRUSTEDPATHS.  NOTE: A warning message is displayed if user tries to add a writable location.  See below.
Trusted Locations
Users can specify multiple paths. 
The tooltip for the new branch is:  Specifies the folders from where AutoCAD can load and execute files that contain code. The AutoCAD executable folder and its subfolders, and the plug-in applications folders are automatically trusted.
Error messages match the existing error messages in the Files tab for folder locations.  For example, if a non-existing folder is specified, an error message is displayed.
NOTE: We support syntax that indicates “trust” for subdirectories of a directory\path.  ‘\…’  (three dots) can be used to specify sub-folders.
Note:  We always recursively trust the acad.exe directory and the two Application Plugins folders (but they are not listed).
Options- Warning Message
If the user selects a writable location for “Trusted Locations”, AutoCAD 2014 presents a warning dialog message with these options...
Button
Description
Continue
Closes the task dialog and returns to the Options dialog.  The location specified is accepted in the “Trusted Locations”.    This is the default option if the user just presses Enter key.
Cancel, X button or ESC key
Closes the task dialog and returns to the Options dialog.  The location specified for “Trusted Locations” is removed, and cursor is left at blank field (same as clicking “Add” button).
  The System tab in Options dialog has also been modified in AutoCAD 2014.  
·         The existing “Load acad.lsp with every drawing” checkbox has been moved to a new sub-dialog, and changed from a single checkbox to a pair of radio buttons.
·         A new group box “Security” has been added with a new button “Executable File Settings”.  This button invokes the new Executable File Settings sub-dialog.
The new Executable File Settings dialog allows users to control the loading of executable code files.
There are three radio buttons that correspond to the SECURELOAD system variable.
The existing “Load acad.lsp with every drawing” (ACADLSPASDOC) is changed from a single checkbox to a pair of radio buttons.
The radio buttons for these 2 controls (SECURELOAD, ACADLSPASDOC) are disabled if SAFEMODE=1.
ID
Control
Type
Accel. key
Description
Enable/Disable
Initial Default
1
Executable File Settings
Title
N/A
  N/A
N/A
  Descriptive Text
Static Text
N/A
These settings restrict the locations from where executable files are loaded.  This helps protect against malicious code in executable files.
N/A
N/A
  Secure Loading
Group box
N/A
  N/A
N/A
  Choose the method to load executable files:
Static Text
N/A
  N/A
N/A
2
Load from all locations without displaying a warning
Radio button
A
Controls where executable code files are loaded from.
SECURELOAD = 0
Enabled.
Disabled if SAFEMODE=1
Unselected
3
Load from Trusted locations, display a warning for other locations
Radio button
W
Controls where executable code files are loaded from.
SECURELOAD = 1
When selected, this displays the File Loading- Security Concern warning dialog when AutoCAD detects and tries to load an executable code file outside of the Trusted locations (Trusted Locations & Trusted Domain Locations).
Enabled.
Disabled if SAFEMODE=1
Selected
4
Load from Trusted locations only
Radio button
T
Controls where executable code files are loaded from.SECURELOAD = 2
Enabled.
Disabled if SAFEMODE=1
Unselected
5
Tip
Static text
  Tip text:  Trusted locations are specified on the Files tab.
N/A
N/A
  Automatic Loading
Group box
N/A
  N/A
N/A
  Choose the method to load acad.lsp:
Static Text
N/A
  N/A
N/A
6
Load acad.lsp once at the start of the session
Radio button
S
Controls whether the acad.lsp file is loaded into every drawing or just the first drawing opened in a session (ACADLSPASDOC=0).
Replaces the “Load acad.lsp with every drawing” checkbox in AutoCAD 2012 (unchecked).
Enabled.
Disabled if SAFEMODE=1
Selected
7
Load acad.lsp when opening each drawing
Radio button
D
Controls whether the acad.lsp file is loaded into every drawing or just the first drawing opened in a session (ACADLSPASDOC=1).
Replaces the “Load acad.lsp with every drawing” checkbox in AutoCAD 2012 (checked).
Enabled.
Disabled if SAFEMODE=1
Unselected
8
OK
Button
  Accepts changes and closes the dialog.
Enabled
N/A
9
Cancel
Button
  Cancels any changes and closes the dialog.
Enabled
N/A
10
Help
Button
H
Opens Help window to the appropriate help topic.
Enabled
N/A
  The Settings in the Executable File Settings dialog are saved in the AutoCAD Named Profile, in the same Registry location as the AutoCAD Support File Search Path (ACAD), and where we added AUTOLOAD & AUTOLOADPATH in AutoCAD 2012 sp1.
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Profiles\<profilename>\General
Install Changes
The install location for the following files have changed or have been reevaluated:
CUIx & MNL files that were previously in the user’s roamable support folder:  %appdata%\Autodesk\AutoCAD 20xx - <lang>\R19.0\enu\Support
The MNL files have been moved to the localized Support folder of the Install Dir:  C:\Program Files\Autodesk\AutoCAD 20xx\Support\en-us.
The CUIx files after evaluation are staying in the user’s roamable support folder because they need to be easily edited.
“/safemode” startup switch
The /nolisp startup switch introduced in AutoCAD 2012 sp1 has been renamed to ‘/safemode’ and now includes all executable code files. This switch starts AutoCAD in a ‘bare minimum state’ to allow users to change AUTOLOADPATH in Options dialog .i.e. If the ‘/safemode’ startup switch is used when launching AutoCAD, no executable code can be loaded and executed. 
Note:  Initially for the /safemode startup switch, we decided to disable all explicit loading of any modules (arx\crx\dbx\lsp\dvb\managed dll, etc), but we found out through testing that this was too restrictive because during AutoCAD’s start up, we explicitly load acmgd.dll, accui.dll and a few others which are necessary for AutoCAD to run.   So instead, we added a new read-only hidden sysvar (SAFEMODEAPPS) to designate which modules can be loaded in safemode.
SAFEMODE
The LISPENABLED system variable introduced in AutoCAD 2012 sp1 has been renamed to SAFEMODE.  This sysvar is read-only and is used to determine whether or not AutoCAD was launched in safemode via the “/safemode” startup switch.
  Item
Description
Name
SAFEMODE (read-only)
Description
Specifies whether executable code can be loaded and executed for the AutoCAD session
Data Type
Integer
Values
0 –executable code can be executed
1 –executable code cannot be executed
Initial Value
0
Stored in
Not Saved- Current Session only
Accessed from
CLI, SETVAR command, startup switch “/safemode”
  SAFEMODEAPPS (hidden, undocumented)
This sysvar is read-only and is used to list the trusted apps that are loaded in safemode via the “/safemode” startup switch.
  Item
Description
Name
SAFEMODEAPPS (read-only)
Description
Specifies which apps can be loaded in safemode.
Data Type
Text
Values
multiple files separated by semi-colons.  AutoCAD only loads the specified files in safemode.
Initial Value
Not documented
Stored in
Named Profile/Registry
Accessed from
CLI, SETVAR command
    New Warning Dialog - When an executable file is found outside Trusted Locations
Default setting in the “Executable File Settings” dialog is “Display warning for executable files outside Trusted locations” (SECURELOAD =1).  When SECURELOAD=1, and AutoCAD tries to load an executable code file from outside of the Trusted locations (Trusted Locations & Trusted Domain Locations) in a non-automation environment, AutoCAD pops up a dialog which warns the user to make sure the file is a trusted file before loading it.   The dialog warns the user about loading files from untrusted locations.
When SECURELOAD=1, this dialog is launched every time AutoCAD detects an executable file that is not in the Trusted Locations.
When SECURELOAD=0 or 2, this dialog is not displayed.
If more than one executable file is detected outside the Trusted Locations, this dialog displays for each file.
If the system does not encounter any of these files outside of the Trusted Locations, then this warning dialog is not displayed.
When SECURELOAD= 2, AutoCAD does not display a dialog warning, and also does not load executable files found if not listed in Trusted locations.  The command line displays “File load canceled: <path\filename>".
{%pathname%}{%custom_filename%} is a variable field and is populated with the <path/filename> of the detected file.
If user picks "Do Not Load", AutoCAD does NOT continue to look for the file in other directories.
We cache the “Do Not Load” or “Load” selection for the session, so the next time the user tries to load the same file, we do not prompt again.
Buttons
Description
Load
Closes the dialog and loads the file.
Do Not Load
Closes the dialog and does not load the file.  This is the default option if the user just presses Enter key.  The command line displays an error message.
Within the APPLOAD dialog, we display:  "Unable to load <filename> file"
When loading from the command line (eg: (load "C:/temp/foo.lsp")), we display: 
"; error: File load canceled: <path\filename>"
Help
Opens the Help topic to SECURELOAD. 
X or ESC key
Closes the dialog and does not load the file. 
  CUIx/MNL Loading changes
acad.MNL (MNL files are just LSP files renamed with .MNL extension).  Prior to AutoCAD 2014, MNL files were autoloaded when the corresponding CUI file was loaded. For example, acad.mnl was always loaded when acad.CUIX was loaded. Many of the viruses try to propagate by editing acad.mnl by adding a line in it to load itself.  
Obviously, this loading style was no longer feasible with the added security. In AutoCAD 2014, we only load the corresponding MNL file if it is found in the TRUSTEDPATHS.  When a CUIX file is loaded we:
1.  Check if the path of the CUIX is on the TRUSTEDPATHS. If so, search for the MNL in that directory only.
2.  If SECURELOAD=1, and if the MNL files are not in Trusted locations, display the File Loading- Security Concern dialog.

If SECURELOAD=2, AutoCAD does not display a warning, and also does not load any MNL file found outside the Trusted locations.
It is recommended that users put shared CUIx files in a read-only location.
Installer Create Deployment Wizard
The Create Deployment wizard that you find in the installer has been enhanced to allow a CAD Manager to set these settings while deploying AutoCAD.  The new settings (same as Executable Code Settings dialog) have been added to the Deployment Wizard Configuration section between the existing Support Content and Search Paths and File Locations sections.
The new section is called “Executable File Settings”
The “Trusted Locations” & “Trusted Domain Locations” branches have been added to the existing Search Paths and File Locations section of the Deployment wizard.
  LISP function
We have added a new lisp function called (findtrustedfile).  It behaves the same as the existing (findfile) function except that it searches the Trusted Locations (TRUSTEDPATHS).
AutoCAD verticals
This functionality behaves exactly the same as in AutoCAD.
AutoCAD OEM 2014
This functionality is available in OEM except the following:
Existing ACADLSPASDOC system variable and related UI is not exposed
No changes to Deployment Wizard.
OEM products have the ability to disable/remove this functionality, including the removal of the system variables and related UI.
AutoCAD for Mac 2014
This functionality is available and behaves nearly identical to AutoCAD for Windows, except there are no UI changes.
The new SECURELOAD, TRUSTEDPATHS & TRUSTEDDOMAINS system variables and the /safemode startup switch is the only way to control the Security settings in AutoCAD for Mac. 
AutoCAD for Mac 2014 has no changes to the Preferences (Options) dialog.
AutoCAD LT 2014
This functionality is not editable in LT.  LT doesn’t have this problem because Lisp & other executable code files cannot be run in AutoCAD LT.
AutoCAD LT hardcodes SECURELOAD=1, and does not expose any of these options in the UI (including the new system variables, Options dialog, or Deployment changes).  Users cannot view or edit the system variables.  Users cannot see the task dialog warning displayed when an executable file attempts to load from outside Trusted Locations (since you can’t load executable code files in AutoCAD LT ), but these code changes are present in AutoCAD LT, just in case there is a way
The Drawing Feed feature, which utilizes the Javascript API, is present in AutoCAD LT.
AutoCAD 2014 Javascript API
If Javascript is detected from a website outside of Executable Code File Search Path, we display the File Loading- Security Concern dialog.

## 评论

**内容**: Martin said...
Thank you for this great read... I have been dealing with this acad.fas virus for a few weeks now. I have over 100 users and some are on 2012, 2013 and 2014. So getting to the bottom has been a nightmare.
I am just unsure why this acad.fas keeps coming back after I deleted it on most of the machines.
I will put some of my new knowledge to work and maybe beat this beast.
Cheers,
Reply
10/10/2013 at 12:54 PM

---
**内容**: BlackBox said...
While I am very pleased that Autodesk has implemented some form of AutoCAD Security, the current mechanism unfortunately suffers multiple pit-falls....
One of which, is that Autodesk has neglected to address the initial, systemic problem, and has only implemented a 'band-aid' to address the symptoms... Changing the order of operation for the FindFile() Method, so that the Support File Search Path (SFSP) is searched first, and if none are found only then search current folder, etc. would allow those who use Acad.[lsp[fas[vlx]]], etc. to be safe, and those who do not would remain just as exposed as they are today.
I've brought this to Autodesk staff's attention multiple times, and even received feedback that this should be done, yet it remains unchanged (for some unknown, presumably good reason?). Further, AutoCAD Security seems to utterly neglect Acad.mnl, etc.
Another is the advent of Autoloader, which is pretty good at doing what it was designed to do (it too has some shortcomings), but doesn't seem to have been designed with Security in mind at all.
Basically, malicious code can now easily create a .bundle in any of the implicitly trusted locations (depending on user permissions), as Autoloader doesn't bother to even check if a given .bundle is Hidden, etc... If a user isn't adept at the complexities of Autolaoder, they might not even notice a malicious .bundle unless it were to cause undesired behavior, frankly.
As discussed with Dieter previously on the topic of Security:
"Coming from the Military myself, the security gamble isn't about preventing exploitation of all possible vulnerabilities... It’s about securing your weakest points in critical order for mission accomplishment, controlling the flow of information, early warning system redundancy, and something that even the lowest ranking Soldier knows... Overlapping fields of fire." - BlackBox
Cheers
Reply
10/12/2013 at 05:30 PM

---
**内容**: Kevin Busacker said...
Thank you for this great article. I do not see AUTOLOADPATH documented in the 2012 SP1 ReadMe like it was with 2013 SP1. Was this such a new feature in 2012 that it was available, but just did not make it to press?
Reply
12/11/2013 at 06:48 AM

---
**内容**: Will Baron said...
A very helpful error message indeed: 'File load canceled: C'! Googling errors that contain spelling mistakes is always more successful than when they don't!
Reply
09/16/2014 at 06:25 AM

---
**内容**: nageswar rao said...
http://bim4scottc.blogspot.in/2013/05/pdf-to-autocad-conversion.html
Reply
10/20/2014 at 03:22 AM

---
**内容**: Andrey Bushman said...
It is must to be AutoCAD 2013 SP1 instead of AutoCAD 2012 SP1.
Reply
08/26/2015 at 05:22 AM

---
