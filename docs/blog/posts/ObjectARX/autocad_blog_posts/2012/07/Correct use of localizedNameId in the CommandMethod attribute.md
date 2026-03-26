---
title: "Correct use of localizedNameId in the CommandMethod attribute"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Our AutoCAD .NET Wizard project template downloadable from the AutoCAD Developer Center includes some boilerplate code to demonstrate how to create..."
author: Autodesk
---
# Correct use of localizedNameId in the CommandMethod attribute

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/correct-use-of-localizednameid-in-the-commandmethod-attribute.html

## 文章内容

By Stephen Preston
Our AutoCAD .NET Wizard project template downloadable from the AutoCAD Developer Center includes some boilerplate code to demonstrate how to create various command types. The first command definition looks like this:
        <CommandMethod("MyGroup", "MyCommand", "MyCommandLocal", CommandFlags.Modal)> _
        Public Sub MyCommand() ' This method can have any name
            ' Put your command code here
        End Sub
A common misunderstanding is thinking that the “MyCommandLocal” string is actual localized command name – someone making that mistake will try to edit that string to create a new localized command name. This string is actually the Id of a string resource in the project, and it’s the string resource that contains the localized commandname. You can see this by clicking the ‘Show All Files’ button in the Visual Studio Solution Explorer and double clicking on the myCommands.resx file.
This opens up the resource file, where you can edit the resource string:
Kean covered this topic back in 2009, and included instructions for creating additional localized resx files to allow your plug-in to support multiple languages. I’m restating it now because we still receive questions on this from time to time.
Once you’ve created your localized plug-in, you can set localized command names in your Autoloader PackageContents.xml file too. For example, here is a <Commands/> group defining a <Command/> that has a global and local name:
<Commands GroupName="ADNPLUGINS">
  <Command Local="BATCHPUBLISH" Global="BATCHPUBLISH" />
</Commands>
You can add additional per local localized names like this:
<Commands GroupName="ADNPLUGINS">
<Command LocalEnu="BATCHPUBLISH_IN_ENGLISH" LocalDeu="BATCHPUBLISH_IN_GERMAN" LocalFra="BATCHPUBLISH_IN_FRENCH" Global="BATCHPUBLISH" />
</Commands>
and so on …

## 评论

**内容**: Steve said...
Thanks for this post Stephen.
Could you expand on how to support multiple languages? Is it just something we have to designate in the XML file, or does it have to be done in the vb.NET file?
Steve
Reply
12/04/2012 at 08:59 AM

---
**内容**: Madhukar Moogala said in reply to Steve...
Hi Steve. You have to do both. Here's a link to KEan Walmsley's post on setting up localized strings for your .NET app - http://through-the-interface.typepad.com/through_the_interface/2009/06/registering-autocad-commands-with-localized-names-using-net.html.
Reply
12/04/2012 at 10:13 AM

---
**内容**: Steve said...
Thanks Stephen.
Reply
12/05/2012 at 06:27 AM

---
