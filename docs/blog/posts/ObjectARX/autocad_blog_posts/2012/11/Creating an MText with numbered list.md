---
title: "Creating an MText with numbered list"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - Database
  - Unicode
description: "Here is a sample code to create an MText that has its content set to a numbered list."
author: Autodesk
---
# Creating an MText with numbered list

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/creating-an-mtext-with-numbered-list.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create an MText that has its content set to a numbered list.
[CommandMethod("MTextNumberedList")]
public void CreateMTextNumberedList()
{
    Database db = Application.DocumentManager.MdiActiveDocument.Database;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord ms = tr.GetObject
            (
                SymbolUtilityServices.GetBlockModelSpaceId(db),
                OpenMode.ForWrite
            ) as BlockTableRecord;
          MText mText = new MText();
        mText.SetDatabaseDefaults();
          String rtfContents = @"{\pntext\f0 1.\tab}First Line\par{\pntext\f0 2.\tab}Second Line\par}";
        mText.SetContentsRtf(rtfContents);
        mText.Location = Point3d.Origin;
          ms.AppendEntity(mText);
        tr.AddNewlyCreatedDBObject(mText, true);
          tr.Commit();
    }
}

## 评论

**内容**: Heinz said...
What is wrong here
Was ist hier falsch
public [u]void[/u] CreateMTextNumberedList()
MText mText = [u]new MText[/u]();
Reply
11/11/2012 at 12:28 AM

---
**内容**: Heinz said...
addendum
these 2 items I get an error message
Nachtrag
bei diesen 2 Einträgen bekomme ich einen Fehlermeldung
Reply
11/11/2012 at 09:25 PM

---
**内容**: Heinz said in reply to Heinz...
danke für keine antwort
Reply
11/15/2012 at 01:14 AM

---
**内容**: Balaji said...
Hi Heinz,
Sorry for the delay.
Can you please post the full code for me to reproduce the error ?
Reply
11/15/2012 at 02:06 AM

---
**内容**: Heinz said...
The code you see above in it.
Der Code seht oben drin.
[ CommandMethod ( "MTextNumberedList" )]

--void-- because the error message is because what I have to reload
but what
Reply
11/15/2012 at 05:30 AM

---
**内容**: Madhukar Moogala said in reply to Heinz...
Hi Heinz,
Its difficult to understand your question. What do you mean by "because the error message is because what I have to reload"?
Perhaps you could tell us what error message you're actually seeing, and we may be able to point you in the right direction.
If I had to guess, it would be that you're new to AutoCAD .NET development, and don't realize that the code snippets we post on this blog generally don't include the 'standard' namespace imports needed to use the AutoCAD API. You can find information on that in the training material and tutorials posted to www.autodesk.com/developautocad.
Reply
11/19/2012 at 09:26 AM

---
**内容**: osk said...
me gustaria tener esta informacion pero en idioma español latnoamericano, como se debe hacer...
Reply
11/28/2012 at 06:29 AM

---
**内容**: Kerry Brown said in reply to osk...
[quote] .. as it should be [/quote]
thanks for the giggle :)
Reply
11/28/2012 at 05:35 PM

---
**内容**: laddie said...
Balaji,
Can you shed any light on how to apply formatting to the numbered list? Specifically I would like to have each numbered section maintain a hanging indent. I am using vb.net.
Thank you in advance.
Reply
04/26/2013 at 10:32 AM

---
**内容**: Balaji said in reply to laddie...
Hi Laddie,
Can you please send me a screenshot to show the kind of formatting that you want for the numbered list ? Were you able to do that using the AutoCAD UI for an MText ?
You can send me the screenshot image to balaji.ramamoorthy@autodesk.com
This will help me try and find a way to do that using the API.
Thank you.
Reply
04/29/2013 at 02:57 AM

---
**内容**: Balaji said in reply to laddie...
Thanks for sharing the screenshot.
Here is a sample rtf content for creating an MText with hanging indent.
myMtext.SetContentsRtf(@"{{\pard\li2160\fi480\pntext\f0 1.\tab}Autodesk \par {\pard\li2160\fi480 \tab Inc} \par {\pard\li2160\fi480\pntext\f0 2.\tab}Developer \par {\pard\li2160\fi480 \tab Technical} \par {\pard\li2160\fi480 \tab Services} }");
Regards,
Balaji
Reply
04/29/2013 at 11:16 AM

---
**内容**: laddie said in reply to Balaji...
TypePad HTML Email
Thank you Balaji. I am very pleasantly surprised at your helpfulness. I will give this code a try. Thank you Laddie 
Reply
04/29/2013 at 11:19 AM

---
**内容**: laddie said...
Balaji,
Thank you for this example code. Based on this code, the line breaks are controlled at a specific word. What I am trying to accomplish is an MTEXT entity that wraps based on the width I provide programatically. The code I am attaching along with a sub routine written to create annotative mtext produces a numbered list that allows the user to add to the entity (hitting enter adds line with next number). The wrap is controlled by a variable passed to the sub routine controlling the width of the MTEXT. The routine successfully creates the numbered list, however the second, third etc. lines in each numbered subsection do not line up with the text on the first line. Instead they fall below the number on the first line. I hope I have explained this clearly. Thank you again for your help.
Dim textstring2 As String = "NOTES:" & vbCrLf & "\par{\f0 1.\tab}NUMBERED SECTION 1 TEXT HERE.\par{\f0 2.\tab}SECTION 2 TEXT HERE.\par}"
Reply
05/03/2013 at 05:35 AM

---
