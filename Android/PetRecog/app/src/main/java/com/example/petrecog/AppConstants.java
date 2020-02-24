package com.example.petrecog;

import android.os.Environment;

/**
 * Some constants for PetRecog App
 */
public class AppConstants {

    public static final String APP_DIR                    = Environment.getExternalStorageDirectory() + "/PetRecog";
    public static final String APP_TEMP                   = APP_DIR + "/temp";
    public static final String APP_IMAGE                  = APP_DIR + "/image";



    public static final int REQUEST_CROP = 6709;
    public static final int REQUEST_PICK = 9162;
    public static final int RESULT_ERROR = 404;

}
