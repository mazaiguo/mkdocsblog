---
title: "CUIX Extended Help Tooltips using XAML Resource DLL"
date: 2016-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
description: "AutoCAD provides two ways to support tooltip, one is the“Extended Help File”, which was designed to support absolute path only."
author: Autodesk
---
# CUIX Extended Help Tooltips using XAML Resource DLL

发布日期: 2016-02-01

原始链接: https://adndevblog.typepad.com/autocad/2016/02/cuix-extended-help-tooltips-using-xaml-resource-dll.html

## 文章内容

By Madhukar Moogala
AutoCAD provides two ways to support tooltip, one is the“Extended Help File”, which was designed to support absolute path only.
This method is intended to be used by end-users so it’s very limited.
The other one is modifying the cui file in order to add a default location for tooltip resources, which is also used by acad and
verticals:
Open the cui file:
Before 2010, there is only acad.cui and that’is it; for 2010 and later, you need unzip the .cuix file to get several editable cui files and the header.cui is what we need.
At the beginning of the cui file, you can find xml nodes like below:
<CustSection xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <FileVersion MajorVersion="0" MinorVersion="6" IncrementalVersion="1" UserVersion="0" />
  <Header>
    <FileReferences>
      <ToolTipFileReferences>
        <ContentSources>
          <ContentSource>AcCommandToolTips;component/CommandToolTips.xaml</ContentSource>
          <ContentSource>VerticalTips;component/CommandToolTips.xaml</ContentSource>
         </ContentSources>
      </ToolTipFileReferences>
    </FileReferences>
    <CommonConfiguration>
Add your own ContentSource as necessary. Note that if you
are using assembly like acad does, the assembly must be in the same/sub folder
as the acad.exe:
Referenced Assembly Resource File
The pack URI for a resource file that is compiled into a referenced assembly uses the following authority and path:
Authority: application:///.
Path: The name of a resource file that is compiled into a referenced assembly. The path must conform to the following format:
AssemblyShortName[;Version][;PublicKey];component/Path
AssemblyShortName: the short name for the referenced assembly.
;Version [optional]: the version of the referenced assembly that contains the resource file. This is used when two or more referenced assemblies with the same short name are loaded.
;PublicKey [optional]: the public key that was used to sign the referenced assembly. This is used when two or more referenced assemblies with the same short name are loaded.
;component: specifies that the assembly being referred to is referenced from the local assembly.
/Path: the name of the resource file, including its path, relative to the root of the referenced assembly's project folder.
  Referenced Assembly Resource File
The pack URI for a resource file that is compiled into a referenced assembly uses the following authority and path:
Authority: application:///.
Path: The name of a resource file that is compiled into a referenced assembly. The path must conform to the following format:
AssemblyShortName[;Version][;PublicKey];component/Path
AssemblyShortName: the short name for the referenced assembly.
;Version [optional]: the version of the referenced assembly that contains the resource file. This is used when two or more referenced assemblies with the same short name are loaded.
;PublicKey [optional]: the public key that was used to sign the referenced assembly. This is used when two or more referenced assemblies with the same short name are loaded.
;component: specifies that the assembly being referred to is referenced from the local assembly.
/Path: the name of the resource file, including its path, relative to the root of the referenced assembly's project folder.
Note: Excerpt is borrowed from <https://msdn.microsoft.com/library/aa970069(v=vs.100).aspx>
Example :
<FileReferences>
      <ToolTipFileReferences>
        <ContentSources>
          <ContentSource>AcCommandToolTips;component/CommandToolTips.xaml</ContentSource>
          <ContentSource>VerticalTips;component/CommandToolTips.xaml</ContentSource>
          <!--Adding CmdToolTip_Resource is short name of my assembly[dll]-->
          <!--CommandToolTips_New.xaml is my resource file -->
              <ContentSource>CmdToolTip_Resource;component/CommandToolTips_New.xaml</ContentSource>
        </ContentSources>
      </ToolTipFileReferences>
    </FileReferences>
Finally, zip the cui files back into a cuix file if necessary.
Let us :
First we need to create an XAML file, we can define many number of tooltips for ribbon button in a single file.
To establish association or mapping between ribbon tool tip and ribbon command button, we will refer ribbon command button’s element id in our XAML file.
I have created a single ribbon command button and XAML to display tooltip.
My extended tool tip :
‘
  XAML sample :
<ResourceDictionary
 xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
 xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
 xmlns:System="clr-namespace:System;assembly=mscorlib"
 xmlns:src="clr-namespace:Autodesk.Windows;assembly=AdWindows"
 x:Uid="ResourceDictionary_">
<src:RibbonToolTip x:Key="MMU_201_3AF55">
     <!--MMU_201_3AF55 is the element id of RibbonCommandButton-->
<src:RibbonToolTip.ExpandedContent>
<StackPanel>
<TextBlock Background="AntiqueWhite" TextAlignment="Center">
    With great power comes great responsibility
    <Image Source="SpiderMan.gif" Width="Auto" Height="Auto">
   </Image>
</TextBlock>
</StackPanel>
</src:RibbonToolTip.ExpandedContent>
</src:RibbonToolTip>
</ResourceDictionary>
Now we will see how to create a content source assembly [DLL]
Create a class library from Visual Studio as mentioned here
Now, delete the class that has been created by wizard template.
Add your image file via “Add an Existing Item” which you want to reference in your xaml file.
After adding change the properties of “Build Action” to Resource and “Don’t Copy to OutPut Directory”
Add your XAML file via “Add an Existing Item”
After adding change the properties as follows
Now build the project and copy the assembly to AutoCAD executable location, this is very important.
You can automate unzipping, updating CUIX and Zipping programmatically as follows.
/*Recursively crawling through XML structure*/
     static XElement UpdateXmlElement(XElement element)
      {
         if (element.Name.LocalName.Equals("ContentSources"))
          {
             element.Add(new XElement("ContentSource", "CmdToolTip_Resource;component/CommandToolTips_New.xaml"));
             return element;
          }
         else{
             foreach(XElement child in element.Elements())
             {
                 UpdateXmlElement(child);
             }
         }
           return element;
      }
      static void CUIEditor
      {
         string cuixFile = "C:\\Temp\\CuixEditor\\CuixEditor\\acad.cuix";
            if(!File.Exists(cuixFile)) return;
          using (ZipArchive zip = ZipFile.Open(cuixFile,ZipArchiveMode.Update))
          {
              /*the Header.cui, which is an XML file*/
              ZipArchiveEntry entry = zip.GetEntry("Header.cui");
              if (entry.FullName.Equals("Header.cui"))
                  {
                  /*We need to append our custom xaml file to ContentSources element availble in Header CUI*/
                      String fn = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());
                      entry.ExtractToFile(fn);
                      XElement element = XElement.Load(fn);
                        XElement contentSource = UpdateXmlElement(element);
                      contentSource.Save(fn);
                      entry.Delete();
                      zip.CreateEntryFromFile(fn, "Header.cui");
                      File.Delete(fn);
                    }
                }
Please find CommandToolTip source file

## 评论

**内容**: Pierre de la Verre said...
Thanks, important topic!
Pierre
Reply
03/04/2016 at 03:12 AM

---
**内容**: José Luis said...
How can I add the xaml files in my c ++ resource project?
Reply
02/07/2017 at 09:07 AM

---
