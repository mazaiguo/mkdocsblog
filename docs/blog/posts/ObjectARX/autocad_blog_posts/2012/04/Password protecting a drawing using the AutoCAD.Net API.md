---
title: "Password protecting a drawing using the AutoCAD.Net API"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - DWG
  - Database
description: "Password for a drawing can be set through program by using the "Database.SaveAs" method. Here is a sample code to demonstrate the use of the "Secur..."
author: Autodesk
---
# Password protecting a drawing using the AutoCAD.Net API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/password-protecting-a-drawing-using-the-autocadnet-api.html

## 文章内容

By Balaji Ramamoorthy
  Password for a drawing can be set through program by using the "Database.SaveAs" method. Here is a sample code to demonstrate the use of the "SecurityParameters" to password protect your drawing.
The links provided in the code refer to MSDN documentation. These can help you choose a provider and the key length. Since "RC4" is the only algorithm supported by AutoCAD, it important to select the key length from the list keeping this in mind.
[CommandMethod("PwdProtect")]
static public void PwdProtectMethod()
{
    String dwgFilePath = "C:\\Test.dwg";
    if (!System.IO.File.Exists(dwgFilePath))
        return;
      string password = "Autodesk";
      // Choose a provider name from the list of providers
    //http://msdn.microsoft.com/en-us/library/windows/desktop/
    //aa380243(v=vs.85).aspx
    string providerName
        = "Microsoft Enhanced Cryptographic Provider v1.0";
      string subject = null;
    string issuer = null;
    string serialNumber = null;
    string comment = null;
    string timeServer = null;
    SecurityActions actions = SecurityActions.EncryptData;
    SecurityAlgorithm algorithm = SecurityAlgorithm.RC4;
      // Find the default/min/max key length
    // for the provider name used
    // http://msdn.microsoft.com/en-us/library/windows/desktop/
    // bb931357(v=vs.85).aspx
      uint keyLength = 128;
    uint providerType = 1;
      try
    {
        using (Database db = new Database(false, true))
        {
            db.ReadDwgFile
                (
                    dwgFilePath,
                    System.IO.FileShare.ReadWrite,
                    true,
                    ""
                );
              SecurityParameters sp
                = new SecurityParameters
                                        (
                                            password,
                                            providerName,
                                            subject,
                                            issuer,
                                            serialNumber,
                                            comment,
                                            timeServer,
                                            actions,
                                            algorithm,
                                            keyLength,
                                            providerType
                                        );
            db.SaveAs
                    (
                        db.Filename,
                        false,
                        DwgVersion.Current,
                        sp
                    );
        }
    }
    catch (System.Exception ex)
    {
        Editor ed =
        Application.DocumentManager.MdiActiveDocument.Editor;
          ed.WriteMessage(ex.Message);
    }
}
-Balaji

## 评论

**内容**: Fernando said...
Probably you will never read me, but it is the third example from your .net codes
i have tried and netloaded acording to the rules and syntaxis, 2 of them in C#
and one in VB.Net and.... neither one nor the others works.
I'm stunned, this is insulting.
Reply
01/22/2019 at 08:03 PM

---
