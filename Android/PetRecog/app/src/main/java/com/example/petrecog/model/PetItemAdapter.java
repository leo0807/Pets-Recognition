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

import java.util.List;


public class PetItemAdapter extends ArrayAdapter<PetItem> {

    private int layoutId;

    public PetItemAdapter(Context context, int layoutId, List<PetItem> list) {
        super(context, layoutId, list);
        this.layoutId = layoutId;
    }

    @NonNull
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View view;
        ViewHolder viewHolder;
        PetItem item = getItem(position);
        if (convertView == null) {
            view = LayoutInflater.from(getContext()).inflate(layoutId, parent, false);
            viewHolder = new ViewHolder();
            viewHolder.imageView = (ImageView) view.findViewById(R.id.item_img);
            viewHolder.textView = (TextView) view.findViewById(R.id.item_text);
            view.setTag(viewHolder);
        } else {
            view = convertView;
            viewHolder = (ViewHolder) view.getTag();
        }

        viewHolder.imageView.setImageBitmap(item.picture);
        viewHolder.textView.setText(item.breed);

        return view;
    }

    class ViewHolder {
        ImageView imageView;
        TextView textView;
    }

}
