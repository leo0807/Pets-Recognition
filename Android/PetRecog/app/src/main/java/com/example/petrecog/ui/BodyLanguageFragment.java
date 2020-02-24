package com.example.petrecog.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;

import androidx.fragment.app.Fragment;

import com.example.petrecog.R;

/**
 * This is the BodyLanguageFragment of PetRecog Application
 * It will be loaded in Main Activity
 *
 * @author  LinYun Li
 */
public class BodyLanguageFragment extends Fragment implements View.OnClickListener{

    private RadioButton body_catSelectBtn, body_dogSelectBtn;
    private int currentChildFragment = 0;

    public BodyLanguageFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_body_language, container, false);
        getChildFragmentManager().beginTransaction().replace(R.id.bodyContainer,new BodyLanguageCatFragment()).commit();
        currentChildFragment = 0;

        body_catSelectBtn = view.findViewById(R.id.body_catSelectBtn);
        body_catSelectBtn.setOnClickListener(this);
        body_dogSelectBtn = view.findViewById(R.id.body_dogSelectBtn);
        body_dogSelectBtn.setOnClickListener(this);


        return view;
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.body_catSelectBtn:
                if(currentChildFragment != 0){
                    getChildFragmentManager().beginTransaction().replace(R.id.bodyContainer,new BodyLanguageCatFragment()).commit();
                    currentChildFragment = 0;
                }
                break;
        }
        switch (v.getId()) {
            case R.id.body_dogSelectBtn:
                if(currentChildFragment != 1){
                    getChildFragmentManager().beginTransaction().replace(R.id.bodyContainer,new BodyLanguageDogFragment()).commit();
                    currentChildFragment = 1;
                }
                    break;

        }
    }
}
