package com.example.petrecog.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;

import androidx.fragment.app.Fragment;

import com.example.petrecog.R;

/**
 * This is the BrandFragment of PetRecog Application
 * It will be loaded in Main Activity
 *
 * @author  LinYun Li
 */
public class BrandFragment extends Fragment implements View.OnClickListener {

    private RadioButton brand_catSelectBtn, brand_dogSelectBtn;
    private int currentChildFragment = 0;

    public BrandFragment() {

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_brand, container,false);
        getChildFragmentManager().beginTransaction().replace(R.id.brandContainer,new BrandCatFragment()).commit();
        currentChildFragment = 0;

        brand_catSelectBtn = view.findViewById(R.id.brand_catSelectBtn);
        brand_catSelectBtn.setOnClickListener(this);
        brand_dogSelectBtn = view.findViewById(R.id.brand_dogSelectBtn);
        brand_dogSelectBtn.setOnClickListener(this);


        return view;
    }

    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.brand_catSelectBtn:
                if(currentChildFragment != 0){
                    getChildFragmentManager().beginTransaction().replace(R.id.brandContainer,new BrandCatFragment()).commit();
                    currentChildFragment = 0;
                }
                break;
        }
        switch (v.getId()) {
            case R.id.brand_dogSelectBtn:
                if(currentChildFragment != 1) {
                    getChildFragmentManager().beginTransaction().replace(R.id.brandContainer, new BrandDogFragment()).commit();
                    currentChildFragment = 1;
                }
                break;
        }
    }

}
