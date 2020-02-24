package com.example.petrecog.ui;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.text.Spannable;
import android.text.SpannableStringBuilder;
import android.text.TextPaint;
import android.text.method.LinkMovementMethod;
import android.text.style.ClickableSpan;
import android.util.Base64;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import com.example.petrecog.model.HistoryItem;
import com.example.petrecog.database.HistoryItemRepo;
import com.example.petrecog.R;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static android.app.PendingIntent.getActivity;

/**
 * This is the PhotoProcessActivity of PetRecog Application
 * Navigate from: Camera Activity
 * Navigate to  : BreedDetail Activity
 *
 * @author  LinYun Li
 */
public class PhotoProcessActivity extends AppCompatActivity {

    ImageView mImageShow;
    TextView mPet_text;
    TextView mBrand_text;
    TextView mEmotion_text;
    TextView mBrand_predict_text;
    TextView mEmotion_predict_text;
    Button mSave_btn;

    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    public static String mRes = null;
    public Bitmap mData = null;

    private boolean mSavedFlag = false;
    private boolean mDeletedFlag = false;
    private boolean isHistoryDisplay = false;

    private ProgressDialog waitingDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_photo_process);

        waitingDialog = new ProgressDialog(this);

        if(getIntent().getIntExtra("input_type", 0) == 1){
            isHistoryDisplay = true;
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
        ActionBar actionBar = getSupportActionBar();
        if(actionBar != null){
            actionBar.setHomeButtonEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
            if(isHistoryDisplay){
                actionBar.setTitle(getIntent().getStringExtra("date"));
            }
            else{
                actionBar.setTitle("Predict");
            }
        }

        mImageShow =  findViewById(R.id.imageShow);
        mPet_text =  findViewById(R.id.pet_text);
        mBrand_text =  findViewById(R.id.brand_text);
        mBrand_predict_text = findViewById(R.id.brand_predict_text);
        mEmotion_text =  findViewById(R.id.emotion_text);
        mEmotion_predict_text = findViewById(R.id.emotion_predict_text);
        mSave_btn = findViewById(R.id.save_btn);

        mPet_text.setText("");
        mBrand_text.setText("");
        mBrand_predict_text.setText("");
        mEmotion_text.setText("");
        mEmotion_predict_text.setText("");

        if(!isHistoryDisplay) {
            mImageShow.setImageURI(getIntent().getData());

            mSave_btn.setText("Save");
        }
        else{
            mImageShow.setImageBitmap(getBitmapFromDb(getIntent().getIntExtra("id", 0)));

            mSave_btn.setText("Delete");
        }

        mSave_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!isHistoryDisplay) {
                    if (mRes == null){
                        Toast.makeText(getBaseContext(), "No Available Data For Saving!!", Toast.LENGTH_LONG).show();
                    }
                    else if (mSavedFlag == true) {
                        Toast.makeText(getBaseContext(), "Already Saved!", Toast.LENGTH_LONG).show();
                    } else {
                        showWaitingDialog();
                        save2db(mRes);
                        mSavedFlag = true;
                        dismissWaitingDialog();
                        showNormalDialog();
                    }
                }
                else{
                    if (mDeletedFlag == true) {
                        Toast.makeText(getBaseContext(), "Already Deleted!", Toast.LENGTH_LONG).show();
                    } else {
                        showDeleteDialog();
                    }
                }
            }
        });

        if(!isHistoryDisplay) {
            showWaitingDialog();
            uploadImageUri(getIntent().getData());

        }
        else{
            try {
                analyzeResponse(getIntent().getStringExtra("description"));
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    public static byte[] Bitmap2Bytes(Bitmap bm) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.PNG, 100, baos);
        return baos.toByteArray();
    }

    private void post(String json){
        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build();

        String url = "http://101.116.13.138/predict";
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder().url(url).post(body).build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
                responseTimeout();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    String myResponse = response.body().string();
                    try {
                        analyzeResponse(myResponse);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
                else{
                    responseFiled(response.message());
                }
            }
        });
    }

    /**
     * Analyze the Response from Server
     * @param jsonStr JSON Sting, Response from Server
     * @throws JSONException
     */
    private void analyzeResponse(String jsonStr) throws JSONException {
        mRes = jsonStr;
        JSONObject jsonObject = new JSONObject(jsonStr);
        String petName = jsonObject.getString("pet");
        String breedName = jsonObject.getString("breed");
        String emotion = jsonObject.getString("emotion");

        String[] breeds = breedName.split("\n");
        String[] breedNameOnly = new String[breeds.length];
        String[] breedPredictOnly = new String[breeds.length];
        breedName = "";
        String breedPredict = "";
        int[] index = new int[breeds.length];
        int i = 0;
        for(String breed : breeds){
            String str = breed.trim().replaceAll(" +", " ");
            breedNameOnly[i] = str.split(" ")[0];
            breedPredictOnly[i] = str.split(" ")[1];
            breedName += breedNameOnly[i] + "\n";
            breedPredict += breedPredictOnly[i] + "\n";
            index[i] = breedName.indexOf(breedNameOnly[i]);
            i += 1;
        }


        String[] emotions = emotion.split("\n");
        String[] emotionNameOnly = new String[emotions.length];
        String[] emotionPredictOnly = new String[emotions.length];
        emotion = "";
        String emotionPredict = "";
        int[] indexe = new int[emotions.length];
        int x = 0;
        for(String emo : emotions){
            String str = emo.trim().replaceAll(" +", " ");
            emotionNameOnly[x] = str.split(" ")[0];
            emotionPredictOnly[x] = str.split(" ")[1];
            emotion += emotionNameOnly[x] + "\n";
            emotionPredict += emotionPredictOnly[x] + "\n";
            indexe[x] = emotion.indexOf(emotionNameOnly[x]);
            x += 1;
        }

        String breedName1 = breedName;
        String emotion1 = emotion;
        String breedPredict1 = breedPredict;
        String emotionPredict1 = emotionPredict;

        SpannableStringBuilder spannableStringBuilder = new SpannableStringBuilder(breedName1);
        for(int j=0; j < breedNameOnly.length; j++){
            final String name = breedNameOnly[j];
            spannableStringBuilder.setSpan(new ClickableSpan() {
                @Override
                public void onClick(View widget) {
                    openDetailActivity(petName, name);
                }

                @Override
                public void updateDrawState(TextPaint ds) {
                    super.updateDrawState(ds);
                    ds.setColor(Color.BLUE);
                    ds.setUnderlineText(false);
                }
            },index[j],index[j] + breedNameOnly[j].length(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
        }

        SpannableStringBuilder span = new SpannableStringBuilder(emotion1);
        for(int y=0; y < emotionNameOnly.length; y++){
            final String name = emotionNameOnly[y];
            span.setSpan(new ClickableSpan() {
                @Override
                public void onClick(View widget) {
                    openDetailActivity("Emotion"+petName, name);
                }

                @Override
                public void updateDrawState(TextPaint ds) {
                    super.updateDrawState(ds);
                    ds.setColor(Color.BLUE);
                    ds.setUnderlineText(false);
                }
            },indexe[y],indexe[y] + emotionNameOnly[y].length(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
        }


        PhotoProcessActivity.this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mPet_text.setText(petName);
                mBrand_text.setText(spannableStringBuilder);
                mBrand_text.setMovementMethod(LinkMovementMethod.getInstance());
                mEmotion_text.setText(span);
                mEmotion_text.setMovementMethod(LinkMovementMethod.getInstance());

                mBrand_predict_text.setText(breedPredict1);
                mEmotion_predict_text.setText(emotionPredict1);

                dismissWaitingDialog();
            }
        });
    }

    private void responseFiled(String response){
        PhotoProcessActivity.this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String str = "Analyze Filed, Please Retry!";
                mPet_text.setText(str);
                mBrand_text.setText("Error" + response);
                mEmotion_text.setText(str);
                dismissWaitingDialog();
            }
        });
    }

    private void responseTimeout(){
        PhotoProcessActivity.this.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String str = "Analyze Filed, Please Retry!";
                mPet_text.setText(str);
                mBrand_text.setText("Request Timeout, Please Retry");
                mEmotion_text.setText(str);
                dismissWaitingDialog();
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
                mData = bitmap;

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

    private void openDetailActivity(String table, String breedName){
        Intent newIntent = new Intent(this.getBaseContext(), BreedDetailActivity.class);
        newIntent.putExtra("breed", breedName);
        newIntent.putExtra("input_type", 1);
        newIntent.putExtra("table", table);
        startActivity(newIntent);
    }

    private void save2db(String jsonStr){
        HistoryItemRepo repo = new HistoryItemRepo(this);
        int id = repo.getNextId();

        HistoryItem historyItem = new HistoryItem();
        historyItem.ID = id;
        historyItem.description = jsonStr;
        historyItem.picture = mData;

        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        Date date = new Date(System.currentTimeMillis());
        historyItem.date = simpleDateFormat.format(date);

        repo.insert(historyItem);

    }

    private void deleteFromDb(int id){
        HistoryItemRepo repo = new HistoryItemRepo(this);
        repo.delete(id);
    }

    private Bitmap getBitmapFromDb(int id){
        HistoryItemRepo repo = new HistoryItemRepo(this);
        return repo.getBitmap(id);
    }

    private void showNormalDialog(){
        final AlertDialog.Builder normalDialog =
                new AlertDialog.Builder(this);
        normalDialog.setTitle("Save State");
        normalDialog.setMessage("Saved Successfully!");
        normalDialog.setPositiveButton("OK",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                        ;
                    }
                });
        normalDialog.show();
    }

    private void showDeleteDialog(){
        final AlertDialog.Builder normalDialog =
                new AlertDialog.Builder(this);
        normalDialog.setTitle("Delete");
        normalDialog.setMessage("Are you sure to delete this history record ?");
        normalDialog.setPositiveButton("Sure",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                        deleteFromDb(getIntent().getIntExtra("id", 0));
                        mDeletedFlag = true;
                        Toast.makeText(getBaseContext(),"Delete Successfully!", Toast.LENGTH_LONG).show();
                        finish();
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

    private void showWaitingDialog() {
        waitingDialog.setTitle("");
        waitingDialog.setMessage("Processing...... Please wait");
        waitingDialog.setIndeterminate(true);
        waitingDialog.setCancelable(false);
        waitingDialog.show();
    }

    private void dismissWaitingDialog() {

        waitingDialog.dismiss();
    }

    @Override
    protected void onDestroy() {
        mSavedFlag = false;
        super.onDestroy();
    }
}
