---
title: "Removing the partial customization file"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - CUI
description: "Following code which iterates the PartialCUIFiles collection and does check to see if the CUIX file with the Filename is exists using Fileexists, i..."
author: Autodesk
---
# Removing the partial customization file

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/removing-the-partial-customization-file.html

## 文章内容

By Virupaksha Aithal
Following code which iterates the PartialCUIFiles collection and does check to see if the CUIX file with the Filename is exists using Fileexists, if its not exists then we remove the partialCUI file from the collection and save , reload the CUI.
[CommandMethod("RCUI")]
public void RemovePartcialCUI()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
      // Load all the partial CUIX files,
    //They are not loaded when the main cuix file
    // is loaded with command line version of CUILOAD
    string mainCuiFile = (
                    string)Application.GetSystemVariable("MENUNAME");
    mainCuiFile += ".cuix";
    CustomizationSection cs = new CustomizationSection(mainCuiFile);
      //remove first unknown file...
    foreach (string fileName in cs.PartialCuiFiles)
    {
        if (!File.Exists(fileName))
        {
            cs.PartialCuiFiles.Remove(fileName);
            cs.Save();
            break;
        }
    }
    if (cs.IsModified)
        cs.Save();
    string flName = cs.CUIFileBaseName;
      Application.SetSystemVariable("FILEDIA", 0);
    doc.SendStringToExecute("cuiunload " + flName + " ",
                                                false, false, false);
    doc.SendStringToExecute("cuiload " + flName +
                                  " filedia 1 ", false, false, false);
}

