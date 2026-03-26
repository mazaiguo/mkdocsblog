---
title: "How to Update the Status of External Process to AutoCAD CommandLine"
date: 2015-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Let us assume you have a .Net command that runs an external process that takes a long time to complete. While you are waiting for it to complete yo..."
author: Autodesk
---
# How to Update the Status of External Process to AutoCAD CommandLine

发布日期: 2015-08-01

原始链接: https://adndevblog.typepad.com/autocad/2015/08/how-to-update-the-status-of-external-process-to-autocad-commandline.html

## 文章内容

By Madhukar Moogala
Let us assume you have a .Net command that runs an external process that takes a long time to complete. While you are waiting for it to complete you can output a progress indicator to the command line :
Note: Following procedure works only .NET 4.5, as I’m incorporating await and aysnc methods.
[CommandMethod("TestCommand")]
static public void TestCommand()
{
Method1();
}
static public async void Method1()
{
try
{
var doc = Application.DocumentManager.MdiActiveDocument;
var ed = doc.Editor;
for (int i = 0; i < 20; i++)
{
ed.WriteMessage("Processing {0}...", i);
string result = await WaitASynchronously();
ed.WriteMessage("Done.\n");
}
}
catch (System.Exception ex)
{
Application.ShowAlertDialog("Error: " + ex.Message);
}
}
static public async Task<string> WaitASynchronously()
{
await Task.Delay(500);
return "Finished";
}

## 评论

**内容**: run 3 said...
There's a lot of useful stuff on the sharing site that everyone should check out; I do it regularly.
Reply
09/05/2022 at 02:00 AM

---
**内容**: hazel said...
Looking for a great app to watch movies on your Android device? Pikashow is a great option that offers a huge library of both classic and new releases. Best of all, it’s completely free to download and use!
Pikashow
Pikashow
Reply
07/19/2023 at 12:15 AM

---
**内容**: ella said...
Cryptocurrencies have revolutionized the financial landscape, offering a decentralized and secure method of conducting transactions. As the popularity of digital currencies continues to soar, cryptocurrency exchange platforms have become crucial for buying, selling, and managing these digital assets. One such prominent player in the market is Coinbase. In this article, we will explore the importance of Coinbase, how to download it, and its features, ensuring you embark on your crypto journey with confidence.
Coinbase App | Coinbase Download
Reply
07/24/2023 at 08:06 PM

---
**内容**: hazel jones said...

Explore essential accessories to enhance your Genyt usage. Find the perfect add-ons for an improved experience.
Get access to the latest movies on Filmywap. Learn how to download them for entertainment on the go.
genyt |
filmywap
Reply
09/14/2023 at 09:40 PM

---
**内容**: hazel jones said...
Get the best movie experience with 9kmovies. Download the latest films in HD quality today!
A detailed comparison of Filmyzilla with other movie download platforms. Find out which one suits your preferences.
9kmovies
filmyzilla
Reply
10/20/2023 at 05:55 AM

---
