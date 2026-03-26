---
title: "Custom code snippet on Visual Studio"
date: 2015-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Database
  - Unicode
description: "Today’s post is focused on productivity, an aspect that is sometimes left behind due our intense work load…And I believe that small improvements ca..."
author: Autodesk
---
# Custom code snippet on Visual Studio

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/custom-code-snippet-on-visual-studio.html

## 文章内容

By Augusto Goncalves
Today’s post is focused on productivity, an aspect that is sometimes left behind due our intense work load…And I believe that small improvements can make a huge difference on our daily work.
Now the idea is to save us some time typing a new command for AutoCAD, that includes, for instance, database, editor and transaction. Sure you can adjust the code.
How make this work? Simple:
Create a .snippet file using any text editor (Notepad can do the trick).
Copy & paste the XML content below
Save at [My Documents]\Visual Studio 2012\Code Snippets\Visual C#\My Code Snippets\ folder, or other version that you have.
At your Visual Studio code, type AcadCmd and press TAB, the code should appear, press TAB again to move between command name and method name, both marked in yellow.
Like it? You may adjust to other commands or other pieces that you use repeatedly. Here is the .snippet for
download.
<?xml version="1.0" encoding="utf-8" ?>
<CodeSnippets xmlns="http://schemas.microsoft.com/VisualStudio/2008/CodeSnippet">
  <CodeSnippet Format="1.0.0">
    <Header>
      <Title>AutoCAD Command</Title>
      <Shortcut>AcadCmd</Shortcut>
      <Description>Code snippet for AutoCAD command method with transaction</Description>
      <SnippetTypes>
        <SnippetType>Expansion</SnippetType>
      </SnippetTypes>
    </Header>
    <Snippet>
      <Declarations>
        <Literal>
          <ID>COMMAND_NAME</ID>
          <ToolTip>Replace with the command name</ToolTip>
          <Default>myCommandName</Default>
        </Literal>
        <Object>
          <ID>METHOD_NAME</ID>
          <ToolTip>Replace with the method name</ToolTip>
          <Default>myMethodName</Default>
        </Object>
      </Declarations>
      <Code Language="CSharp">
        <![CDATA[
        [CommandMethod("$COMMAND_NAME$")]
        public static void $METHOD_NAME$()
        {
            Database db = Application.DocumentManager.MdiActiveDocument.Database;
            Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
            using (Transaction trans = db.TransactionManager.StartTransaction())
            { 
 
            }
        }
        ]]>
      </Code>
    </Snippet>
  </CodeSnippet>
</CodeSnippets>

## 评论

**内容**: KHill said...
Could you please post a link to download the entire XML code? The formatting trimmed off the content so it's not all there to be copied.
Thanks
Reply
05/08/2015 at 07:35 AM

---
**内容**: Augusto Goncalves said in reply to KHill...
Sorry about that, I tested here and could select, copy & paste the whole XML code...
Anyway, updated the post to include the download link, thanks!
Regards,
Augusto Goncalves
Reply
05/08/2015 at 07:39 AM

---
**内容**: Gdiael Barros said...
Congratulations for such a nice and usefull blog post.
There are a plugin to assist the snippet desing process:
https://visualstudiogallery.msdn.microsoft.com/B08B0375-139E-41D7-AF9B-FAEE50F68392
Reply
05/08/2015 at 12:53 PM

---
**内容**: Augusto Goncalves said in reply to Gdiael Barros...
Interesting! Thanks for sharing!
Reply
05/08/2015 at 12:56 PM

---
**内容**: rafrbu said...
And not to forget: trans.Commit();
Reply
05/14/2015 at 09:25 AM

---
**内容**: Augusto Goncalves said in reply to rafrbu...
Indeed, good point! :-)
Reply
05/14/2015 at 09:31 AM

---
