---
title: "Converting C# to Java – An Experiment (Part 1)"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Forge
  - Plugin
description: "Yesterday, in a rather roundabout way, I introduced you to my personal investigation (as a Java newbie) into how easy it is to convert existing C# ..."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 1)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-c-to-java-an-experiment-part-1.html

## 文章内容

By Stephen Preston
Yesterday, in a rather roundabout way, I introduced you to my personal investigation (as a Java newbie) into how easy it is to convert existing C# code to Java. I’ve already explained that the hardest part for me was polishing up my C# skills (I keep forgetting the semicolons and curly brackets). My plan was to write a relatively (but not too) simple AutoCAD C# plug-in, convert the basic business logic to Java, and then embed that in an Android app. I wanted this exercise to be about the C# and the Java. Therefore, I deliberately stuck to a non-graphical application, so I didn’t have to start learning additional graphics libraries. I decided on a simple commandline binary prioritization helper plug-in.
In this post, I’ll show you the C# and give you a working AutoCAD plug-in.
The idea of binary prioritization (or comparison) is to prioritize a list by comparing each item in the list against every other item in the list. The item that you prefer the most after summing all your comparisons is the most important item. Its an obvious tool for a programmer . To demonstrate, here’s a simple example -
I’ve just moved house, and I have along list of tasks I need to do to. Here is a small part of my ToDo list:
Fix the roof (before the winter rain comes)
Paint the spare bedroom (because we can’t assemble our bookcases until we’ve painted)
Paint the house exterior (before the winter rain comes)
Dig up the lawn (to plant a vegetable garden)
Build a fence (to stop our chickens – which we haven’t bought yet - escaping)
In my binary comparison, I record the answers to the following questions:
Q. Which is more important – ‘fix the roof’ or ‘paint the spare bedroom’?
A. The rain probably won’t come until November, but I can’t unpack all my books until the spare bedroom is painted, so painting the room is more important.
Q. Which is more important – ‘fix the roof’ or ‘paint the house exterior’?
A. The painting could probably wait another year at a pinch, so fixing the roof is more important.
Q. Which is more important – ‘fix the roof’ or ‘dig up the lawn’?
A. Urban homesteading can wait, the rain won’t – fixing the roof is more important.
Etc.
Etc.
I keep doing this until I’ve compared every item with every other item. I then find that I chose each item the following number of times:
Paint the spare bedroom : 4
Fix the roof : 3
Paint the house exterior : 2
Build a fence : 1
Dig up the lawn : 0
And that’s my prioritized task list. Off I go to buy some paint brushes and VOC-free paint.
So now for my C# code. Bear in mind that this is something I cobbled together quickly. Its definitely not a style guide, and the usual health warnings apply (e.g. error handling is left as an exercise for the reader ). I should also point out that the only Java I’d written before running this experiment was a simple Hello World Android app – there was no attempt to write the C# in a migration friendly way, except that I made a little effort to keep some separation between my UI and business logic.
Here is the core logic for the application – the Item class representing an item in the list I want to prioritize, and the PrioritizerCore class which is basically a List with a few helper functions:
using System;
using System.Collections.Generic;
  namespace Prioritizer
{
  //Item class stores info on each item that you want to prioritize
  //Implements IEquatable interface so we can use this class with
  // a custom comparator - see PrioritizerCore.Sort() method.
  [Serializable()]
  public class Item : IEquatable<Item>
  {
    //The text describing this Item - also used to ensure uniqueness
    private string m_strItemText;
    //The list of Items this Item is more important than
    private List<Item> m_BetterThanList;
      //Constructor
    public Item()
    {
      m_BetterThanList = new List<Item>();
    }
      //Implement IEquatable<Item>::Equals
    //For our  purposes, Items are equal if their names match
    public  bool Equals(Item other)
    {
      //A null item isn't equal this this
      if (other == null)
        return false;
        //Items are equal if their names match
      if (this.m_strItemText == other.m_strItemText)
        return true;
        //Otherwise, Items are not equal
      return false;
    }
      //Read-write property
    //The name of this Item
    public string ItemText
    {
      get { return m_strItemText; }
      set { m_strItemText = value; }
    }
      //Read-only property
    //Number of Items this Item is rated higher than
    // in binary comparisons
    public int Score
    {
      get { return m_BetterThanList.Count; }
    }
      //Returns true if item successfully added
    //Returns false if item was already in the list, or we try to add
    // an Item to its own BetterThanList
    public bool AddBetterThanItem(Item anItem)
    {
      if (anItem == this)
        return false;
        if (this.IsBetterThan(anItem))
      {
        return false;
      }
      else
      {
        m_BetterThanList.Add(anItem);
        //If anItem had already been selected as better than this Item
        // then we remove this Item from anItem's BetterThan list
        if (anItem.IsBetterThan(this))
        {
          anItem.Remove(this);
        }
        return true;
      }
    }
      //Returns true if this Item is better than the supplied Item
    public bool IsBetterThan(Item anItem)
    {
      return m_BetterThanList.Contains(anItem);
    }
      //Removes an Item from the list
    //Returns true if successful, false if Item wasn't in list
    public bool Remove(Item anItem)
    {
      return m_BetterThanList.Remove(anItem);
    }
      //Returns Item at position 'index' in this Item's BetterThanList
    //Returns null if index is outside list bounds
    public Item GetBetterThanItem(int index)
    {
      if (index >= 0 & index < m_BetterThanList.Count)
      {
        return m_BetterThanList[index];
      }
      else
      {
        return null;
      }
    }
  }
      //PrioritizerCore  is responsible for handling the list of Items.
  [Serializable()]
  public class PrioritizerCore
  {
      private List<Item> m_ItemList;
      //Constructor
    public PrioritizerCore()
    {
      m_ItemList = new List<Item>();
    }
      //Adds a new Item to the list
    // but only if the name (ItemText) is unique
    public bool AddItem(string strItemText)
    {
      Item tmpItem = new Item();
      tmpItem.ItemText = strItemText;
      if (m_ItemList.Contains(tmpItem))
        return false;
        m_ItemList.Add(tmpItem);
      return true;
    }
        //Returns Item at position 'index' in list.
    //Returns null if index is outside list bounds.
    public  Item getAtIndex(int index)
    {
      if (index >= 0 & index < m_ItemList.Count)
      {
        return m_ItemList[index];
      }
      else
      {
        return null;
      }
    }
      //Clears the list
    public void Reset()
    {
      m_ItemList.Clear();
    }
      //Read-only property
    //Returns number of items in the list
    public  int ItemCount
    {
      get { return m_ItemList.Count; }
    }
        //Returns true if any priorities have been set in list
    //(Which also means there must be at least two items in the list)
    public bool HasPriorities
    {
      get
      {
        foreach (Item i in m_ItemList)
        {
          if (i.Score > 0)
          {
            return true;
          }
        }
        return false;
      }
    }
        //Sort list - highest priority Item first
    //If Priorities are equal, sort in ascending alphabetical order
    public void Sort()
    {
      m_ItemList.Sort(new ItemComparer());
    }
      //Sort in order of descending Score.
    //If Result is same, sort on ascending Text.
    private class ItemComparer : IComparer<Item>
    {
      public int Compare(Item x, Item y)
      {
        //If items have same prioritization score, use prioritization
        // between the two items to sort. If that doesn't work, sort
        // alphanumerically on ItemText.
        if (x.Score == y.Score)
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
            return x.ItemText.CompareTo(y.ItemText);
          }
        }
          //If items have different priority scores, then sort on that.
        if (x.Score > y.Score)
          return -1;
        //if (x.iResult < y.iResult) - the only option left
        return 1;
      }
    }
  }
  }
I kept the UI separate so I could more easily port the above code to Java and then bolt on my Android UI later (which, of course, is completely different from the AutoCAD UI). Here is the AutoCAD part of the code (written for AutoCAD 2012):
using System;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
  // This line is not mandatory, but improves loading performances
[assembly: CommandClass(typeof(Prioritizer.MyCommands))]
  namespace Prioritizer
{
  //Our command class.
  //We're not using static methods/variables,
  // so this class is 'per document'
  public class MyCommands
  {
    private PrioritizerCore m_Prioritizer;
      //Constructor
    public MyCommands()
    {
      Init();
    }
      //Initialize everything
    private void Init()
    {
      // Put your command code here
      if (null == m_Prioritizer)
      {
        m_Prioritizer = new PrioritizerCore();
      }
    }
      //Keep asking user to add items until they cancel command or
    // enter null string
    [CommandMethod("AddItems")]
    public  void AddItems()
    {
      while (InputListItem());
    }
      //Loops through all priorities, asking user to make binary choice
    // for each unique pair.
    [CommandMethod("AddPriorities")]
    public void AddPriorities()
    {
      //Can't prioritize unless we have at least two Items
      if (m_Prioritizer.ItemCount < 2)
      {
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        ed.WriteMessage("\nRun AddItems command before setting priorities.");
        return;
      }
      for (int i = 0; i < m_Prioritizer.ItemCount; i++)
      {
        for (int j = i + 1; j < m_Prioritizer.ItemCount; j++)
        {
          bool bChoice = InputItemPriority(m_Prioritizer.getAtIndex(i),
                            m_Prioritizer.getAtIndex(j));
          //If false returned, then user cancelled prioritization,
          // and we exit loop.
          if (!bChoice)
          {
            return;
          }
        }
      }
      }
      //Print list of items to command line - ordered by priority
    [CommandMethod("DisplayList")]
    public void DisplayList()
    {
      // If less than 2 Items, we can't have set Priorities yet.
      if (m_Prioritizer.ItemCount < 2)
      {
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        ed.WriteMessage
          ("\nNo data to show.\nRun AddItems and AddPriorities commands.\n");
        return;
      }
      //Don't display results unless user has set priorities
      if (!m_Prioritizer.HasPriorities)
      {
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        ed.WriteMessage("\nNo priorities set.\nRun AddPriorities command.\n");
        return;
      }
      //Sort list in priority order
      m_Prioritizer.Sort();
      //Display each Item in the list (in sort order)
      for (int i = 0; i < m_Prioritizer.ItemCount; i++)
      {
        OutputItem(m_Prioritizer.getAtIndex(i));
      }
      }
      //Load previously saved priority list
    [CommandMethod("LoadItems")]
    public void LoadItems()
    {
      //Prompt for FileNameResult using AutoCAD file dialog
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      PromptOpenFileOptions opts = new PromptOpenFileOptions("\nEnter filename:");
      opts.Filter = "prioritizer files (*.prz)|*.prz";
      opts.DialogName = "Prioritizer";
      opts.DialogCaption = "Load Priority list";
      opts.InitialFileName = "Prioritizer.prz";
      PromptFileNameResult res = ed.GetFileNameForOpen(opts);
      //If file exists, we load it.
      if (res.Status == PromptStatus.OK)
      {
        if (File.Exists(res.StringResult))
        {
          Stream TestFileStream = File.OpenRead(res.StringResult);
          BinaryFormatter deserializer = new BinaryFormatter();
          m_Prioritizer = (PrioritizerCore)deserializer.Deserialize(TestFileStream);
          TestFileStream.Close();
          return;
        }
      }
      ed.WriteMessage("\nLoad cancelled\n");
    }
      //Save priority list
    [CommandMethod("SaveItems")]
    public void SaveItems()
    {
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      //Only save list if there is a list
      if (m_Prioritizer.ItemCount == 0)
      {
        ed.WriteMessage("\nNo data to save.\n");
        return;
      }
      //Prompt for filepath using AutoCAD save dialog and then save.
      PromptSaveFileOptions opts = new PromptSaveFileOptions("\nEnter filename:");
      opts.Filter = "prioritizer files (*.prz)|*.prz";
      opts.DialogName = "Prioritizer";
      opts.DialogCaption = "Save Priority list";
      opts.InitialFileName = "Prioritizer.prz";
      PromptFileNameResult res = ed.GetFileNameForSave(opts);
      if ((res.Status == PromptStatus.OK) &&
            (!String.IsNullOrEmpty(res.StringResult)) &&
            (!String.IsNullOrWhiteSpace(res.StringResult)))
      {
          Stream TestFileStream = File.Create(res.StringResult);
          BinaryFormatter serializer = new BinaryFormatter();
          serializer.Serialize(TestFileStream, m_Prioritizer);
          TestFileStream.Close();
      }
      else
      {
        ed.WriteMessage("\nSave cancelled\n");
        return;
      }
    }
        //Ask user to input Items on command line
    //Returns true if user didn't cancel or hit Enter without typing text
    public bool InputListItem()
    {
      Database db =
        Application.DocumentManager.MdiActiveDocument.Database;
      Editor ed =
        Application.DocumentManager.MdiActiveDocument.Editor;
      PromptStringOptions opts =
        new PromptStringOptions("\nEnter item for list:");
      opts.AllowSpaces = true;
      //Prompt for text. Return true if valid text was entered
      PromptResult res = ed.GetString(opts);
      if (res.Status == PromptStatus.OK)
      {
        if (res.StringResult == "")
        {
          return false;
        }
        //Don't allow duplicates
        if (!m_Prioritizer.AddItem(res.StringResult))
        {
          ed.WriteMessage("\nYou already entered an item with that name.");
        }
        return true;
      }
      else
      {
       return false;
      }
    }
        //Present (boolean) choice between two items
    // Return True if 1st item is chosen. Otherwise false
    public bool InputItemPriority( Item Choice1,  Item Choice2)
    {
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      PromptKeywordOptions opts = new PromptKeywordOptions(
        "\nWhich is higher priority: <1. " + Choice1.ItemText +
          "> or <2. " + Choice2.ItemText + ">.");
      opts.Keywords.Add("1");
      opts.Keywords.Add("2");
      //Prompt user to select (1 or 2).
      //(Could have prompted for integer instead of keywords here).
      PromptResult res = ed.GetKeywords(opts);
      if (res.Status == PromptStatus.OK)
      {
        //Tell Item 1 it is better than Item 2
        if (res.StringResult == "1")
        {
          Choice1.AddBetterThanItem(Choice2);
          return true;
        }
        //Tell Item2 it is better than Item 1
        else if (res.StringResult == "2")
        {
          Choice2.AddBetterThanItem(Choice1);
          return true;
        }
      }
      return false;
    }
        //Display an item
    public void OutputItem(Item anItem)
    {
      Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
        "\n" + anItem.ItemText + " : " + anItem.Score);
    }
    //Display whole list
    public void OutputList(List<Item> anItemList)
    {
      foreach (Item i in anItemList)
      {
        OutputItem(i);
      }
      Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("\n");
    }
  }
}
The commands are:
ADDITEMS – Add new items to your list
ADDPRIORITIES – Prioritize the list
DISPLAYLIST – Displays the list in order of priority
As a special bonus, I’ve even added serialization (which is embarrassingly easy using the [Serializable] attribute):
SAVEITEMS – Saves your list and priorities
LOADITEMS – Loads a list you previously saved
The functionality is quite basic (for example, you can’t even remove or edit items), and the AutoCAD commandline isn’t the best UI choice for this application. But it works. Here is the commandline output for the example I’ve already used:
Command: ADDITEMS
Enter item for list: Fix the roof
Enter item for list: Paint the spare bedroom
Enter item for list: Paint the house exterior
Enter item for list: Dig up the lawn
Enter item for list: Build a fence
Enter item for list:
Command: ADDPRIORITIES
Which is higher priority: <1. Fix the roof> or <2. Paint the spare bedroom>.
[1/2]: 2
Which is higher priority: <1. Fix the roof> or <2. Paint the house exterior>.
[1/2]: 1
Which is higher priority: <1. Fix the roof> or <2. Dig up the lawn>. [1/2]: 1
Which is higher priority: <1. Fix the roof> or <2. Build a fence>. [1/2]: 1
Which is higher priority: <1. Paint the spare bedroom> or <2. Paint the house
exterior>. [1/2]: 1
Which is higher priority: <1. Paint the spare bedroom> or <2. Dig up the lawn>.
[1/2]: 1
Which is higher priority: <1. Paint the spare bedroom> or <2. Build a fence>.
[1/2]: 1
Which is higher priority: <1. Paint the house exterior> or <2. Dig up the
lawn>. [1/2]: 1
Which is higher priority: <1. Paint the house exterior> or <2. Build a fence>.
[1/2]: 1
Which is higher priority: <1. Dig up the lawn> or <2. Build a fence>. [1/2]: 2
Command: DISPLAYLIST
Paint the spare bedroom : 4
Fix the roof : 3
Paint the house exterior : 2
Build a fence : 1
Dig up the lawn : 0
Give it a test drive if you like. The next post in this series will concentrate on migrating the PrioritizerCore and Item implementations to Java. See you again soon .

