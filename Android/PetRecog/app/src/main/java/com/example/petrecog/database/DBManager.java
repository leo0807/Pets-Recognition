package com.example.petrecog.database;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

import com.example.petrecog.model.PetItem;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

public class DBManager {
    private Context mContext;

    private List<PetItem> animalItems = new ArrayList<PetItem>();

    public DBManager(Context mContext) {
        this.mContext = mContext;
    }

    //From assets folder copy db file to dbpath folder
    public SQLiteDatabase openDatabase(String mDataBaseName) {
        String DB_PATH;
        if(android.os.Build.VERSION.SDK_INT >= 4.2){
            DB_PATH = this.mContext.getApplicationInfo().dataDir + "/databases/";
        }
        else {
            DB_PATH = "/data/data/" + this.mContext.getPackageName() + "/databases/";
        }
        String dbPath = DB_PATH + mDataBaseName;
        if (!new File(dbPath).exists()) {
            try {
                boolean flag = new File(DB_PATH).mkdirs();
                boolean newFile = new File(dbPath).createNewFile();
                try {
                    FileOutputStream out = new FileOutputStream(dbPath);
                    InputStream in = mContext.getAssets().open(mDataBaseName);
                    byte[] buffer = new byte[1024];
                    int readBytes = 0;
                    while ((readBytes = in.read(buffer)) != -1)
                        out.write(buffer, 0, readBytes);
                    in.close();
                    out.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else
        {
            // If the DB file is modified, needs to replace it
            try {
                FileOutputStream out = new FileOutputStream(dbPath);
                InputStream in = mContext.getAssets().open("myDatabase.db");
                byte[] buffer = new byte[1024];
                int readBytes = 0;
                while ((readBytes = in.read(buffer)) != -1)
                    out.write(buffer, 0, readBytes);
                in.close();
                out.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return SQLiteDatabase.openOrCreateDatabase(dbPath, null);
    }

    public List<PetItem> getAllPetsfromTable(SQLiteDatabase sqliteDB, String table) {
        PetItem animalItem = null;
        try {
            Cursor cursor = sqliteDB.rawQuery("select * from " + table, null);
            while (cursor.moveToNext()) {

                Integer mid = cursor.getInt(cursor.getColumnIndex("ID"));
                String mbreed = cursor.getString(cursor.getColumnIndex("Breed"));
                String mdescription = cursor.getString(cursor.getColumnIndex("Description"));
                byte[] mpicture = cursor.getBlob(cursor.getColumnIndex("Picture"));

                String base64String=new String(mpicture,"ascii");

                byte[] decodedString = Base64.decode(base64String.split(",")[1], Base64.DEFAULT);
                Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);

                animalItem = new PetItem();

                animalItem.id = mid;
                animalItem.breed = mbreed;
                animalItem.description = mdescription;
                animalItem.picture = decodedByte;

                animalItems.add(animalItem);
            }
            cursor.close();
            return animalItems;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;

    }

    public PetItem getPetFromTableViaName(SQLiteDatabase sqliteDB, String table, String name){
        PetItem animalItem = null;

        Cursor cursor = sqliteDB.query(table, null, "breed=?", new String[]{name}, null, null, null);
        while (cursor.moveToNext()) {

            Integer mid = cursor.getInt(cursor.getColumnIndex("ID"));
            String mbreed = cursor.getString(cursor.getColumnIndex("Breed"));
            String mdescription = cursor.getString(cursor.getColumnIndex("Description"));
            byte[] mpicture = cursor.getBlob(cursor.getColumnIndex("Picture"));

            String base64String= null;
            try {
                base64String = new String(mpicture,"ascii");
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }

            byte[] decodedString = Base64.decode(base64String.split(",")[1], Base64.DEFAULT);
            Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);

            animalItem = new PetItem();

            animalItem.id = mid;
            animalItem.breed = mbreed;
            animalItem.description = mdescription;
            animalItem.picture = decodedByte;
        }
        cursor.close();
        return animalItem;
    }
}
