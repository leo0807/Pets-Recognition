package com.example.petrecog.database;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.petrecog.model.HistoryItem;

public class NewDatabase extends SQLiteOpenHelper {

    private final String TABLE_NAME = HistoryItem.TABLE;
    private final String VALUE_ID = HistoryItem.KEY_ID;
    private final String VALUE_DESC = HistoryItem.KEY_DESCRIPTION;
    private final String VALUE_PIC = HistoryItem.KEY_PIC;
    private final String VALUE_DATE = HistoryItem.KEY_DATE;

    final String SQL_CREATE_TABLE = "create table " + TABLE_NAME + "(" +

        VALUE_ID + " integer primary key AUTOINCREMENT ," +
        VALUE_DESC + " text ," +
        VALUE_PIC + " blob ," +
        VALUE_DATE + " text " +
        ")";


    public NewDatabase(Context context, String databaseName, int version) {
        super(context, databaseName, null, version);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(SQL_CREATE_TABLE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }

}
