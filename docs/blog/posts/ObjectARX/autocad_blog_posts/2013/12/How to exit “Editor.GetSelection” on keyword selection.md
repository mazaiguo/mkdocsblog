---
title: "How to exit “Editor.GetSelection” on keyword selection"
date: 2013-12-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Selection
description: "One way to exit the “GetSelection” API on keyword selection is to throw an AutoCAD exception from the keyword press event handler. Below is a sampl..."
author: Autodesk
---
# How to exit “Editor.GetSelection” on keyword selection

发布日期: 2013-12-01

原始链接: https://adndevblog.typepad.com/autocad/2013/12/how-to-exit-editorgetselection-on-keyword-selection.html

## 文章内容

By Virupaksha Aithal
One way to exit the “GetSelection” API on keyword selection is to throw an AutoCAD exception from the keyword press event handler. Below is a sample example of the procedure. On press of any keyword, below code throws the “Autodesk.AutoCAD.Runtime.ErrorStatus.OK” exception passing the keyword pressed. This exception is handled in the code to identify the keyword pressed.
[CommandMethod("SELKW")]
publicvoid GetSelectionWithKeywords()
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      // Create our options object
    PromptSelectionOptions pso = newPromptSelectionOptions();
      // Add our keywords
    pso.Keywords.Add("FIrst");
    pso.Keywords.Add("Second");
      // Set our prompts to include our keywords
    string kws = pso.Keywords.GetDisplayString(true);
    pso.MessageForAdding =
                "\nAdd objects to selection or " + kws;
    pso.MessageForRemoval =
            "\nRemove objects from selection or " + kws;
      pso.KeywordInput +=
           newSelectionTextInputEventHandler(pso_KeywordInput);
      PromptSelectionResult psr = null;
    try
    {
        psr = ed.GetSelection(pso);
          if (psr.Status == PromptStatus.OK)
        {
            //your logic
        }
    }
    catch (System.Exception ex)
    {
        if (ex is Autodesk.AutoCAD.Runtime.Exception)
        {
            Autodesk.AutoCAD.Runtime.Exception aEs =
                    ex as Autodesk.AutoCAD.Runtime.Exception;
              //user has pressed keyword.
              if (aEs.ErrorStatus ==
                        Autodesk.AutoCAD.Runtime.ErrorStatus.OK)
            {
                ed.WriteMessage("\nKeyword entered: {0}",
                                                     ex.Message);
            }
            else
            {
                //other exception, please handle
            }
        }
    }
  }
void pso_KeywordInput(object sender, SelectionTextInputEventArgs e)
{
    //user has pressed keyword, so throw Exception
    throw new Autodesk.AutoCAD.Runtime.Exception(
                Autodesk.AutoCAD.Runtime.ErrorStatus.OK, e.Input);
}
Posted at 01:37 AM in .NET, Virupaksha Aithal | Permalink

## 评论

**内容**: wpartist said...
It is really great !, Because this site is important which people every day show it & they are know many other things about exit keyword & Google keyword selection. I read this article & I hope it is help full to me & others traffic.
Reply
09/09/2014 at 01:19 AM

---
**内容**: CHRISTOPHER FUGITT said...
This is working out for me. The UI isn't going back to normal after throwing the exception. I loose the right click menu, the cursor doesn't go back to the pick box. I'm using AutoCAD Civil 3D 2016.
I guess I'll put a button on the screen to get there instead.
Reply
10/10/2017 at 12:49 PM

---
**内容**: swaywood said...
It is good, but after i select the entities, the commandline still show the keywords, i can also enter the keyword, it is not reasonable.
Maybe you can use GetEntity and GetPoint and GetCorner to simulate Getselection with keywords.
Reply
01/10/2018 at 03:31 AM

---
**内容**: Dani Regar said...
It is really great !, Because this site is important which people every day show it & they are know many other things about exit keyword & Google keyword selection. I read this article & I hope it is help full to me & others traffic
Reply
04/27/2018 at 03:42 PM

---
**内容**: today bepanah said...
Production: Cinevistaas
Bepanah full Star Cast: Jennifer Winget as Zoya female lead, Harshad Chopda as Aditya (male lead), Sehban Azim as Yash (Zoya’s husband), Namita Dubey as Pooja woh apna sa (Aditya’s wife), Aaryaa  BePanah Sharma as Zoya’s mother, Aanchal Goswami as Zoya’s sister, Shweta Ghulam as Anjana Hooda (Aditya’s mother), Rajesh Khattar as Aditya’s father, Vaishnavi Dhanraj, Iqbal Azad as Jennifer’s father
About Bepannaah serial on Colors
Bepannaah (Bepanha) is an upcoming show on Colors. The show will be a romantic drama and will feature popular TV actors Jennifer Winget (Beyhadh fame) and Harshad Chopda in lead roles. today Bepanah 
This marks Cinevistaas’ third collaboration with Jennifer after Dill Mill Gayye and Beyhadh, which is currently on air on Sony. The show was earlier titled as Adhura Alivda. Bepanah
UPDATE: Bepanah New Promo reveals shocking story line of Jennifer Winget’s new show
Harshad is mainly recognized for his role of Prem Juneja in Kis Desh Mein Hai Meraa Dil. Later he has worked in many popular daily soaps like Tere Liye, Dharampatni, Dil Se Di Dua-Saubhagyavati and many more. He was last seen in the series Humsafars on Sony TV. The actor made his Bollywood debut last year with The End, which was a failure at the box-office. Yeh Hai Chahatein
Reply
07/21/2018 at 11:39 AM

---
**内容**: Rubel Ahmed said...
Hello,
I’d like to edit the cookie opt-in checkbox text “Save my name, email, and website in this browser for the next time I comment.”
Basically I’d like to remove the word “website” as my comment post section does not have a Website field.
Any help is greatly appreciated.
See more article here

Thanks.
Reply
03/25/2019 at 09:14 AM

---
**内容**: Hiten Chaudhary said...
bahut khoob bhai. good job keep it up
Reply
03/12/2022 at 08:45 AM

---
**内容**: Vikram said...
Very informative and helpful thanks
Reply
08/10/2022 at 08:15 PM

---
**内容**: profilrr link said...
Thank you dear, I found your information really useful. I would like to say thanks once again for this information.
Keep posting all the new information.
https://profilrr.com/blog/>Free bio link generator
Reply
06/27/2023 at 04:38 AM

---
