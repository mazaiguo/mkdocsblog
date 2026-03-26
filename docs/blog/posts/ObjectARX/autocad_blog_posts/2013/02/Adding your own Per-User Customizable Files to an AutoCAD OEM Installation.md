---
title: "Adding your own Per-User Customizable Files to an AutoCAD OEM Installation"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
  - Palette
  - Plugin
description: "In my OEM Installation, I want to be able to add files to the user customizable folders on a per-user basis.  I've used the Wizard to add files the..."
author: Autodesk
---
# Adding your own Per-User Customizable Files to an AutoCAD OEM Installation

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/adding-your-own-per-user-customizable-files-to-an-autocad-oem-installation.html

## 文章内容

By Fenton Webb
Issue
In my OEM Installation, I want to be able to add files to the user customizable folders on a per-user basis.  I've used the Wizard to add files there, but they don't get copied when I switch users.  How can I add files to the OEM installer that will be present for every user that runs my product?
Solution
There are three separate mechanisms used by the AutoCAD/OEM installer to place files, depending on when and where the files are ultimately placed (it is assumed the reader has some experience working with MSI).
During 'primary' installation (first normal installation, run as an administrator) the user customizable files are copied to the ‘UserDataCache’ folder under the target install directory, as normal.  Since the user files must also be placed in the roamable per-user folders, the DuplicateFile table is then used to copy these files during a separate action during the primary install.
During ‘secondary install’ (spawned the first time the OEM product is run as a different user), it is assumed the current user has changed, and the user files must be copied to the new user's per-user data folder again.  The installer uses entries found in the ‘MoveFiles’ table to copy them over.
So, for an OEM installer, we can add a couple things to our MSI to make this work.  For the example where we add a file (test.bmp) to the ‘<roamable per-user profile>Support\ToolPalette\Images’ folder, we can use these steps:
1)  Add the image file to the ‘Per-User Support’ target in the OEMMakeWizard.  While this doesn’t get this file exactly where we want it to be, it does get us closer by adding the file to the File table in MSI (after we run the OEMInstallerWizard).
2) Build the project with the OEM MakeWizard and build the MSI with the OEMInstallerWizard.
3) In the CD image for the install create a folder named 'Images'. If you used the suggested naming convention suggested in the help file for the Installer Wizard the path to add the Images folder would be similar to this:
..\TargetMaster\Program Files\<nameOfApp>\UserDataCache\ToolPalette\
4) Manually move the image file from:
..\TargetMaster\Program Files\UserDataCache\Support
To the new Images directory added in step three. 
5)  Edit the MSI for your install with a utility such as Orca. (Available free as the ‘Database Tool’ in the Installer SDK from MSDN)  Add ‘UserToolPaletteImagesFolder’ to the Directory Table, with a parent of ‘UserToolPaletteFolder’ and a DefaultDir of ‘Images’.  Similarly, add ‘RoamingUserToolPaletteImagesFolder’ with a parent of ‘RoamingUserToolPaletteFolder’ and a DefaultDir of ‘Images’.  We must do this since we’re adding directories to both the UserDataCache and the user support folders.
UserToolPaletteImagesFolder UserToolPaletteFolder   Images
RoamingUserToolPaletteImagesFolder  RoamingUserToolPaletteFolder   Images
6) Change the Directory entry for the component in the Component table which represents your file to the ‘UserToolPaletteImagesFolder’.  You can find this component by using ‘Find’ (Ctrl+F), searching for your filename from the top of the Component table.
COMP_test.bmp <UUID for test.bmp> UserToolPaletteImagesFolder   0
7)  Find the entry in the DuplicateFile table that represents your file. The information for these fields should be obtained from the fields for this file in the File table.  The ‘FileKey’ and ‘File’ fields can be the set to the contents of the ‘File’ field in the File table. The Component is set similarly.  The DestName can be equivalent to ‘FileName’, and the DestFolder should be the target for the file in the roaming folders, in this example ‘RoamingUserToolPaletteImagesFolder’.
FILE_test.bmp  COMP_test.bmp FILE_test.bmp   test.bmp  RoamingUserToolPaletteImagesFolder
Note: You can copy and paste the entries from the File Table. However ensure that no trailing spaces are added. Also if an error occurs when trying to modify this row, add a new row and use the information from the existing row. (Then delete the original row).
8) Add an entry in the ‘MoveFile’ table to represent your file. The FileKey and Source folder can be the same, set to the source of the move/copy operation.  In this example ‘UserToolPaletteImagesFolder’ for the directory we created in the UserDataCache.  The ‘DestFolder’ is the destination of the move, ‘RoamingUserToolPaletteImagesFolder’.  The ‘Component’ entry  should be ‘Comp_duplicate_roamable_file’ and ‘SourceName’ should be ‘*.*’.
UserToolPaletteImagesFolder Comp_duplicate_roamable_file   *.*   UserToolPaletteImagesFolder            RoamingUserToolPaletteImagesFolder   0
9) After making these changes to the MSI, the image file will be available in the user's profile directory. (..ToolPalette\Images). When the  OEM product is run and shut down, it will create a couple of new directories for the Palettes and Images. (..\ToolPalette\Palettes\Images). The image files will be created in the new Images directory.
That should do it.  Your file should be included in each user's per-user data!

