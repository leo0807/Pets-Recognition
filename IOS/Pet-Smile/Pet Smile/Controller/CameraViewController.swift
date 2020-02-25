//
//  PhotoViewController.swift
//  Clima
//
//  Created by Junxu ZHANG on 30/1/20.
//  Copyright © 2020 App Brewery. All rights reserved.
//

import UIKit
import AVFoundation
import Photos
import Alamofire
import SQLite
import SQLite3

class CameraViewController: UIViewController,AVCapturePhotoCaptureDelegate,UINavigationControllerDelegate,  UIImagePickerControllerDelegate {
    
    var imagePicker:UIImagePickerController!
    var assetsFetchResults:PHFetchResult<PHAsset>!
    var imageManager:PHCachingImageManager!
    var assetGridThumbnailSize:CGSize!
    
    
    @IBOutlet weak var imageView: UIImageView!
 
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        imagePicker = UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.allowsEditing = true
        imageView.layer.borderWidth = 1.0
        imageView.layer.borderColor = UIColor.white.cgColor
        
    }
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        // This delegate is used to listen whether choose the picked (or taked) image
        if let avaliableImage = info[.editedImage] as? UIImage{
            //print("enter")
            imageView.image = avaliableImage
            let photoVC : PhotoViewController = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "PhotoVC") as! PhotoViewController
            photoVC.takenPhoto = avaliableImage
            self.dismiss(animated: true, completion: nil)
            self.present(photoVC, animated: true, completion: nil)
            // Once data takenm, transfer to database
            
        }
        
    }
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        //Listen of cancel operation, when tap cancel in photo libray of take photo
        self.dismiss(animated: true, completion: nil)
    }
    
    
    @IBAction func imageCapture(_ sender: UIButton) {
        
        let alert = UIAlertController(title: "Choose Image", message: nil, preferredStyle: .actionSheet)
        alert.addAction(UIAlertAction(title: "Camera", style: .default, handler: { _ in
            self.openCamera()
        }))

        alert.addAction(UIAlertAction(title: "Gallery", style: .default, handler: { _ in
            self.openGallary()
        }))
        alert.addAction(UIAlertAction(title: "Video Camera", style: .default, handler: { _ in
            self.performSegue(withIdentifier: "videoSegue", sender: self)
        }))
        alert.addAction(UIAlertAction.init(title: "Cancel", style: .cancel, handler: nil))

        /*If you want work actionsheet on ipad
        then you have to use popoverPresentationController to present the actionsheet,
        otherwise app will crash on iPad */
        switch UIDevice.current.userInterfaceIdiom {
        case .pad:
            alert.popoverPresentationController?.sourceView = sender
            alert.popoverPresentationController?.sourceRect = sender.bounds
            alert.popoverPresentationController?.permittedArrowDirections = .up
        default:
            break
        }
        self.present(alert, animated: true, completion: nil)
        //imagePicker.sourceType = .camera
        //Take pictire
        //present(imagePicker, animated: true, completion: nil)
    }
    
    func openCamera()
    {
        if(UIImagePickerController .isSourceTypeAvailable(UIImagePickerController.SourceType.camera))
        {
            imagePicker.sourceType = UIImagePickerController.SourceType.camera
            imagePicker.allowsEditing = true
            self.present(imagePicker, animated: true, completion: nil)
        }
        else
        {
            let alert  = UIAlertController(title: "Warning", message: "You don't have camera", preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
            self.present(alert, animated: true, completion: nil)
        }
    }

    func openGallary()
    {
        imagePicker.sourceType = UIImagePickerController.SourceType.photoLibrary
        imagePicker.allowsEditing = true
        self.present(imagePicker, animated: true, completion: nil)
    }

}



extension UIImage {
    func toBase64() -> String? {
        guard let imageData = self.pngData() else { return nil }
        return imageData.base64EncodedString(options: Data.Base64EncodingOptions.lineLength64Characters)
    }
}



