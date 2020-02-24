package com.example.petrecog.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import com.example.petrecog.model.HistoryItem;
import com.example.petrecog.ui.PhotoProcessActivity;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

public class HistoryItemRepo {
    private NewDatabase dbHelper;

    public HistoryItemRepo(Context context){
        dbHelper = new NewDatabase(context, "history.db", 1);
    }

    public int insert(HistoryItem historyItem){

        SQLiteDatabase db = dbHelper.getWritableDatabase();

        ContentValues values=new ContentValues();
        values.put(HistoryItem.KEY_ID, historyItem.ID);
        values.put(HistoryItem.KEY_DESCRIPTION, historyItem.description);
        byte[] data = PhotoProcessActivity.Bitmap2Bytes(historyItem.picture);
        byte[] mPic = Base64.encode(data, 0);
        values.put(HistoryItem.KEY_PIC, mPic);
        values.put(HistoryItem.KEY_DATE, historyItem.date);

        long historyItem_Id = db.insert(HistoryItem.TABLE,null,values);
        db.close();
        return (int)historyItem_Id;
    }

    public void delete(int historyItem_Id){
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        db.delete(HistoryItem.TABLE,HistoryItem.KEY_ID+"=?", new String[]{String.valueOf(historyItem_Id)});
        db.close();
    }
    public void update(HistoryItem historyItem){
        SQLiteDatabase db = dbHelper.getWritableDatabase();

        ContentValues values = new ContentValues();

        values.put(HistoryItem.KEY_ID, historyItem.ID);
        values.put(HistoryItem.KEY_DESCRIPTION, historyItem.description);
        byte[] data = PhotoProcessActivity.Bitmap2Bytes(historyItem.picture);
        byte[] mPic = Base64.encode(data, 0);
        values.put(HistoryItem.KEY_PIC ,mPic);
        values.put(HistoryItem.KEY_DATE, historyItem.date);

        db.update(HistoryItem.TABLE,values,HistoryItem.KEY_ID+"=?",new String[] { String.valueOf(historyItem.ID) });
        db.close();
    }

    public ArrayList<HistoryItem> getAllHistoryItems(){

        SQLiteDatabase db=dbHelper.getReadableDatabase();
        String selectQuery="SELECT "+
                HistoryItem.KEY_ID+","+
                HistoryItem.KEY_DESCRIPTION+","+
                HistoryItem.KEY_PIC+","+
                HistoryItem.KEY_DATE +" FROM " + HistoryItem.TABLE;
        ArrayList<HistoryItem> historyItems=new ArrayList<HistoryItem>();
        Cursor cursor = db.rawQuery(selectQuery,null);

        if(cursor.moveToFirst()){
            do{
                HistoryItem historyItem = new HistoryItem();
                historyItem.ID = cursor.getInt(cursor.getColumnIndex(HistoryItem.KEY_ID));
                historyItem.description = cursor.getString(cursor.getColumnIndex(HistoryItem.KEY_DESCRIPTION));
                byte[] mpicture = cursor.getBlob(cursor.getColumnIndex(HistoryItem.KEY_PIC));
                historyItem.picture = byte2bitmap(mpicture);
                historyItem.date = cursor.getString(cursor.getColumnIndex(HistoryItem.KEY_DATE));
                historyItems.add(historyItem);
            }while(cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return historyItems;
    }

    public int getNextId(){

        SQLiteDatabase db=dbHelper.getReadableDatabase();
        String selectQuery="SELECT "+
                HistoryItem.KEY_ID+","+
                HistoryItem.KEY_DESCRIPTION+","+
                HistoryItem.KEY_PIC+","+
                HistoryItem.KEY_DATE +" FROM " + HistoryItem.TABLE;
        HistoryItem historyItem = new HistoryItem();
        Cursor cursor = db.rawQuery(selectQuery,null);

        if(cursor.moveToLast()){
            do{
                historyItem.ID = cursor.getInt(cursor.getColumnIndex(HistoryItem.KEY_ID));
            }while(cursor.moveToNext());
        }
        cursor.close();
        db.close();

        if(historyItem.ID == -1){
            return 0;
        }
        else{
            return (historyItem.ID + 1);
        }
    }

    public Bitmap getBitmap(int id){

        SQLiteDatabase db=dbHelper.getReadableDatabase();
        String selectQuery="SELECT "+
                HistoryItem.KEY_ID+","+
                HistoryItem.KEY_DESCRIPTION+","+
                HistoryItem.KEY_PIC+","+
                HistoryItem.KEY_DATE +
                " FROM " + HistoryItem.TABLE +
                " WHERE " + HistoryItem.KEY_ID + "=?";
        HistoryItem historyItem = new HistoryItem();
        Cursor cursor = db.rawQuery(selectQuery,new String[]{String.valueOf(id)});

        if(cursor.moveToFirst()){
            do{
                historyItem.ID = cursor.getInt(cursor.getColumnIndex(HistoryItem.KEY_ID));
                historyItem.description = cursor.getString(cursor.getColumnIndex(HistoryItem.KEY_DESCRIPTION));
                byte[] mpicture = cursor.getBlob(cursor.getColumnIndex(HistoryItem.KEY_PIC));
                historyItem.picture = byte2bitmap(mpicture);
                historyItem.date = cursor.getString(cursor.getColumnIndex(HistoryItem.KEY_DATE));
            }while(cursor.moveToNext());
        }
        cursor.close();
        db.close();

        return historyItem.picture;
    }

    private Bitmap byte2bitmap(byte[] bytes){


        String base64String = null;
        try {
            base64String = new String(bytes,"ascii");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        byte[] decodedString = Base64.decode(base64String, Base64.DEFAULT);
        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);

        return decodedByte;
    }
}
