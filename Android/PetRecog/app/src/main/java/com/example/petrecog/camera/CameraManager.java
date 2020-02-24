package com.example.petrecog.camera;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;

import com.example.petrecog.AppConstants;
import com.example.petrecog.utils.ImageUtils;
import com.example.petrecog.model.PhotoItem;
import com.example.petrecog.ui.CameraActivity;
import com.example.petrecog.ui.CropPhotoActivity;
import com.example.petrecog.ui.PhotoProcessActivity;

import java.util.Stack;

public class CameraManager {

    private static CameraManager mInstance;
    private Stack<Activity> cameras = new Stack<Activity>();

    public static CameraManager getInst() {
        if (mInstance == null) {
            synchronized (CameraManager.class) {
                if (mInstance == null)
                    mInstance = new CameraManager();
            }
        }
        return mInstance;
    }

    //open camera
    public void openCamera(Context context) {
        Intent intent = new Intent(context, CameraActivity.class);
        context.startActivity(intent);
    }

    //judge whether crop photo
    public void processPhotoItem(Activity activity, PhotoItem photo) {
        Uri uri = photo.getImageUri().startsWith("file:") ? Uri.parse(photo
                .getImageUri()) : Uri.parse("file://" + photo.getImageUri());
//        Uri uri = Uri.parse(photo.getImageUri());
        if (ImageUtils.isSquare(photo.getImageUri())) {
            Intent newIntent = new Intent(activity, PhotoProcessActivity.class);
            newIntent.setData(uri);
            activity.startActivity(newIntent);
        } else {
            Intent i = new Intent(activity, CropPhotoActivity.class);
            i.setData(uri);

            activity.startActivityForResult(i, AppConstants.REQUEST_CROP);
        }
    }

    public void close() {
        for (Activity act : cameras) {
            try {
                act.finish();
            } catch (Exception e) {

            }
        }
        cameras.clear();
    }

}
