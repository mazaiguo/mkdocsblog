---
title: "Dissecting MTEXT Format Codes"
date: 2017-09-01
categories:
  - AutoCAD
tags:
  - Dimension
  - Unicode
description: "I have received a query how can I identify a special symbol from MTEXT content format string.To understand this better, we will look at a simple ex..."
author: Autodesk
---
# Dissecting MTEXT Format Codes

发布日期: 2017-09-01

原始链接: https://adndevblog.typepad.com/autocad/2017/09/dissecting-mtext-format-codes.html

## 文章内容

By Madhukar Moogala
I have received a query how can I identify a special symbol from MTEXT content format string.To understand this better, we will look at a simple example, below is a screen shot of Cylinder whose dimensions are expressed in
∅68
+0.8
+0.1
The format codes would be
\A1;\fAIGDT|b0|i0;\H2.5000;\ln\fArial|b0|i0;\H2.5000;68{\H1.3;\S+0,8^+0,1;}
Understanding each format code:
\f = Font file name, in this example it is AIGDT
AIGDT stands for Autodesk Inventor Geomertic Dimension and Tolerance font file.
codes starting with pipe are generally displays the traits of font.
b tells ‘bold’ where 0 is off,and 1 is on.
i tells ‘italic’ where 0 is off and 1 is on.
c tells ‘code page’ followed by code page number for example |c238
p  tells ‘pitch; followed by number for example |p10
\L    Start underline
\l    Stop underline
\O    Start overstrike
\o    Stop overstrike
\K    Start strike-through
\P    New paragraph (new line)
\pxi    Control codes for bullets, numbered paragraphs and columns
\X    Paragraph wrap on the dimension line (only in dimensions)
\Q    Slanting (obliquing) text by angle - e.g. \Q30;
\H    Text height - e.g. \H3x or \H2.500
\W    Text width - e.g. \W0.8x
\S     Stacking Fractions
e.g. \SA^B:
A
B
e.g. \SX/Y:
X
Y
e.g. \S1#4:
¼
\A   Alignment
\A0; = bottom
\A1; = center
\A2; = top
\C  Color change
\C1; = red
\C2; = yellow
\C3; = green
\C4; = cyan
\C5; = blue
\C6; = magenta
\C7; = white

\T  Tracking, char.spacing - e.g. \T2;
\~  Non-wrapping space, hard space
{}
Braces - define the text area influenced by the code
\  Escape character - e.g. \\ = "\", \{ = "{"


\fAIGDT|b0|i0;\H2.5000;\ln
'\l' is format code for lower underline, and from Font family AIGDT 'n' is special symbol for ∅.
Below is table of character mapping between control code and special symbol.
For example following format code
\A1;{\fAIGDT|b0|i0;m}\H2.5000;80
would render this

For character map utility, this document contains how to retrieve tool for various versions of windows.
http://sites.psu.edu/symbolcodes/windows/charmap/
MTEXT also supports straight away Unicode tool, and not all font files will support all symbols, every font files has its reason for existence but there will unique Unicode which prevents from clashing between symbols.
Using different font file like ISOCPEUR, I can render diameter symbol or ‘latin captial letter with diagonal stoke’, or the symbol which I have begin this post ∅, unicode is ‘\U+00D8’
{\fISOCPEUR|b0|i0|c0|p34;\H0.95833x;\C256;\U+00D8\A1;\H1.04348x;\C7;80}
Hope this helps, if you find any interesting format coding for font file, do let me know, I will keep updating this.

## 评论

**内容**: zouhair warii said...
thank you for this article
can you post more exemples
Reply
05/18/2020 at 08:39 AM

---
**内容**: Joe said...
Very useful article... definitely saving this.
Given the string:
\pi0.1122;Composite\P\pi0.33077;C01\P\pi0.28018;0,0,0\P\pi0.19922;000000\P\pi0.2822;white
How do I interpret the "\pi0.11222;"? I know that it is a centered mtext sub-string (because that's what I created), but don't see out to infer that from the dxf.
Can you offer any help?
Reply
02/02/2021 at 08:53 AM

---
