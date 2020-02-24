package com.example.petrecog.ui;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.ContextMenu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.petrecog.model.HistoryItem;
import com.example.petrecog.model.HistoryItemAdapter;
import com.example.petrecog.database.HistoryItemRepo;
import com.example.petrecog.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * This is the HistoryActivity of PetRecog Application
 * Navigate from: Camera Activity
 * Navigate to  : BreedDetail Activity
 *
 * @author  LinYun Li
 */
public class HistoryActivity extends AppCompatActivity {

    private ListView listView;
    private List<HistoryItem> list = new ArrayList<>();

    HistoryItemAdapter itemAdapter;

    private final int UPDATE_LIST = 12121;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        ActionBar actionBar = getSupportActionBar();
        if(actionBar != null){
            actionBar.setHomeButtonEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setTitle("History");
        }

        listView = findViewById(R.id.history_list);


        itemAdapter = new HistoryItemAdapter(this, R.layout.item_history, list);
        listView.setAdapter(itemAdapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                HistoryItem item = list.get(position);

                openPhotoProcessActivity(item);
            }
        });

        //Triggered by long press listItem
        listView.setOnCreateContextMenuListener(new View.OnCreateContextMenuListener() {

            @Override
            public void onCreateContextMenu(ContextMenu arg0, View arg1,
                                            ContextMenu.ContextMenuInfo arg2) {
//                arg0.setHeaderTitle("Select Option");
                arg0.add(0, 0, 0, "Delete");
            }
        });

//        getAllHistoryItems();

    }

    //set long pressed event
    @Override
    public boolean onContextItemSelected(MenuItem item) {
        // TODO Auto-generated method stub
        AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
        //get the id of the item
        int id = list.get((int)(info.id)).ID;
        switch(item.getItemId()){
            case 0:
                showDeleteDialog(id);
                return true;
            case 1:
                Toast.makeText(this, "other", Toast.LENGTH_SHORT).show();
                return true;
        }

        return super.onContextItemSelected(item);
    }


    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case UPDATE_LIST:
                    List<HistoryItem> mHistoryList = (List<HistoryItem>) msg.obj;
                    if (mHistoryList != null){
                        for (HistoryItem mHistaory : mHistoryList) {
                            itemAdapter.add(mHistaory);
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    };



    private void getAllHistoryItems(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                HistoryItemRepo repo = new HistoryItemRepo(getApplicationContext());

                ArrayList<HistoryItem> historyItems =  repo.getAllHistoryItems();

                Message message = new Message();
                message.what = UPDATE_LIST;
                message.obj = historyItems;
                handler.sendMessage(message);
            }
        }).start();

    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                this.finish(); // back button
                return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void openPhotoProcessActivity(HistoryItem item){
        Intent newIntent = new Intent(this, PhotoProcessActivity.class);
        newIntent.putExtra("id",item.ID);
        newIntent.putExtra("input_type", 1);
        newIntent.putExtra("date", item.date);

        newIntent.putExtra("description",item.description);

        startActivity(newIntent);
    }

    private void showDeleteDialog(int id){
        final AlertDialog.Builder normalDialog =
                new AlertDialog.Builder(this);

        normalDialog.setTitle("Delete");
        normalDialog.setMessage("Are you sure to delete this history record ?");
        normalDialog.setPositiveButton("Sure",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                        deleteFromDb(id);
                        itemAdapter.clear();
                        getAllHistoryItems();
                        Toast.makeText(getBaseContext(),"Delete Successfully!", Toast.LENGTH_LONG).show();
                    }
                });
        normalDialog.setNegativeButton("Cancel",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                        ;
                    }
                });

        normalDialog.show();
    }

    private void deleteFromDb(int id){
        HistoryItemRepo repo = new HistoryItemRepo(this);
        repo.delete(id);
    }

    @Override
    protected void onResume() {
        super.onResume();
        itemAdapter.clear();
        getAllHistoryItems();
    }
}
