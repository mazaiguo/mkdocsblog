---
title: "Converting C# to Java – An Experiment (Part 5)"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Unicode
description: "(Links to previous installments: Part 1; Part 2; Part 3; Part 4)."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 5)

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/converting-c-to-java-an-experiment-part-5.html

## 文章内容

By Stephen Preston
(Links to previous installments: Part 1; Part 2; Part 3; Part 4).
Last time, we hooked up a simple Android UI to display a few hardcoded Items in a ListView. Today we'll add some functionality to allow us to add or edit items in the list. I've decided to implement a footer to the ListView that will contain a button to add items. I'll also respond to someone clicking an item in the list to edit that item. Both those actions will launch a new screen - and that is the main focus of today's post:
Switching control from one screen/layout to another using an Intent (and then returning control back to the original screen).
First, let's create the XML for our new screen. Create a new Android XML file called 'edititem' and copy this XML into it:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >
    <EditText
        android:id="@+id/EditItemText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" 
        android:singleLine="true" >
        <requestFocus />
    </EditText>
    <LinearLayout
        android:id="@+id/linearLayout1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" >
        <Button
            android:id="@+id/buttonEditCancel"
            android:layout_width="fill_parent"
            android:layout_height="wrap_content"
            android:text="Cancel" android:gravity="center" android:layout_weight="1" android:onClick="onCancelButtonClick"/>
        <Button
            android:id="@+id/buttonEditOk"
            android:layout_width="fill_parent"
            android:layout_height="wrap_content"
            android:text="Ok" android:gravity="center" android:layout_weight="1" android:onClick="onOkButtonClick"/>
    </LinearLayout>
</LinearLayout>
I'm being a bit naughty here by using hardcoded strings instead of adding new string resources to the project 'strings.xml' file. This is just for the convenience of documenting steps in this blog. You should reference resources for all text that appears in your Android app so you can easily localize it later.
For that matter, I'm probably inadvertently ignoring other Java/Android best practices simply because I'm learning this as I go along.
Now we want to create a new Activity class to display this layout. We'll call this ItemEditActivity:
Here is the code to put in ItemEditActivity.java:
package Preston.Stephen.Prioritizer;
 
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.TextView.OnEditorActionListener;

public class ItemEditActivity extends Activity {
  
  private int m_row;
  private String m_itemText;
  
  
  /** Called when the activity is first created. */
  @Override
  public void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      setContentView(R.layout.edititem);
      
      EditText editView = (EditText)findViewById(R.id.EditItemText);
      //Retrieve data passed to this Activity from the calling Activity.
      //This is stored in the Intent
      Bundle extras = getIntent().getExtras();
      m_itemText = extras.getString(CSMigrationTestActivity.INTENT_ITEM_TEXT);
      //If data (the Item name) was passed, put this in the editbox.
      if (m_itemText != null) {
        editView.setText(m_itemText);
      }
      //We also pass the row in the list this Item was stored in, so the 
      // calling Activity can update the correct Item when we return
      m_row = extras.getInt(CSMigrationTestActivity.INTENT_ITEM_ROW);
      
      //This code is to make the Activity interpret Enter being pressed as 
      // clicking ok to dismiss the screen
      editView.setOnEditorActionListener(new OnEditorActionListener() {
        public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
          if (actionId == EditorInfo.IME_ACTION_DONE) {
            Button okButton = (Button)findViewById(R.id.buttonEditOk);
            okButton.performClick();
              return true;
          }  
          return false;
        }
      });
      
  }

  //Handler function for Ok button click
  //Returns updated text data.
  public void onOkButtonClick(View v) {
    EditText editView = (EditText)findViewById(R.id.EditItemText);
    String txt = editView.getText().toString();
    if (!(m_itemText == txt)) {
    Intent i = new Intent();
    i.putExtra(CSMigrationTestActivity.INTENT_ITEM_TEXT, txt);
    i.putExtra(CSMigrationTestActivity.INTENT_ITEM_ROW, m_row);
    setResult(RESULT_OK, i);
    }
    else {
      setResult(RESULT_CANCELED);
    }
    finish();
    }

  //Handler function for Cancel button click
 public void onCancelButtonClick(View v) {
    setResult(RESULT_CANCELED);
    finish();
  }
  
}
Eclipse reports some errors in this code because there are some static items we have to add to CSMigrationTestActivity.
The above code demonstrates two ways to respond to events in Java/Android:
The first way is to add a Listener function in your code. You can see this in the call to editView.SetOnEditorActionListener. 
The second way is to specify it in the layout XML. See the android:onClick attributes in the Button elements of edititem.xml. The function names written there match the function names in our Activity implementation (onOkButtonClick and onCancelButtonClick). 
BTW I worked through the basic Notepad tutorial on the Android Developer Center to understand both Listeners and switching control to new Activities.
Now we've created a new Activity, we have make sure the Android OS knows about it, so we add it to the app's manifest file. Double-click AndroidManifest.xml now:

Then scroll down and click the Application link:
In the ApplicationNodes section, click the Add button, select Activity, and click Ok:

Select the entry you just added to the list, click the Browse button by the Name editbox, select ItemEditActivity and click Ok. The other parameters are optional, but you can populate them if you like.

Make sure you save the manifest when you're done.
Its easy to forget to update the manifest when you add a new Activity. If you find your app is crashing when you try to launch a new Activity, then the manifest is the first thing to check.
Next we want to add a button to our main view that will display this second view. Create another layout XML called footer.xml, and edit the XML to:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical" >
    <Button
        android:id="@+id/AddButton"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:text="Add Items" android:layout_gravity="center" android:gravity="center" android:clickable="true" android:soundEffectsEnabled="true"/>
</LinearLayout>
Open CSMigrationTestActivity.java and add the code highlighted in yellow in this full listing for the class:
package Preston.Stephen.Prioritizer;
 
import Preston.Stephen.Prioritizer.MyAdapter;
import Preston.Stephen.Prioritizer.R;
import Preston.Stephen.Prioritizer.ItemEditActivity;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.AdapterView.OnItemClickListener;

public class CSMigrationTestActivity extends Activity {
    /** Called when the activity is first created. */
  
  //constants
  public static final String INTENT_ITEM_TEXT = "_id";  
  public static final String INTENT_ITEM_ROW = "_row";  
  
  //Member variables
  private ListView m_listView;
  private MyAdapter m_adapter;
  private View m_footerView;
  
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        //Store ListView for this activity in a member variable for convenience 
        m_listView = (ListView)this.findViewById(R.id.ItemList); 
        //Inflate footer view and add to listview
        LayoutInflater li = getLayoutInflater();
        m_footerView = (View)li.inflate(R.layout.footer, null);
        m_listView.addFooterView(m_footerView);
        
        //Create our Adapter and attach it to our ListView
        m_adapter = new MyAdapter(this);
        m_listView.setAdapter(m_adapter);
        //Add some items to the list
        m_adapter.add("Fix the roof");        
        m_adapter.add("Paint the spare bedroom");        
        m_adapter.add("Paint the house exterior");
        m_adapter.add("Dig up the lawn");
        m_adapter.add("Build a fence");
        //Setup listeners so we can respond to user clicking on screen
        createListeners();
    }
    
    
    //Setup listeners so we can respond to user clicking on screen
    private void createListeners() {
      //Respond to user clicking on item in list
      m_listView.setOnItemClickListener(new OnItemClickListener() {
        public void onItemClick(AdapterView<?> parent, View view,
            int position, long id) {
          editItem(position, ((TextView)view).getText().toString());
        }
      });
      
      //Respond to user clicking in list view footer to add a new item
      m_footerView.findViewById(R.id.AddButton).setOnClickListener(new OnClickListener() {
        @Override
        public void onClick(View v) {
          
          editItem(m_adapter.getCount(), "");
        }
      });
    }
    
    
    //Starts ItemEditActivity to retrieve new entry for list or edit existing
    //Data is passed via the Intent we create
    public void editItem(int position, String itemText) {
      Intent editIntent = new Intent(this, ItemEditActivity.class);
      //Add data to Intent
      editIntent.putExtra(INTENT_ITEM_TEXT, itemText);
      editIntent.putExtra(INTENT_ITEM_ROW, position);
      //Launch our edit Activity
      startActivityForResult(editIntent, 0);
    }
    
    //Called when ItemEditActivity returns
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
      super.onActivityResult(requestCode, resultCode, intent);

      switch (requestCode) {
      case 0:
        processEdit(resultCode, intent);
        break;
      case 1:
        //For later
      break;
      }
    }
    
    
    //Add or edit a new item.
    //TODO: Re-architect so ItemEditActivity checks name is acceptable before 
    // returning control to this activity.
    private void processEdit(int resultCode, Intent intent) {
      if (resultCode == RESULT_OK) {
        Bundle b = intent.getExtras();
        String str = b.getString(INTENT_ITEM_TEXT);
        int row = b.getInt(INTENT_ITEM_ROW);
        if (row == m_adapter.getCount()) {
          m_adapter.add(str);
        }
        else {
          m_adapter.renameAt(row, str);
        }
      }
    }
}
We add our 'Add Items'  button to the bottom of the view by using a LayoutInflater to create a new View from footer.xml and passing it to the ListView's addFooter function.
Our createListeners function adds a listener for the ListView being clicked, and for our "Add Items' button.
The other important new code here - and the main point of this article - is the code required to launch our ItemEditActivity when 'Add Items' is clicked. We launch our new Activity with our call to startActivityForResult(), and that activity returns control to this Activity via onActivityResult().
Note that we pass a request code to the activity we're starting up, which it later returns to the calling activity. Because we only have one onActivityResult() function, this is how we know which activity is returning its results to us. When we add additional activities that perform other tasks to our app, we'll need to be able to tell which one is returning control to us. 
New Activities are launched (and data passed to them) using Intents. Our editItem function creates an Intent and uses it to launch the new Activity by passing that Intent to startActivityForResult(). In this case, we know which Activity we want to launch, but you can also use Intents to 'broadcast' to other apps that your app needs a service performing for it. (Read more about it here).
We also have to update our Item.Equals() function, because the if (String == String) logic in Java isn't correctly comparing the String contents:
      // Items considered equal if their text is equal
      //Old line
      //if (this.getItemText() == lhs.getItemText())) {
      //New line
      if (this.getItemText().compareToIgnoreCase(lhs.getItemText()) == 0) {
        return true;
      }
      return false;
    }
And we're adding functionality for the user to rename an Item, which we didn't have in our AutoCAD .NET plug-in, so we implement a setItemTextAt() function in PrioritizerCore:
  public boolean setItemTextAt(int index, String newText) {
    if ((index <0)||(index >= m_ItemList.size())) {
      return false;
    }
    Item tmpItem = new Item();
    tmpItem.setItemText(newText);
    if (m_ItemList.contains(tmpItem))
      return false;
    m_ItemList.get(index).setItemText(newText);
    return true;
  }
And we add a corresponding function in MyAdapter:
   public boolean renameAt(int index, String newText) {
    return m_prioritizer.setItemTextAt(index, newText);
  }
That should be all we need to do for our app to work. However, its possible I missed highlighting the odd code change, so here is a download of the full project to date.
Now its time to run the app. The list looks the same as last time except it has a button at the bottom that you can press to add a new item:

Clicking on 'Add Item' launches our new activity which prompts the user to enter a new Item. Clicking on an Item in the list launches the same activity, but populates it with the name of the Item:

That's it for today. And that's pretty much all there is to programming a simple (text-based) Android app. In my final post on this subject, I'll be posting a completed (or at least more complete) version of this project and summarizing this series. Most of the rest of the work is just more of the same - adding buttons to perform other functions in the app(prioritization etc), and (maybe) fully implementing serialization so we can work with multiple lists, and so we can handle restoring an Activity if it gets destroyed by the OS. There's also an architectural flaw in the current implementation that I'd like to fix, where the EditItemActivity can't check whether the edited/new Item name already exists.
I've not written all of that yet, and I'm off to Portland for the Manufacturing DevCamp for the rest of this week - so it may be a while before that final post appears.

