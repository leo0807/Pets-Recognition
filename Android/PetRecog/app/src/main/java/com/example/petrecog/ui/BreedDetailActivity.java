package com.example.petrecog.ui;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.petrecog.database.DBManager;
import com.example.petrecog.R;
import com.example.petrecog.model.PetItem;

/**
 * This is the BreedDetailActivity of PetRecog Application
 * Navigate from: Main Activity or PhotoProcess Activity
 * Navigate to  : None
 *
 * @author  LinYun Li
 */
public class BreedDetailActivity extends AppCompatActivity {

    ImageView mImageShow;
    TextView mDescription_text;

    private final int UPDATE_LIST = 12121;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_breed_detail);

        initView();
    }

    /**
     * Initial view
     */
    private void initView()
    {
        // Add actionBar and set title
        ActionBar actionBar = getSupportActionBar();
        if(actionBar != null){
            actionBar.setHomeButtonEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setTitle(getIntent().getStringExtra("breed"));
        }

        mImageShow = findViewById(R.id.pic_show);
        mDescription_text = findViewById(R.id.description_show);

        int inputType = getIntent().getIntExtra("input_type", 1);

        //input_type tell which info is transferred from previous Activity
        if (inputType == 0){
            //previous Activity is MainActivity
            byte[] bis = getIntent().getByteArrayExtra("pic");
            Bitmap bitmap = BitmapFactory.decodeByteArray(bis, 0, bis.length);
            mImageShow.setImageBitmap(bitmap);

            mDescription_text.setText(formatDescription(getIntent().getStringExtra("description")));
        }
        else{
            //previous Activity is PhotoProcessActivity
            queryDBfile(getIntent().getStringExtra("table"), getIntent().getStringExtra("breed"));

        }
    }

    /**
     * Clicked the back icon shown in the actionBar
     */
    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.finish(); // back button
                return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * Handle the result after reading the Database file
     * Load image and description into UI
     */
    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case UPDATE_LIST:
                    PetItem mPet = (PetItem) msg.obj;
                    if (mPet != null){
                        mImageShow.setImageBitmap(mPet.picture);
                        mDescription_text.setText(formatDescription(mPet.description));
                    }
                    else{
                        mDescription_text.setText("Unknown Pet!!!");
                    }
                    break;
                default:
                    break;
            }
        }
    };

    /**
     * Using a new thread to Query Specified Breed information from Specified Table in DataBase
     * @param table The table name of Database which need to be queried
     * @param breedName The name of breed which need to be queried
     */
    private void queryDBfile(String table, String breedName){
        new Thread(new Runnable() {
            @Override
            public void run() {
                DBManager dbManager = new DBManager(getBaseContext());
                SQLiteDatabase petInfoDatabase = dbManager.openDatabase("myDatabase.db");

                PetItem mPet = dbManager.getPetFromTableViaName(petInfoDatabase, table, breedName);

                petInfoDatabase.close();

                Message message = new Message();
                message.what = UPDATE_LIST;
                message.obj = mPet;
                handler.sendMessage(message);
            }
        }).start();
    }

    /**
     * Format the Descriptions
     * Add one new empty line between two paragraph
     * @param str Source Description String
     * @return Formatted Description String
     */
    private String formatDescription(String str){
        return  str.replace("\n\n", "\n").replace("\n", "\n\n");
    }

}
