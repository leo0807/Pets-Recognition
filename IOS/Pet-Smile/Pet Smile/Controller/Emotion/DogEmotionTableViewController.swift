//
//  DogEmotionTableViewController.swift
//  Pet Smile
//
//  Created by Scott on 13/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit
import SQLite
import SQLite3
struct DogEmotionData {
    let image: UIImage?
    let breedName: String?
    let description:String?
    
    
}
class DogEmotionTableViewController: UITableViewController {
    
    var index = 0
    var data = [DogEmotionData]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        do {
            let databasePath = Bundle.main.path(forResource: "myDatabase", ofType: "db")!
            
            let db = try? Connection(databasePath) //Connection(databasePath, readonly: true)
            let table = Table("EmotionDog")
            
            let breed = Expression<String>("Breed")
            let description = Expression<String>("Description")
            let pic = Expression<String>("Picture")
            
            for i in try! (db?.prepare(table))!{
                
                data.append(DogEmotionData.init(image: base64Convert(base64String: i[pic]), breedName: i[breed], description: i[description]))
            }
            
        }
        
        self.tableView.register(CustomCell.self, forCellReuseIdentifier: "custom")
        self.tableView.rowHeight = UITableView.automaticDimension
        self.tableView.estimatedRowHeight = 200
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "custom") as! CustomCell
        cell.mainImage = data[indexPath.row].image
        cell.message = data[indexPath.row].breedName
        customizeCell(cell)
        return cell
    }
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return data.count
    }
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        //myIndex = indexPath.row
        index = indexPath.row
        performSegue(withIdentifier: "dogEmotionSegue", sender: self)
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is DogEmotionViewController{
            let vc = segue.destination as? DogEmotionViewController
            vc?.breed = data[index].breedName!
            vc?.dogImg = data[index].image!
            vc?.descriptionText = data[index].description!
        }
    }
    
}

func base64Convert(base64String: String?) -> UIImage{
    if (base64String?.isEmpty)! {
        return #imageLiteral(resourceName: "no_image_found")
    }else {
        // !!! Separation part is optional, depends on your Base64String !!!
        let temp = base64String?.components(separatedBy: ",")
        var index = 0
        if temp?.count ?? 0 > 1{
            index = 1
        }
        let dataDecoded : Data = Data(base64Encoded: temp![index], options: .ignoreUnknownCharacters)!
        let decodedimage = UIImage(data: dataDecoded)
        return decodedimage!
    }
}
