---
title: "Drag entities like Copy/Move"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Selection
description: "One of the solutions to drag entities like AutoCAD does is using the AcEd global function acedDragGen. It prompts the user to modify a selection se..."
author: Autodesk
---
# Drag entities like Copy/Move

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/drag-entities-like-copymove-1.html

## 文章内容

By Xiaodong Liang
One of the solutions to drag entities like AutoCAD does is using the AcEd global function acedDragGen. It prompts the user to modify a selection set by graphically dragging its entities. The method is defined as (from ObjectARX help) :
int acedDragGen(
    const ads_name ss, 
    const ACHAR * pmt, 
    int cursor, 
    int (*scnf) (ads_point pt, ads_matrix mt), 
    ads_point p
);
const ads_name ss
Selection set obtained by acedSSGet() or acedSSAdd()
const ACHAR * pmt
Optional prompt string that acedDragGen() displays before pausing for user input; for no prompt, pass a NULL pointer
int cursor
Form of cursor to display while the user drags the selection set (*scnf) (ads_point pt, ads_matrix mt) : Pointer to the function thatacedDragGen() calls whenever the user moves the cursor
ads_point p
Value of the cursor's final location after the user finishes dragging the selection set
  Only entities from the current drawing's model space and paper space can be manipulated by this function. It does not manipulate non-graphical objects or entities in other block definitions.
The scnf argument must be a pointer to a function whose declaration is compatible with the following: 
int sample_fcn( ads_point pt, ads_matrix mt);
  This function specifies a transformation that acedDragGen() applies to the selection set. The acedDragGen() function calls it every time the user moves the cursor. The first argument, pt, is the current cursor location represented in the entity coordinate system that corresponds to the current UCS. The function should not modify pt. The second, mt, is a 4(4 transformation matrix. The scnf function can transform the selected entities by modifying this matrix, which acedDragGen() then applies to the selection set. By passing the same matrix to acedGrVecs(), you can display vectors that are transformed in the same way as the selection set. This can be useful when the selection set is large and would take a long time to regenerate.
Following is a code demo. It also shows how to if you want to control the display mode of the original entities while dragging.
  // Global, so it can be used in the
// DragGen callback function...
ads_point basePt;
static void myDrag()
{
     ads_name ss;  
     // Get the Selection Set
     acedSSGet(NULL,NULL,NULL,NULL,ss);
     // Base Point for Moving...
     acedGetPoint(NULL,
                  L"Select Base Point",
                   basePt);
     long len;
     acedSSLength(ss,&len);
        // if you want to control the display mode of
     // the ORIGINAL entities while draging
     //for(int c=0;c<len;c++)
     //{
     //     ads_name ent;
     //     acedSSName(ss,c,ent);                   
     //     e.g. hide the original entities
     //     acedRedraw(ent,2); 
     // mode:
     //1  Redraw entity 
    // 2  Undraw entity (blank it out) 
    // 3  Highlight entity 
    // 4  Unhighlight entity 
     //}
       //Value of the cursor's final location
      //after the user finishes
     // dragging the selection set 
     ads_point final_pt;
       // Call DragGen with the callback function
     acedDragGen(ss,
                 L"Drag Me Around",
                 0,
                 dragGenCallback,
                  final_pt);
       //restore the mode of original entities
     //for(int c=0;c<len;c++)
     //{
     //     ads_name ent;
     //     acedSSName(ss,c,ent);          
     //     acedRedraw(ent,1);
     //}
       // get the final matirx and do your work
     // such as copy or move
     // with the value of final_pt 
} 
  // Here is the callback...
static int dragGenCallback(ads_point pt,ads_matrix mt)
{
     AcGeVector3d vec(pt[0]-basePt[0],pt[1]-basePt[1],pt[2]-basePt[2]);
     AcGeMatrix3d mat;
     // Set our matrix to translate the mouse movements...
     mat.setToTranslation(vec);
     // And place the results in mt
     for(int c=0;c<4;c++)
     {
          for(int cd=0;cd<4;cd++)
          mt[c][cd]=mat(c,cd);
     }
     return RTNORM;
}
The sample of .NET is available at:
http://through-the-interface.typepad.com/through_the_interface/2010/06/allowing-interactive-dragging-of-a-selection-of-autocad-objects-using-net.html

