---
title: "Converting C# to Java – An Experiment (Part 3)"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
description: "In part 1 of this series I created a simple task list prioritization tool for AutoCAD written in C#. This was based on two classes: Item and Priori..."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 3)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-c-to-java-an-experiment-part-3.html

## 文章内容

By Stephen Preston
In part 1 of this series I created a simple task list prioritization tool for AutoCAD written in C#. This was based on two classes: Item and PrioritizerCore.
In part 2, I setup an Android app project in Eclipse, and migrated my Item class from C# to Java, discovering how very similar the two languages are.
Today, I'll migrate the PrioritizerCore class. (As for the Item class, the goal today is to get the code to compile in Eclipse - we'll check the logic still works when we hook the classes into a working Android app).
We'd already copied the PrioritizerCore C# code into a PrioritizerCore.java file in our Android project, so we can just jump in and start editing. Before making additional changes, we'll go through the code and make the same edits as we did for Item without further comment:
Change string to String and bool to boolean.
Change LIst to ArrayList.
Change the Serializable attibute to the Java Serializable interface.
Change properties to get/set methods, and change calls to properties in the same way.
Change all function names to start with a lowercase character instead of uppercase.
USe intellisense to reference missing packages.
 That removes the vast majority of compilation errors. Those that remain are new.
The first new error we encounter is the foreach loop - which is really handy for iterating the elements of a collection. The C# code looks like this:
      foreach (Item i in m_ItemList)
Java has an equivalent, but the syntax is slightly different. We change that line to:
      for (Item i : m_ItemList)
which I really like - its even more succinct than the C# :-).
The next error is:
  public void sort()
  {
    m_ItemList.sort(new ItemComparer());
  }
Again Java has an equivalent of the sort method and the equivalent of a Comparator. We change our code to:
  public void sort()
  {
    Collections.sort(m_ItemList, new ItemComparer());
  }
As you'd expect, the next error is in our custom comparator definition. We change 
  private class ItemComparer : IComparer<Item>
to
  private class ItemComparer implements Comparator<Item>
  And that's it. No more errors.PrioritizerCore.java now looks like this:
  package Preston.Stephen.Prioritizer;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;


//PrioritizerCore  is responsible for handling the list of Items.
//[Serializable()]
public class PrioritizerCore implements Serializable
{

  private static final long serialVersionUID = 1L;
  private ArrayList<Item> m_ItemList;

  //Constructor
  public PrioritizerCore()
  {
    m_ItemList = new ArrayList<Item>();
  }

  //Adds a new Item to the list 
  // but only if the name (ItemText) is unique
  public boolean addItem(String strItemText)
  {
    Item tmpItem = new Item();
    tmpItem.setItemText(strItemText);
    if (m_ItemList.contains(tmpItem))
      return false;

    m_ItemList.add(tmpItem);
    return true;
  }


  //Returns Item at position 'index' in list.
  //Returns null if index is outside list bounds.
  public  Item getAtIndex(int index)
  {
    if (index >= 0 & index < m_ItemList.size())
    {
      return m_ItemList.get(index);
    }
    else
    {
      return null;
    }
  }

  //Clears the list
  public void reset()
  {
    m_ItemList.clear();
  }

  //Read-only property
  //Returns number of items in the list
  public  int getItemCount()
  {
    return m_ItemList.size();
  }


  //Returns true if any priorities have been set in list
  //(Which also means there must be at least two items in the list)
  public boolean hasPriorities()
  {
      for (Item i : m_ItemList)
      {
        if (i.getScore() > 0)
        {
          return true;
        }
      }
      return false;
  }


  //Sort list - highest priority Item first
  //If Priorities are equal, sort in ascending alphabetical order
  public void sort()
  {
    Collections.sort(m_ItemList, new ItemComparer());
  }

  //Sort in order of descending Score. 
  //If Result is same, sort on ascending Text.
  private class ItemComparer implements Comparator<Item>
  {
    public int compare(Item x, Item y)
    {
      //If items have same prioritization score, use prioritization
      // between the two items to sort. If that doesn't work, sort
      // alphanumerically on ItemText.
      if (x.getScore() == y.getScore())
      {

        if (x.IsBetterThan(y))
        {
          return -1;
        }
        else if (y.IsBetterThan(x))
        {
          return 1;
        }
        else
        {
          return x.getItemText().compareTo(y.getItemText());
        }
      }

      //If items have different priority scores, then sort on that.
      if (x.getScore() > y.getScore())
        return -1;
      //if (x.iResult < y.iResult) - the only option left
      return 1;
    }
  }
}
  Here's a summary of the migration issues we found today:
Java has a 'foreach' equivalent - for (Item i : m_ItemList).
The Java 'sort' method is a static method of the Collection class instead of an instance method of a specific collection.
The Java equivalent of the C# IComparer interface is IComparator (which I believe is more grammatically correct :-).
Next time we'll hook the PrioritizerCore and Item classes into a simple Android Activity, so we can display a list of Items in an Android ListView.
_______________________________
Credit where its due:
I'm using Java2HTML (as advertised by Kean Walmsley) to copy the formatted code in Eclipse into my blog posts.
This C# to Java comparison cheat sheet was very helpful when working out how to migrate my code.

