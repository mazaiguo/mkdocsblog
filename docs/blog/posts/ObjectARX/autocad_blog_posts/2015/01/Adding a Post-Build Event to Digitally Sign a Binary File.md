---
title: "Adding a Post-Build Event to Digitally Sign a Binary File"
date: 2015-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plugin
description: "This blog post assumes reader is aware of digital signatures ,if not please refer following link Code Signing"
author: Autodesk
---
# Adding a Post-Build Event to Digitally Sign a Binary File

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/adding-a-post-build-event-to-digitally-sign-a-binary-file.html

## 文章内容

By Madhukar Moogala
  This blog post assumes reader is aware of digital signatures ,if not please refer following link Code Signing
I will demonstrate how you can you add a  simple code command line to digital sign your executable files like .exe \.dll.
If you are not aware of post build event feature in VS project , please go through following link. Post Build Event
  On a Windows machine SignTool.exe is available from Microsoft that enables signing executable files. It can be used to sign both the managed (.NET) and native files. The sign tool takes the pfx file with the public and the private key as the input.
Post build Command Line :
Usage : signtool sign  /f <yourPfxfile> /p <password>  <executablefile>
/f is signcertfile , Specifies the signing certificate in a file. Only the Personal Information Exchange (PFX) file format is supported.If the file is in PFX format protected by a password, use the /p option to specify the password.
    Example : call "C:\Program Files (x86)\Windows Kits\8.0\bin\x86\signtool.exe" sign /f "C:\mkCert\mypfxfile.pfx" /p "autodesk123" $(TargetPath)
For further reading and other command line options ,please refer
SignTool
  What is PFX file and How to get one ?
Personal Format Exchange is a Microsoft format extension for PKCS#12 , contains public and private keys for the associated certificate , these certificates are issued by Certificate Authorities and can be purchased from vendors like Verisign  etc, more information on issuing authorities can be found Certificate Authority.
We can also create our own certificate for testing and internal distribution, paraphrasing wiki definition of Digital Certificate which we are about to create.
A digital certificate certifies the ownership of a public key by the named subject of the certificate. This allows others (relying parties) to rely upon signatures or on assertions made by the private key that corresponds to the certified public key. In this model of trust relationships, a CA is a trusted third party - trusted both by the subject (owner) of the certificate and by the party relying upon the certificate.
    We need two tools to create Certificate “MakeCert” and “Pvk2Pfx” these are shipped with  Visual Studio, launch Developer Command Prompt
  1. MakeCert
This tool outputs the certificate as a .cer file and generates a pvk file it is not exist.
Usage :
makecert -sv yourprivatekeyfile.pvk -n "cert name" yourcertfile.cer -b mm/dd/yyyy -e mm/dd/yyyy –r
Example :
makecert -sv C:\DigiCertificate\myPrivateKey.pvk -n "CN=\"Madhukar,M\" " C:\DigiCertificate\myCertifacte.cer -b 01/07/2015 -e 01/30/2015 –r
while mentioning  name against ‘-n’ option , you need follow X500 naming standard , characters like quotes comma etc. are reserved ,you need to use escape codes to get them or else makecert throws an error
Error: CryptCertStrToNameW failed => 0x80092023 (-2146885597)
Failed
For more information on Distinguished Names
You will be prompted to set the password for the private key file.
You will again be prompted to enter the password to sign the certificate. Please note that this is a self-signed certificate and so you will be signing the public key with the private key.
Here is a snap shot of a self-signed certificate ,aka cer file.
The certificate has the following information.
Version number of the certificate, the current version is 3.
Certificate serial number, the unique serial number is specific to a CA.
Signature, it includes the algorithm used for signing.
Issuer name, the certificate authority name.
Validity period of the certificate.
Subject name, in this case the publisher name.
Subject public key info, the public key of the publisher.
Here is a snap shot of cer file details.
2. Pvk2pfx
This tool is used to create a pfx file that can be used for signing. The pfx file has the certificate, the public and the private key of the publisher.
Usage:
pvk2pfx –pvk yourprivatekeyfile.pvk -pi password –spc yourcertfile.cer –pfx yourpfxfile.pfx –po yourpfxpassword
Example:
pvk2pfx -pvk C:\DigiCertificate\myPrivateKey.pvk –pi pvkpassword -spc C:\DigiCertificate\myCertifacte.cer -pfx C:\DigiCertificate\myPfxfile.pfx –po pfxpassword
Note : -pi <pvk-pswd>   - PVK password.
         -po <pfx-pswd>   - PFX password; same as -pi if not given.
At the end of this operation you will have a .pfx file that can be used for signing as stated above in the post.

## 评论

**内容**: binary file said...
this is a software to compare two files easily and efficiently. Binary file compare is the technique ... in digital environment between the folders and files present in that environment. I think It is almost ...
Reply
01/22/2015 at 05:14 AM

---
**内容**: digital signature autocad said...
EXCELLENT information. Your directions are clear and concise, and easy to follow. Thanks for your hard work in posting this info.
Reply
03/29/2015 at 12:33 AM

---
**内容**: gamis modern said...
your article is very interesting
Reply
06/17/2015 at 01:44 AM

---
**内容**: digital signature said...
This article is very help to me. Thank you for this. please provide more things related to this.
Reply
03/11/2022 at 10:33 PM

---
