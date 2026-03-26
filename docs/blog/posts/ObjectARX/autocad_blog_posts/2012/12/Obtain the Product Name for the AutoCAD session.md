---
title: "Obtain the Product Name for the AutoCAD session"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "There is a key in the registry for each particular installation of AutoCAD called 'ProductName' which has this information.  You can get to the par..."
author: Autodesk
---
# Obtain the Product Name for the AutoCAD session

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/obtain-the-product-name-for-the-autocad-session.html

## 文章内容

By Virupaksha Aithal
There is a key in the registry for each particular installation of AutoCAD called 'ProductName' which has this information.  You can get to the particular session's root key via the MachineRegistryProductRootKey member of HostApplicationServices.  From this you can query the ProductName to receive the actual name of the installation you are running. 
[CommandMethod("ProductName")]
public static void ProductName()
{
    string strReg =
       HostApplicationServices.Current.MachineRegistryProductRootKey;
      using (RegistryKey prod =
                    Registry.LocalMachine.OpenSubKey(strReg, false))
    {
        string strProduct = prod.GetValue("ProductName") as string;
          Document doc = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
        ed.WriteMessage(strProduct + "\n");
    }
}

