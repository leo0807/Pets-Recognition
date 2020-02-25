//
//  PhotoViewController.swift
//  Clima
//
//  Created by Junxu ZHANG on 30/1/20.
//  Copyright © 2020 App Brewery. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
import Foundation
import SQLite
import SQLite3

class PhotoViewController: UIViewController {
    
    var takenPhoto: UIImage?
    
    @IBOutlet weak var processLabel: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var categoryLabelOne: UILabel!
    @IBOutlet weak var categoryLabelTwo: UILabel!
    @IBOutlet weak var categoryLabelThree: UILabel!
    
    let urlString = "http://192.168.56.1:5000/predict"
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if let avaliableImage = takenPhoto{
            
            imageView.image = avaliableImage
            imageInitialization(imageView)
            if let imageData = avaliableImage.pngData(){
                let img = imageData.base64EncodedString()
                upload(url: urlString, param: ["image": img])
                print("upload Image completed")
            }
        }
    }
    
    @IBAction func goBack(_ sender: UIButton) {
        self.dismiss(animated: true, completion: nil)
    }
    @IBAction func photoDone(_ sender: UIButton) {
        performSegue(withIdentifier: "historyTableSegue", sender: nil)

    }
    

    func upload( url: String, param: [String: Any]){
        AF.request(url, method: .post, parameters: param, encoding: JSONEncoding.default, headers: nil, interceptor: nil)
            
            .responseJSON { (response) in
                if let data = response.data, let utf8Text = String(data: data, encoding: .utf8) {
                    print("Data: \(utf8Text)") // original server data as UTF8 string
                    do{
                        // Get json data
                        if let json = try? JSON(data: data){
                            
                            var emotionContent:String = ""
                            var breedContent: String = ""
                            DispatchQueue.main.async {
                                for (key, subJson) in json {
                                    if key == "emotion"{
                                        emotionContent += split(subJson.stringValue)
                                        
                                    }else if key == "breed"{
                                        breedContent += split(subJson.stringValue)
                                    }
                                }
                                
                                self.categoryLabelOne.text = "Pet: \(json["pet"].string!)"
                                self.categoryLabelTwo.text = "Breed:\(breedContent)"
                                self.categoryLabelThree.text = "Emotion:\(emotionContent)"
                                self.processLabel.text = "Completed"
                                
                                do {
                                    // Connect the database
                                    let path = NSSearchPathForDirectoriesInDomains(
                                        .documentDirectory, .userDomainMask, true
                                    ).first!

                                    let db = try? Connection("\(path)/myDatabase.db")
                                    let table = Table("PhotoHistory")
                                    //Row name
                                    let id = Expression<Int64>("Id")
                                    let pet = Expression<String>("Pet")
                                    let breed = Expression<String>("Breed")
                                    let emotion = Expression<String>("Emotion")
                                    let picture = Expression<String>("Picture")
                                    
                                    let date = Date()
                                    let format = DateFormatter()
                                    format.dateFormat = "yyyy-MM-dd HH:mm:ss"
                                    let formattedDate = format.string(from: date)
                                    let imgDate = Expression<String>("Date")
                                    
                                    if (try? db?.prepare(table)) != nil{
                                        do{
                                            print("Write to Table1")
                                            try! db?.run(table.insert(pet <- json["pet"].string!,breed <- breedContent, emotion <- emotionContent, picture <- self.imageView.image!.toBase64()!, imgDate <- formattedDate))
                                        }
                                    }else{
                                        // If there is no such a table, create a new one
                                        print("Create Table")
                                        try! db?.run(table.create { t in    // CREATE TABLE "History" (
                                            t.column(id, primaryKey: true) //     "id" INTEGER PRIMARY KEY NOT NULL,
                                            t.column(pet)
                                            t.column(breed)  //     "email" TEXT UNIQUE NOT NULL,
                                            t.column(emotion)
                                            t.column(picture)
                                            t.column(imgDate)//     "name" TEXT
                                        })
                                        //Write data to table
                                        do{
                                            print("Write to Table2")
                                            try! db?.run(table.insert(pet <- json["pet"].string!,breed <- breed, emotion <- emotion, picture <- self.imageView.image!.toBase64()!,imgDate <- formattedDate))
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
        }
    }
    //Customize the shown image
    func imageInitialization(_ image: UIImageView) {
        imageView.layer.borderWidth = 4.0
        imageView.layer.masksToBounds = false
        imageView.layer.borderColor = UIColor.white.cgColor
        imageView.layer.cornerRadius = imageView.frame.size.width / 2
        imageView.clipsToBounds = true
    }
    
}

//Reseponse data processing
func split(_ input: String) -> String{
    var result:String = ""
    let removeNewline = input.filter {!$0.isNewline}
    let removeSpace : [String] = removeNewline.components(separatedBy: " ")
    let removeEmpty = removeSpace.filter {!$0.isEmpty}
    let maxLength = removeEmpty.max(by: {$1.count > $0.count})!.count
    
    for item in removeEmpty{
        if let number = Double(item){
            result = result + String(format: "%.2f",number * 100) + "%\n"
        }
        else{
            let itemLength = item.count
            let space = String(repeatElement(" ", count: maxLength - itemLength))
            let removeUnderline = item.components(separatedBy: "_").joined(separator: " ").capitalized
            
            result = result + removeUnderline + space + " "
        }
    }
    return result
}

