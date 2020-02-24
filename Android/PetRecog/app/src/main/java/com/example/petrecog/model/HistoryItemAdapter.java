package com.example.petrecog.model;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.example.petrecog.R;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;

public class HistoryItemAdapter extends ArrayAdapter<HistoryItem> {
    private int layoutId;

    public HistoryItemAdapter(Context context, int layoutId, List<HistoryItem> list) {
        super(context, layoutId, list);
        this.layoutId = layoutId;
    }

    @NonNull
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View view;
        HistoryItemAdapter.ViewHolder viewHolder;
        HistoryItem item = getItem(position);
        if (convertView == null) {
            view = LayoutInflater.from(getContext()).inflate(layoutId, parent, false);
            viewHolder = new ViewHolder();
            viewHolder.imageView = (ImageView) view.findViewById(R.id.history_img);
            viewHolder.textView = (TextView) view.findViewById(R.id.history_breed);
            viewHolder.tv_emotion = (TextView) view.findViewById(R.id.history_emotion);
            viewHolder.tv_date = (TextView) view.findViewById(R.id.history_date);
            view.setTag(viewHolder);
        } else {
            view = convertView;
            viewHolder = (HistoryItemAdapter.ViewHolder) view.getTag();
        }


        String[] texts = {"Breed", "Emotion"};
        try {
            texts = analyzeJson(item.description);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        viewHolder.textView.setText(texts[0]);
        viewHolder.tv_emotion.setText(texts[1]);
        viewHolder.tv_date.setText(item.date);
        viewHolder.imageView.setImageBitmap(item.picture);

        return view;
    }

    public void addItem(String breed){

    }

    private String[] analyzeJson(String jsonStr) throws JSONException {
        JSONObject jsonObject = new JSONObject(jsonStr);
        String petName = jsonObject.getString("pet");
        String breedName = jsonObject.getString("breed");
        String emotion = jsonObject.getString("emotion");

        String[] breeds = breedName.split("\n");
        String[] breedNameOnly = new String[breeds.length];
        int i = 0;
        for(String breed : breeds){
            String str = breed.trim();
            breedNameOnly[i] = str.split(" ")[0];
            i++;
        }

        String[] emotions = emotion.split("\n");
        String[] emotionNameOnly = new String[emotions.length];
        int x = 0;
        for(String emo : emotions){
            String str = emo.trim();
            emotionNameOnly[x] = str.split(" ")[0];
            x++;
        }

        String[] retVal = new String[2];
        retVal[0] = breedNameOnly[0];
        retVal[1] = emotionNameOnly[0];

        return retVal;

    }

    class ViewHolder {
        ImageView imageView;
        TextView textView;
        TextView tv_emotion;
        TextView tv_date;
    }
}
