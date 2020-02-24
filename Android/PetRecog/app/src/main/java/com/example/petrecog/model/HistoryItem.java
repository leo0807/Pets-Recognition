package com.example.petrecog.model;

import android.graphics.Bitmap;

public class HistoryItem {

    //table name
    public static final String TABLE = "History";

    //column name
    public static final String KEY_ID = "id";
    public static final String KEY_DESCRIPTION = "description";
    public static final String KEY_PIC = "pic";
    public static final String KEY_DATE = "date";

    //Attributes
    public int ID = -1;
    public String description = "None";
    public Bitmap picture = null;
    public String date = "20200210";

    public void History(){

    }
}
