---
title: "Autoloader and localization"
date: 2013-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - AutoLISP
  - C++
description: "Have you noticed that the Autodesk Exchange Store website is showing its UI interface in non-English? From the website perspective, it will automat..."
author: Autodesk
---
# Autoloader and localization

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/autoloader-and-localization.html

## 文章内容

By Augusto Goncalves
What's coming
Have you noticed that the Autodesk Exchange Store website is showing its UI interface in non-English? From the website perspective, it will automatically select the correct version according to the ‘Language’ settings of the browser, or you can select at the bottom of the page.
Now the interesting point: we’ll soon start accepting applications that are in other languages, including multi-language or localized only (e.g. German only apps).
This post will show how make your application work for multi-language using the Autoloader mechanism.
Background
The AutoCAD command registration can work with names in English and non-English, called Global and Local names, respectively. With .NET API we can implement this feature with Resources, as described here, which work for all supported languages on the same assembly, also can be used for command line strings and for other resources. Now ObjectARX supports one Global and one Local command name, usually one English and one non-English, and can load resources for different languages (if manually implemented). Finally Lisp don’t have a build-in localization feature.
The Autoloader mechanism (.bundle folder and PackageContents.xml) can be used when the application is multi-language (i.e. supporting more than 1 language). The XML support localization for almost all properties and modules, by loading the correct file according to the product language. If you application have only 1 language, even non-English, then there is no need for this localization features (as it will always load the same modules).
Approaches
There are some approaches to create an application that can work on different languages. In some cases, the application will have only one non-English language, for instance, if is designed for a specific market. As already mentioned, if is only 1 language, then no additional work is necessary (as the same modules will load every time).
If your code automatically identify the language and change its command name and interface, e.g. using .NET Resources, then great. This post will show the simples approach: separated modules for each language.
Using the PackageContents
Let say an application have 2 languages, English and Portuguese. The idea is to enable the ‘HelloWorld’ command on English systems and ‘OlaMundo’ on Portuguese systems (either by OS, AutoCAD or Regional Settings configured to this language). The images below show it running, of English and Portuguese environments, respectively.
For this case, there are 2 DLLs, that register and have all resources for both languages. The goal is to ensure only the correct DLL will be loaded on each system. This approach can be used for DLLs, ARX, DBX, Lisp or CUIx files, just specify which file is loaded on each supported locale and the Autoloader will make sure the correct version is loaded.
The following XML code show some attributes suffixed with Ptb, which then contain the specific version of the data, and the affected lines are marked in yellow. Note the OnlineDocumentation and ModuleName attributes. The last marked lines contains the commands names, Global and Local, where the Local is suffixed by Ptb. Other markup, line Description, are required so the user can understand what the application will do. The HelpFile will make sure the proper help is opened when the user press F1.
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0"
                    AutodeskProduct="AutoCAD"
                    Name="My Global Product"
                    Description="Global Product"
                    DescriptionPtb="Produto Global"
                    AppVersion="1.0.0"
                    FriendlyVersion="1.0.0"
                    ProductType="Application"
                    SupportedLocales="Enu|Ptb"
                    AppNameSpace="appstore.exchange.autodesk.com"
                    OnlineDocumentation="www.autodesk.com"
                    OnlineDocumentationPtb="www.autodesk.com.br"
                    Author="ADN DevTech"
                    HelpFile="./Contents/Resources/helpENU.html"
                    HelpFilePtb="./Contents/Resources/helpPTB.html"
                    ProductCode=""
                    UpgradeCode="">
    <CompanyDetails Name="ADN DevTech"
                  Url="http://www.autodesk.com"
                  Email="email@autodesk.com" />
    <RuntimeRequirements OS="Win32|Win64"
                       Platform="AutoCAD" />
  <Components Description="MainDLL">
    <RuntimeRequirements OS="Win32|Win64"
                         Platform="AutoCAD"
                         SeriesMin="R19.0" SeriesMax="R19.1" />
    <ComponentEntry AppName="Main DLL" Version="1.0"
                    ModuleName="./Contents/Win/MainModule.enu.dll"
                    ModuleNamePtb="./Contents/Win/MainModule.ptb.dll"
                    AppDescription="This is the main module"
                    LoadOnCommandInvocation="True">
      <Commands>
        <Command
          LocalPtb="olaMundo"
          Global="helloWorld" />
      </Commands>
    </ComponentEntry>
  </Components>
</ApplicationPackage>
Finally the SupportedLocales markup will make sure the Exchange Store MSI is created for the desired languages (once the application is submitted).
The list of supported languages is (link):
Chs - Chinese Simplified (PRC)
Cht - Chinese Traditional (Taiwan)
Csy – Czech
Deu – German
Enu – English
Esp – Spanish
Fra – French
Hun – Hungarian
Ita – Italian
Jpn – Japanese
Kor – Korean
Plk – Polish
Ptb – Portuguese
Rus - Russian
You can find another article about this topic at this post.
Submit process
Once the application is ready, you can submit it to the store as usual. It will be evaluated by the Exchange Store team. The link will be the same (link), although not yet available.

## 评论

**内容**: JV said...
Please, in spanish is "HolaMundo"
Reply
05/16/2013 at 08:58 AM

---
**内容**: Augusto Goncalves said in reply to JV...
That's because I used Portuguese (PTB) on this post, so 'Olá Mundo' is how we say it around here :)
Thanks,
Augusto Goncalves
Reply
05/16/2013 at 09:19 AM

---
