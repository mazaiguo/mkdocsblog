---
title: "MLeader text that reflects MLeaderStyle settings"
date: 2015-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "Here is a short code snippet that creates an MLeader based on an existing MLeaderStyle. For the MLeader's text to correctly follow any changes made..."
author: Autodesk
---
# MLeader text that reflects MLeaderStyle settings

发布日期: 2015-11-01

原始链接: https://adndevblog.typepad.com/autocad/2015/11/mleader-text-that-reflects-mleaderstyle-settings.html

## 文章内容

By Balaji Ramamoorthy
Here is a short code snippet that creates an MLeader based on an existing MLeaderStyle. For the MLeader's text to correctly follow any changes made to the MLeaderStyle, it is necessary to clone the MLeaderStyle.DefaultText and use it as the MLeader's text. Creating a new MText without relying on the DefaultText can cause the text to not reflect any later changes that are made to the MLeaderStyle.
Thanks to Xin Xu from the AutoCAD engineering team for providing this tip.
[CommandMethod("MLTest")]
public void MLTestMethod()
{
    Editor ed = default(Editor);
    ed = Application.DocumentManager.MdiActiveDocument.Editor;

    PromptPointResult ppr1 = default(PromptPointResult);
    ppr1 = ed.GetPoint(
        new PromptPointOptions("Select start point"));

    if (ppr1.Status != PromptStatus.OK)
        return;

    PromptPointResult ppr2 = default(PromptPointResult);
    ppr2 = ed.GetPoint(
            new PromptPointOptions("Select end point"));
    if (ppr2.Status != PromptStatus.OK)
        return;

    Database db = HostApplicationServices.WorkingDatabase;

    ObjectId myMLeaderId = ObjectId.Null;
    using (Transaction trans 
                = db.TransactionManager.StartTransaction())
    {
        ObjectId myleaderStyleId = db.MLeaderstyle;
        MLeaderStyle mlstyle 
            = trans.GetObject(myleaderStyleId, 
                        OpenMode.ForRead) as MLeaderStyle;

        using (MLeader myMLeader = new MLeader())
        {
            myMLeader.SetDatabaseDefaults();
            myMLeader.PostMLeaderToDb(db);
            myMLeaderId = myMLeader.ObjectId;
            myMLeader.MLeaderStyle = db.MLeaderstyle;

            int leaderIndex = myMLeader.AddLeader();
            int leaderLineIndex 
                = myMLeader.AddLeaderLine(leaderIndex);
            myMLeader.AddFirstVertex(
                        leaderLineIndex, ppr1.Value);
            myMLeader.AddLastVertex(
                        leaderLineIndex, ppr2.Value);

            MText myMText 
                = mlstyle.DefaultMText.Clone() as MText;
            if (myMText != null)
            {
                myMText.SetContentsRtf("Autodesk");
                myMLeader.MText = myMText;
            }
        }
        trans.Commit();
    }
}

## 评论

**内容**: Kerry Brown said...
Hi Balaji,
Can you please explain why you use the default keyword when you declare the variables ?
Thanks,
Regards,
Reply
11/25/2015 at 09:40 AM

---
**内容**: Balaji said in reply to Kerry Brown...
Hi Kerry,
I had implemented the code in this blog post initially in VB.Net and later used an online converter to do the C# conversion for the sake of creating this blog post. The converter had introduced this and i did not notice it. Sorry, I do not know what that means. But, the C# version did build and run ok in AutoCAD.
Please do let me know if you have any information on it.
This is the converter that i had used for my VB.Net to C# conversion :
converter.telerik.com
Thanks
Balaji
Reply
11/25/2015 at 10:32 PM

---
**内容**: Kerry Brown said...
I didn't think it was needed initially, then it started to interest me because I decided this may be something new I needed to know.
I posted on the Swamp http://www.theswamp.org/index.php?topic=50511.msg556363#msg556363.
The consensus was that it was not necessary.
Thanks for your response.
And thank you particularly for your contributions to the learning pool.
Regards,
Reply
11/25/2015 at 11:28 PM

---
**内容**: Андрей Бушман said...
The working with each option of MLeaderStyle maybe is interesting too for some developers: http://bushman-andrey.blogspot.ru/2014/06/autocad_8823.html
Reply
11/26/2015 at 02:04 AM

---
**内容**: Balaji said in reply to Андрей Бушман...
Hi Андрей,
Thanks for sharing this nice blog post.
Regards,
Balaji
Reply
11/26/2015 at 10:12 PM

---
**内容**: backrooms game said...
I appreciate you sharing this good article piece.
Reply
09/18/2022 at 08:07 PM

---
**内容**: io games said...
The best blog ever is your post. Your post is interesting and interesting
Reply
09/27/2023 at 01:56 AM

---
