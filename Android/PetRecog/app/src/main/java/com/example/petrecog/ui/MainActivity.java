package com.example.petrecog.ui;

import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentTransaction;

import com.example.petrecog.camera.CameraManager;
import com.example.petrecog.R;
import com.melnykov.fab.FloatingActionButton;

/**
 * This is the MainActivity of PetRecog Application
 * Navigate from: While opening the Application
 * Navigate to  : Camera Activity and Detail Activity
 *
 * @author  LinYun Li
 */
public class MainActivity extends FragmentActivity implements View.OnClickListener {

    private LinearLayout tab1,tab2,tab3;
    private View currentSelectTab;
    private TextView tvTab1,tvTab2,tvTab3;

    private Fragment currentFragment;
    private BrandFragment brandFragment = new BrandFragment();
    private BodyLanguageFragment bodyLanguageFragment = new BodyLanguageFragment();

    FloatingActionButton fab;

    private long firstTime = 0; //used for Double-click BACK key to quit

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initView();

        //Set the brandFragment as the default fragment
        selectFragment(brandFragment);
        selectView(tab1);

    }

    /**
     * Initial view
     */
    private void initView() {

        tab1 = findViewById(R.id.tab1);
        tab2 = findViewById(R.id.tab2);
        tab3 = findViewById(R.id.tab3);
        tvTab1 = findViewById(R.id.tvTab1);
        tvTab2 = findViewById(R.id.tvTab2);
        tvTab3 = findViewById(R.id.tvTab3);

        tab1.setOnClickListener(this);
        tab2.setOnClickListener(this);
        tab3.setOnClickListener(this);

        fab = findViewById(R.id.fab);
        //Click fab button to open Camera Activity
        fab.setOnClickListener(v -> CameraManager.getInst().openCamera(MainActivity.this));
    }

    /**
     * Load Specified Fragment into container
     * @param fragment Specified Fragment
     */
    private void selectFragment(Fragment fragment){
        if(currentFragment == null){
            FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
            transaction.add(R.id.fragmentContainer, fragment).commit();
            currentFragment = fragment;
        }else{
            if(currentFragment != fragment){
                FragmentTransaction transaction =getSupportFragmentManager().beginTransaction();

                if(!fragment.isAdded()){
                    transaction.hide(currentFragment).add(R.id.fragmentContainer, fragment).commitAllowingStateLoss();
                }else{
                    transaction.hide(currentFragment).show(fragment).commitAllowingStateLoss();
                }
                currentFragment = fragment;
            }

        }
    }

    /**
     * Change the image and text color when fragment changed
     */
    private void selectView(View view){
        if(currentSelectTab != null){
            currentSelectTab.setSelected(false);
        }
        view.setSelected(true);//Change select state to change image and text color
        currentSelectTab = view;

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.tab1:
                selectFragment(brandFragment);
                selectView(v);
                break;
            case R.id.tab3:
                selectFragment(bodyLanguageFragment);
                selectView(v);
                break;
            case R.id.tab2:
                CameraManager.getInst().openCamera(MainActivity.this);
                break;
        }
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {

        // Double click BACK key to quit the application
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            long secondTime = System.currentTimeMillis();
            if (secondTime - firstTime < 2000) {
                System.exit(0);
            } else {
                Toast.makeText(getApplicationContext(), "Press Back again to Quit!", Toast.LENGTH_SHORT).show();
                firstTime = System.currentTimeMillis();
            }

            return true;
        }

        return super.onKeyDown(keyCode, event);
    }
}
