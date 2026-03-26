---
title: "Can I sign my AutoCAD .NET plug-in with a strong name?"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "I am trying to create a strong name for my assembly, but it raises the following error message: "Referenced assembly 'acmgd' does not have a strong..."
author: Autodesk
---
# Can I sign my AutoCAD .NET plug-in with a strong name?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/can-i-sign-my-autocad-net-plug-in-with-a-strong-name.html

## 文章内容

By Marat Mirgaleev
Issue
I am trying to create a strong name for my assembly, but it raises the following error message: "Referenced assembly 'acmgd' does not have a strong name". Is there any way to solve this?
Solution
Unfortunately, we do not provide strong named versions of AutoCAD .NET assemblies. There are some reasons for this:
- A strongly named assembly adheres to a stricter versioning policy: patching the dll is trickier;
- A strongly named assembly must be installed into the GAC to avoid the performance hit related to extra validation. The GAC itself further complicates deployment.
By the way, we signed our dlls in AutoCAD 2005 and we got rid of the signatures because of the complications.
Thus, your assembly cannot have a strong name if it depends on AutoCAD assemblies.
However there are workarounds available:
- Instead of setting security policy for file you can set it for entire folder:
   CasPol.exe -m -ag 1.2 -url "\\YourNetworkDrive\Path\*" FullTrust -name MYNAME
or
- Sign your assembly with Authenticode signature and configure to trust the 'publisher'.

## 评论

**内容**: Andrey said...
And I too was faced with this problem in the past, and the solution of Autodesk wasn't pleasant to me...
>A strongly named assembly adheres to a stricter versioning policy: patching the dll is trickier;
Administrator can to manage search of assembly via acad.config file. It even is convenient. What can be a problem in it?
>A strongly named assembly must be installed into the GAC to avoid the performance hit related to extra validation.
How strongly it influences on productivity?
>The GAC itself further complicates deployment.
What's the problem?
>However there are workarounds available:
The offered answers aren't responses to the given question.
Reply
08/27/2012 at 02:39 AM

---
**内容**: Albert said...
Hi Andrey,
If we strongly name an assembly then we must put into the GAC otherwise we take a massive performance hit when the assembly is loaded (because all pages in the image must be loaded and hashed).
Once we put an assembly into the GAC we must make sure that the dependencies of the assembly are also in the GAC or SxS so that they can be loaded.
acmgd.dll depends on acad.exe which means that we would have to put acad.exe and all of its dependencies into the GAC/SxS. This would create more problems than it would solve. See how VS 2012 moves away from SxS to offer easier deployment for C/C++ runtime, MFC.
Albert
on behalf of the AutoCAD Team
Reply
10/29/2012 at 08:21 AM

---
**内容**: Carl said...
ok, 2015 autocad has stuffed us!!! pre-2014 we could do binary serialization on our custom object, but no longer!!! not either autocad or net4.5 REQUIRES strongly typed names in the GAC to do this!!! So now I'm desperately trying to get and attach a cert for interanl software!! I just did and guess what - "vbc : error BC30145: Unable to emit assembly: Referenced assembly 'Acdbmgd' does not have a strong name" - with a digital signature. What the heck are we supposed to do here!!??
Reply
03/02/2015 at 05:09 PM

---
**内容**: Ben said...
So then, what are the implications if i want to obfuscate my dll?
I'm quoting from the CryptoObfucsator manual:

>> Enable Tamper Detection
> When checked, Crypto Obfuscator will itself perform strong name verification of the assembly even if strong-name verification has been turned OFF on the machine on which the assembly is running or if the assembly has been registered in the verification 'skip-list' - this is typically done by hackers or crackers. Furthermore, the strong name verification is done using the original key used to sign the assembly when it was obfuscated by Crypto Obfuscator. Thus, strong name verification fails even if the key is removed or replaced - again something typically done by hackers or crackers.
> Note that your assembly must be originally strong named for this to work and you must specify the same strong name key via the Signing / Authenticode tab. If you turn ON this setting for an assembly for which you have not specified a strong name key, you will receive the following error message:
> The assembly xyz has the 'Enable Tamper Detection' setting ON but no key file is specified via the 'Signing / Authenticode' tab. Please specify a key file and try again.
So what are the implications of this: I cannot enable tamper detection on my assembly using crypto-obfuscate?
rgds
Ben

Reply
03/20/2016 at 05:23 PM

---
