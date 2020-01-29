package com.example.petrecog;

import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class PhotoProcessActivity extends AppCompatActivity {

    ImageView mimageShow;
    TextView mbrand_text;
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_photo_process);

        ActionBar actionBar = getSupportActionBar();
        if(actionBar != null){
            actionBar.setHomeButtonEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
        }

        initView();
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

    private void initView()
    {
        mimageShow = (ImageView) findViewById(R.id.imageShow);
        mimageShow.setImageURI(getIntent().getData());

        mbrand_text = (TextView) findViewById(R.id.brand_text);

        uploadImageUri(getIntent().getData());

        //debug(bowlingJson("Jesse", "Jake"));


//        TODO upload()
    }

    String bowlingJson(String player1, String player2) {
        return "{'winCondition':'HIGH_SCORE',"
                + "'name':'Bowling',"
                + "'round':4,"
                + "'lastSaved':1367702411696,"
                + "'dateStarted':1367702378785,"
                + "'players':["
                + "{'name':'" + player1 + "','history':[10,8,6,7,8],'color':-13388315,'total':39},"
                + "{'name':'" + player2 + "','history':[6,10,5,10,10],'color':-48060,'total':41}"
                + "]}";
    }

    public byte[] Bitmap2Bytes(Bitmap bm) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.PNG, 100, baos);
        return baos.toByteArray();
    }

    private void post(String json){
        OkHttpClient client = new OkHttpClient();
        String url = "http://101.116.27.109/predict";
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder().url(url).post(body).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    String myResponse = response.body().string();

                    PhotoProcessActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mbrand_text.setText(myResponse);
                        }
                    });
                }
            }
        });
    }

    private void uploadImageUri(Uri uri){
        new Thread(){
            @Override
            public void run() {
                super.run();

                Bitmap bitmap = null;

                try {
                    bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                byte[] data = Bitmap2Bytes(bitmap);

                JSONObject body = new JSONObject();
                try {
                    body.put("image", Base64.encodeToString(data, 0));
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                post(body.toString());
            }
        }.start();
    }

    private void get(){
        OkHttpClient client = new OkHttpClient();
        String url = "https://reqres.in/api/users?page=2";
        Request request = new Request.Builder().url(url).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    String myResponse = response.body().string();

                    PhotoProcessActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mbrand_text.setText(myResponse);
                        }
                    });
                }
            }
        });
    }

    private void debug(String json){
        OkHttpClient client = new OkHttpClient();
        String url = "http://www.roundsapp.com/post";
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder().url(url).post(body).build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    String myResponse = response.body().string();

                    PhotoProcessActivity.this.runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mbrand_text.setText(myResponse);
                        }
                    });
                }
            }
        });
    }








}
