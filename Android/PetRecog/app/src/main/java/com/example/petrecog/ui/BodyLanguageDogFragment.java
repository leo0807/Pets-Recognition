package com.example.petrecog.ui;

import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.os.Handler;
import android.os.Message;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;

import com.example.petrecog.database.DBManager;
import com.example.petrecog.R;
import com.example.petrecog.model.PetItem;
import com.example.petrecog.model.PetItemAdapter;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

/**
 * This is the BodyLanguageDogFragment of PetRecog Application
 * It will be loaded in BodyLanguage Fragment (Main Activity)
 *
 * @author  LinYun Li
 */
public class BodyLanguageDogFragment extends Fragment {

    private List<PetItem> list = new ArrayList<>();
    PetItemAdapter itemAdapter;

    private final int UPDATE_LIST = 12121;

    public BodyLanguageDogFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_brand_cat, container, false);

        ListView listView = (ListView) view.findViewById(R.id.brand_list);

        itemAdapter = new PetItemAdapter(getContext(), R.layout.item_brand, list);
        listView.setAdapter(itemAdapter);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                PetItem item = list.get(position);

                openDetailActivity(item);
            }
        });

        readDBfile();
        return view;
        // Inflate the layout for this fragment
    }

    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case UPDATE_LIST:
                    List<PetItem> mAnimalLists = (List<PetItem>) msg.obj;
                    if (mAnimalLists != null){
                        for (PetItem mAnimal : mAnimalLists) {
                            itemAdapter.add(mAnimal);
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    };

    private void readDBfile(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                DBManager dbManager = new DBManager(getContext());
                SQLiteDatabase petInfoDatabase = dbManager.openDatabase("myDatabase.db");

                List<PetItem> mCatLists = dbManager.getAllPetsfromTable(petInfoDatabase, "EmotionDog");

                petInfoDatabase.close();

                Message message = new Message();
                message.what = UPDATE_LIST;
                message.obj = mCatLists;
                handler.sendMessage(message);
            }
        }).start();
    }

    /**
     * Open BreedDetailActivity
     * @param item Specified PetItem
     */
    private void openDetailActivity(PetItem item){
        Intent newIntent = new Intent(getActivity(), BreedDetailActivity.class);
        newIntent.putExtra("breed",item.breed);
        newIntent.putExtra("input_type", 0);

        Bitmap m = item.picture;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        m.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] bitmapByte = baos.toByteArray();
        newIntent.putExtra("pic",bitmapByte);
        newIntent.putExtra("description",item.description);
        startActivity(newIntent);
    }


}
