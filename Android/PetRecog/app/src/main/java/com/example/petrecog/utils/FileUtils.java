package com.example.petrecog.utils;

import android.content.Context;
import android.content.res.AssetManager;
import android.os.Environment;

import com.example.petrecog.App;
import com.example.petrecog.model.PhotoItem;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;

public class FileUtils {

    private static String    BASE_PATH;
    private static String    STICKER_BASE_PATH;

    private static FileUtils mInstance;

    public static FileUtils getInst() {
        if (mInstance == null) {
            synchronized (FileUtils.class) {
                if (mInstance == null) {
                    mInstance = new FileUtils();
                }
            }
        }
        return mInstance;
    }

    public File getExtFile(String path) {
        return new File(BASE_PATH + path);
    }

    /**
     * Get the size of the Folder
     * @param file File instant
     * @return long Size (the unit is K)
     * @throws Exception
     */
    public long getFolderSize(File file) {
        try {
            long size = 0;
            if (!file.exists()) {
                return size;
            } else if (!file.isDirectory()) {
                return file.length() / 1024;
            }
            File[] fileList = file.listFiles();
            for (int i = 0; i < fileList.length; i++) {
                if (fileList[i].isDirectory()) {
                    size = size + getFolderSize(fileList[i]);
                } else {
                    size = size + fileList[i].length();
                }
            }
            return size / 1024;
        } catch (Exception e) {
            return 0;
        }
    }


    public String getBasePath(int packageId) {
        return STICKER_BASE_PATH + packageId + "/";
    }


    //读取assets文件
    public String readFromAsset(String fileName) {
        InputStream is = null;
        BufferedReader br = null;
        try {
            is = App.getApp().getAssets().open(fileName);
            br = new BufferedReader(new InputStreamReader(is));
            String addonStr = "";
            String line = br.readLine();
            while (line != null) {
                addonStr = addonStr + line;
                line = br.readLine();
            }
            return addonStr;
        } catch (Exception e) {
            return null;
        } finally {
            IOUtil.closeStream(br);
            IOUtil.closeStream(is);
        }
    }

    public void removeAddonFolder(int packageId) {
        String filename = getBasePath(packageId);
        File file = new File(filename);
        if (file.exists()) {
            delete(file);
        }
    }

    public void delete(File file) {
        if (file.isFile()) {
            file.delete();
            return;
        }

        if (file.isDirectory()) {
            File[] childFiles = file.listFiles();
            if (childFiles == null || childFiles.length == 0) {
                file.delete();
                return;
            }

            for (int i = 0; i < childFiles.length; i++) {
                delete(childFiles[i]);
            }
            file.delete();
        }
    }

    public String getPhotoSavedPath() {
        return BASE_PATH + "stickercamera";
    }

    public String getPhotoTempPath() {
        return BASE_PATH + "stickercamera";
    }

    public String getSystemPhotoPath() {
        return Environment.getExternalStorageDirectory().getAbsolutePath() + "/DCIM/Camera";
    }


    private FileUtils() {
        String sdcardState = Environment.getExternalStorageState();
        //save to cache it no SD card
        if (Environment.MEDIA_MOUNTED.equals(sdcardState)) {
            BASE_PATH = Environment.getExternalStorageDirectory().getAbsolutePath()
                        + "/PetRecog/";
        } else {
            BASE_PATH = App.getApp().getCacheDirPath();
        }

        STICKER_BASE_PATH = BASE_PATH + "/pets/";
    }

    public boolean createFile(File file) {
        try {
            if (!file.getParentFile().exists()) {
                mkdir(file.getParentFile());
            }
            return file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean mkdir(File file) {
        while (!file.getParentFile().exists()) {
            mkdir(file.getParentFile());
        }
        return file.mkdir();
    }

    public boolean writeSimpleString(File file, String string) {
        FileOutputStream fOut = null;
        try {
            fOut = new FileOutputStream(file);
            fOut.write(string.getBytes());
            return true;
        } catch (Throwable e) {
            e.printStackTrace();
            return false;
        } finally {
            IOUtil.closeStream(fOut);
        }
    }

    public String readSimpleString(File file) {
        StringBuffer sb = new StringBuffer();
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(file));

            String line = br.readLine();
            if (StringUtils.isNotEmpty(line)) {
                sb.append(line.trim());
                line = br.readLine();
            }
        } catch (Throwable e) {
            e.printStackTrace();
            return "";
        } finally {
            IOUtil.closeStream(br);
        }
        return sb.toString();
    }

    //Relative paths
    public boolean copyAssetDirToFiles(Context context, String dirname) {
        try {
            AssetManager assetManager = context.getAssets();
            String[] children = assetManager.list(dirname);
            for (String child : children) {
                child = dirname + '/' + child;
                String[] grandChildren = assetManager.list(child);
                if (0 == grandChildren.length)
                    copyAssetFileToFiles(context, child);
                else
                    copyAssetDirToFiles(context, child);
            }
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    //Relative paths
    public boolean copyAssetFileToFiles(Context context, String filename) {
        return copyAssetFileToFiles(context, filename, getExtFile("/" + filename));
    }

    private boolean copyAssetFileToFiles(Context context, String filename, File of) {
        InputStream is = null;
        FileOutputStream os = null;
        try {
            is = context.getAssets().open(filename);
            createFile(of);
            os = new FileOutputStream(of);

            int readedBytes;
            byte[] buf = new byte[1024];
            while ((readedBytes = is.read(buf)) > 0) {
                os.write(buf, 0, readedBytes);
            }
            os.flush();
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        } finally {
            IOUtil.closeStream(is);
            IOUtil.closeStream(os);
        }
    }

    public boolean renameDir(String oldDir, String newDir) {
        File of = new File(oldDir);
        File nf = new File(newDir);
        return of.exists() && !nf.exists() && of.renameTo(nf);
    }

    /**  
     * Copy single file
     */
    public void copyFile(String oldPath, String newPath) {
        InputStream inStream = null;
        FileOutputStream fs = null;
        try {
            int bytesum = 0;
            int byteread = 0;
            File oldfile = new File(oldPath);
            if (oldfile.exists()) {
                inStream = new FileInputStream(oldPath);
                fs = new FileOutputStream(newPath);
                byte[] buffer = new byte[1444];
                while ((byteread = inStream.read(buffer)) != -1) {
                    bytesum += byteread; //Bytes  Size of file
                    System.out.println(bytesum);
                    fs.write(buffer, 0, byteread);
                }
            }
        } catch (Exception e) {
            System.out.println("Error while copy single file");
            e.printStackTrace();
        } finally {
            IOUtil.closeStream(inStream);
            IOUtil.closeStream(fs);
        }

    }

    public File getCacheDir() {
        return App.getApp().getCacheDir();
    }


    //Get PhotoItems from the path
    public ArrayList<PhotoItem> findPicsInDir(String path) {
        ArrayList<PhotoItem> photos = new ArrayList<PhotoItem>();
        File dir = new File(path);
        if (dir.exists() && dir.isDirectory()) {
            for (File file : dir.listFiles(new FileFilter() {

                @Override
                public boolean accept(File pathname) {
                    String filePath = pathname.getAbsolutePath();
                    return (filePath.endsWith(".png") || filePath.endsWith(".jpg") || filePath
                            .endsWith(".jepg"));
                }
            })) {
                photos.add(new PhotoItem(file.getAbsolutePath(), file.lastModified()));
            }
        }
        Collections.sort(photos);
        return photos;
    }


}
