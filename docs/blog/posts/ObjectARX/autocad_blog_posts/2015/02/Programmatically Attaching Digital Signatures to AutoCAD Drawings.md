---
title: "Programmatically Attaching Digital Signatures to AutoCAD Drawings"
date: 2015-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - DWG
  - DXF
description: "In this blog we will see how we can leverage SecurityParams AutoCAD .NET API to digitally sign drawings[read DWG\DXF]."
author: Autodesk
---
# Programmatically Attaching Digital Signatures to AutoCAD Drawings

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/programmatically-attaching-digital-signatures-to-autocad-drawings.html

## 文章内容

By Madhukar Moogala
In this blog we will see how we can leverage SecurityParams AutoCAD .NET API to digitally sign drawings[read DWG\DXF].
First and foremost important thing is to have Digital Certificate issued from a recognised vendor, about code signing fundamentals you can refer to this, Certificate vendor generally issues a PFX and password which is require to register in store, for registration of Certificate in store, we can take help of Certificate Import Wizard available in Internet Explorer Tools\Internet Options\Content\Certificates
After registering Certificate in store, here are few preliminary checks.
Launch “AcSignApply.exe” Tool shipped with AutoCAD and available in ProgramFiles\AutoDesk\AutoCAD XXX\. And check if your Digital Certificate is available.
Interactively attach your Digital signature to DWG and check if drawing is getting signed.
In the below screen shot I have shown a Certificate issued by VeriSign which I used for testing.
If you are able to sign the drawings interactively the same should be possible using API, here is the code to do.
public void DWGSign() // This method can have any name
{
string subject;
string issuer;
string serialNumber;
string comment;
string timeServer;
uint keyLength;
uint providerType;
// The path to the certificate.
string PFXpath = "C:\\Sign\\Test.pfx";
/*password given by CA,
* this is same password which you enter while installing PFX in store*/
string pwd = "TestPassword";
// Load the certificate into an X509Certificate object.
X509Certificate2 cert = new X509Certificate2();
/*Importing certificate*/
cert.Import(PFXpath, pwd, X509KeyStorageFlags.PersistKeySet);
  /*verify certificate*/
bool verificationResult = cert.Verify();
/*Get the CommanName, CN of CA*/
issuer = cert.GetNameInfo(X509NameType.SimpleName, true);
subject = cert.GetNameInfo(X509NameType.SimpleName, false);
  /*get serial number*/
serialNumber = cert.SerialNumber;
comment = "You can describe the Drawing info here";
/*If timeserver is null, application picks computer time*/
timeServer = "Natl Inst of Standards and Technology(time.nist.gov)";
  /*Encyrption key size*/
keyLength = (uint)cert.PublicKey.Key.KeySize;
/*Numeric Id*/
providerType = (uint)cert.Version;
  try
{
  string mainfullpath = "C:\\Temp\\Architectural - Metric.dwg";
Database tempDb;
  using (tempDb = new Database(false, true))
{
tempDb.ReadDwgFile(mainfullpath,
FileShare.ReadWrite,
false,
"");
tempDb.CloseInput(true);
SecurityParameters sp = new SecurityParameters(null,
null,
subject,
issuer,
serialNumber,
comment,
timeServer,
SecurityActions.SignData,
SecurityAlgorithm.RC4,
keyLength,
providerType);
  mainfullpath = "C:\\Temp\\Signednew.dwg";
tempDb.SaveAs(mainfullpath, false, DwgVersion.Current, sp);
}
  }
catch (SystemException ex)
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    ed.WriteMessage(ex.Message);
}
  }
  After succeeding code, you would see a logo on the DWG thumbnail and when opened in AutoCAD you would get entire signing information of the drawing.

## 评论

**内容**: eSignature said...
A special thanks for this informative post. I definitely learned new stuff here I wasn't aware of !
Reply
05/29/2015 at 04:38 AM

---
**内容**: FredSenior said in reply to eSignature...

Dear Madhukar Moogala,
Thanks for the code you posted above.
I want to know, how can i get the validity statue of digital signature in dwg drawing IN MY CODE.
In AutoCAD command line, the command "sigvalidate" can show the validity of signature in current drawing,
but how can i get this message in my code ?
Many thanks!
Reply
07/02/2016 at 11:07 PM

---
