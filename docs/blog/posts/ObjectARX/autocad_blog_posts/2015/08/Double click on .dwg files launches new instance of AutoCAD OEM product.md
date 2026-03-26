---
title: "Double click on .dwg files launches new instance of AutoCAD OEM product"
date: 2015-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - OEM
description: "When a drawing file is opened via the explorer by double clicking on it, the application associated with that file type is launched automatically. ..."
author: Autodesk
---
# Double click on .dwg files launches new instance of AutoCAD OEM product

发布日期: 2015-08-01

原始链接: https://adndevblog.typepad.com/autocad/2015/08/double-click-on-dwg-files-launches-new-instance-of-autocad-oem-product.html

## 文章内容

By Balaji Ramamoorthy
When a drawing file is opened via the explorer by double clicking on it, the application associated with that file type is launched automatically. If you notice that separate instances of the AutoCAD or AutoCAD OEM product gets launched on double clicking two separate drawings, here are two likely reasons and ways to set it right.
1. In the explorer, right click on a .dwg file and choose "Properties". In the "General" tab, the application that the .dwg file will open is displayed as shown in the below screenshot. If an application such as your AutoCAD OEM product or a specific version of AutoCAD is chosen, then a new instance will be launched on double click. Instead, try choosing the "AutoCAD DWG Launcher" as the application by clicking on the "Change" button.
2. In some systems, it is also possible that despite choosing the "AutoCAD DWG Launcher", separate instances get launched on double clicking two different drawings. This is likely because of the improper association of the .dwg file type and the application. To set it right, you may need to tweak the registry values but please ensure that you have a backup of the registry keys that you modify in this process.
- Delete the "HKEY_CLASSES_ROOT\.dwg". This will ensure that there are no applications associated with the .dwg file type.
- Under "HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps", delete the AutoCAD OEM product entry in case it is already listed. The entries under apps are the ones that launcher application will use to open a .dwg file. The default application that the launcher will use is listed under HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps -> Default key.
For example, here is the value that was removed for an OEM product
- Launch the AutoCAD / AutoCAD OEM product and at startup, the DWG association dialog should get displayed. Choose the recommended option which is "Always reassociate DWG files with <Product name>".
- Close AutoCAD / AutoCAD OEM product. The double clicking on two separate .dwg files should not get opened in the same instance of the application. You can also verify that DWG file association is right under HKEY_CURRENT_USER\Software\Autodesk\DwgCommon\shellex\apps -> Default key.

## 评论

**内容**: Timbot said...
we also had to remove the .dwg key from HKEY_CURRENT_USER\Software\Classes\.dwg to get it to work properly
Reply
08/19/2015 at 01:45 PM

---
**内容**: Dominik_CADT said...
Hi. we have the same problem but when we do that then the OEM will open the first DWG 2 times.
What can we do by this issue?
Thanks,
Reply
06/13/2016 at 02:27 AM

---
**内容**: Ramakrishnan said...
Thanks for sharing such important information. It is very useful. I hope you will come up with more informative blogs in future.
Reply
05/18/2018 at 10:09 PM

---
**内容**: fateme hadi said...
Hi. I have a dwg file that when i want to open it, this eror is displayed; drawing file is not valid!!! I turned off my sistem, while my file was open. After that this problem was occured. please guide me
Reply
01/16/2019 at 02:38 PM

---
**内容**: Arshad said...
Thanks A lot For Sharing such a important information i was looking for this from so many days finally i have the good and correct answer highly appreciated....cheers
Reply
12/08/2019 at 01:56 AM

---
**内容**: Gusmuh said...
Thank you! This was a huge help!
Reply
01/02/2020 at 03:35 PM

---
**内容**: Rohit said...
Hleped a lot Thanks
Reply
07/09/2020 at 10:20 PM

---
**内容**: Bhagyashri Kadam said...
This Is Most Useful And Give More Knowledge For Me And Let Me Share It For Alot Of People. And Dont Forget Ti Visit Me Back
Click Here For Visit My Site thanks .
Reply
05/18/2021 at 02:27 AM

---
**内容**: cookie clicker 2 said...
Thanks for sharing!
Reply
09/24/2021 at 03:30 AM

---
**内容**: flagle said...
For me this was a huge help!
Reply
09/18/2022 at 08:04 PM

---
**内容**: df said...
it's help me alot. love it
moto x3m
Reply
11/27/2022 at 06:41 PM

---
**内容**: gawes83833 said...
This is a cockfight-related betting site that is legal in various countries of the world including the Philippines. This virtual gaming site is quite popular among people. The WPC2029 updates are regularly given on the WPC 2029 Facebook page.
https://www.webtechmantra.com/wpc2029/”>wpc2029
Reply
03/08/2023 at 11:50 PM

---
**内容**: gawes83833 said...
This is a cockfight-related betting site that is legal in various countries of the world including the Philippines. This virtual gaming site is quite popular among people. The WPC2029 updates are regularly given on the WPC 2029 Facebook page.
https://www.webtechmantra.com/wpc2029/
Reply
03/08/2023 at 11:50 PM

---
**内容**: vinod032 said...
Additionally, packaged goods are often accompanied by clear labeling and product information, making it easy for consumers to identify the contents and make informed purchasing decisions.
Reply
03/17/2023 at 02:09 AM

---
**内容**: kivekif180 said...
Overall, while genyoutube download wallpaper can be a useful tool for downloading videos from YouTube, it's important to be mindful of copyright laws and respect the intellectual property of others. Additionally, when downloading wallpapers, it's best to use a dedicated wallpaper application or website to ensure high-quality and appropriate content.
https://www.webtechmantra.com/genyoutube/
Reply
03/17/2023 at 10:41 AM

---
**内容**: ReddyShivatmika said...
In today’s article, we will provide you with the complete procedure to view the login report ab-hwc.nhp.gov.in along with information about AB HWC Portal Daily Entry.
Reply
03/20/2023 at 01:11 AM

---
**内容**: pavola7287 said...
In addition to the standard login system, OnPassive also offers two-factor authentication (2FA) for added security. With 2FA, users need to enter a code sent to their mobile device to access their account. This adds an extra layer of security and helps to prevent unauthorized access to your account. In conclusion.
https://www.webtechmantra.com/onpassive-login/
Reply
03/23/2023 at 12:55 AM

---
**内容**: loh adif255 said...
The picme login program sends timely alerts and reminders to pregnant women and healthcare providers about upcoming appointments and vaccination schedules. This ensures that pregnant women receive timely care and vaccinations.
https://www.webtechmantra.com/picme/
Reply
04/25/2023 at 02:21 AM

---
**内容**: Beredo9847 said...
snapchat saver is an app designed to help users save their favorite Snapchat content without alerting the sender.
https://www.flipupdates.com/best-snapchat-saver-apps/
Reply
04/27/2023 at 10:09 PM

---
**内容**: Hocive2988 said...
ysl black opium dossier.co The luxurious and sophisticated fragrance designed for women, exudes an aura that is synonymous with opulence.
https://www.flipupdates.com/ysl-black-opium-dossier-co/
Reply
04/28/2023 at 12:02 AM

---
**内容**: reticeg358 said...
Rapipay Fintech Private Limited was officially established on April 6th, 2009 in the city of Delhi and registered as a privately-owned fintech company. It offers an online payment platform that helps businesses securely and conveniently accept customer payments. It allows customers to pay using their preferred payment methods, including credit/debit cards, net banking, UPI, IMPS, and wallets.
https://www.webtechmantra.com/rapipay-crm-login/
Reply
04/28/2023 at 01:35 AM

---
**内容**: reticeg358 said...
TAFCOP is a new platform, which means Telecom Analytics for Fraud Management and Consumer Protection. It is launched by DoT (Department of Telecom) that allows customers to scrutinize and inspect all mobile SIM numbers that are registered with their UID (Aadhaar Cards) in India.

https://www.webtechmantra.com/tafcop/
Reply
05/05/2023 at 03:45 AM

---
**内容**: Moxetob806 said...
In the current digital era, Instagram has gained immense popularity as a social media platform to share personal experiences, stories, and photos. Specifically, an instagram bio for girls presents an excellent opportunity to express their personality and highlight their individuality. It serves as a platform to showcase their passions, personality, and unique qualities, and ultimately, to exhibit who they are.
https://www.flipupdates.com/instagram-bio/
Reply
05/10/2023 at 10:31 PM

---
**内容**: Mekawey186 said...
gmr transcription has a team of highly skilled and experienced transcriptionists who are proficient in transcribing audio and video content. They can handle a wide range of transcription projects, including business meetings, interviews, academic research, legal proceedings, medical dictations, and more.
For More Information : https://www.flipupdates.com/gmr-transcription/
Reply
06/06/2023 at 12:41 AM

---
**内容**: Wordle answer today said...
Your article is incredibly informative and intriguing. I am seeking this type of post.
Reply
06/06/2023 at 09:07 PM

---
