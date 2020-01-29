package com.example.petrecog;

import android.os.Bundle;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentTransaction;

import com.melnykov.fab.FloatingActionButton;

public class MainActivity extends FragmentActivity implements View.OnClickListener {

    private LinearLayout tab1,tab2,tab3;
    private View currentSelectTab;
    private TextView tvTab1,tvTab2,tvTab3;//底部tab文字

    private Fragment currentFragment;
    private BrandFragment brandFragment = new BrandFragment();
    private BodyLanguageFragment bodyLanguageFragment = new BodyLanguageFragment();

    FloatingActionButton fab;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initView();

        selectFragment(brandFragment);
        selectView(tab1);

    }

    private void initView() {

        tab1 = (LinearLayout) findViewById(R.id.tab1);
        tab2 = (LinearLayout) findViewById(R.id.tab2);
        tab3 = (LinearLayout) findViewById(R.id.tab3);
        tvTab1 = (TextView) findViewById(R.id.tvTab1);
        tvTab2 = (TextView) findViewById(R.id.tvTab2);
        tvTab3 = (TextView) findViewById(R.id.tvTab3);

        tab1.setOnClickListener(this);
        tab2.setOnClickListener(this);
        tab3.setOnClickListener(this);

        fab = (FloatingActionButton)findViewById(R.id.fab);
        fab.setOnClickListener(v -> CameraManager.getInst().openCamera(MainActivity.this));
    }

    private void selectFragment(Fragment fragment){
        if(currentFragment == null){
            FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
            //将Fragment加入到容器中
            transaction.add(R.id.fragmentContainer, fragment).commit();
            currentFragment = fragment;
        }else{
            if(currentFragment != fragment){
                FragmentTransaction transaction =getSupportFragmentManager().beginTransaction();
                /**
                 * 如果要切换到的Fragment没有被Fragment事务添加，则隐藏被切换的Fragment，添加要切换的Fragment,否则，则隐藏被切换的Fragment，显示要切换的Fragment
                 */
                if(!fragment.isAdded()){//如果Fragment没有添加add
                    transaction.hide(currentFragment).add(R.id.fragmentContainer, fragment).commitAllowingStateLoss();
                }else{
                    transaction.hide(currentFragment).show(fragment).commitAllowingStateLoss();
                }
                currentFragment = fragment;
            }

        }
    }

    /**
     * 选中时字体、图片颜色变化
     */
    private void selectView(View view){
        if(view == tab2){//发布按钮
            CameraManager.getInst().openCamera(MainActivity.this);
            return;
        }
        if(currentSelectTab != null){
            currentSelectTab.setSelected(false);
        }
        view.setSelected(true);//改变图片颜色
        currentSelectTab = view;

        if(view == tab1){
            tvTab1.setSelected(true);
            tvTab3.setSelected(false);
        }else if(view == tab3){
            tvTab1.setSelected(false);
            tvTab3.setSelected(true);
        }
    }

    @Override
    public void onClick(View v) {
        selectView(v);

        switch (v.getId()) {
            case R.id.tab1:
                selectFragment(brandFragment);
                break;
            case R.id.tab3:
                selectFragment(bodyLanguageFragment);
                break;
        }
    }
}
