//
//  CatEmotionTableViewController.swift
//  Pet Smile
//
//  Created by Scott on 13/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit
import SQLite3
import SQLite
struct CatEmotionData {
    let image: UIImage?
    let breedName: String?
    let description:String?
}

class CatEmotionTableViewController: UITableViewController {
    var index = 0
    var data = [CatEmotionData]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        do {
            let databasePath = Bundle.main.path(forResource: "myDatabase", ofType: "db")!
            
            let db = try? Connection(databasePath) //Connection(databasePath, readonly: true)
            let table = Table("EmotionCat")
            
            let breed = Expression<String>("Breed")
            let description = Expression<String>("Description")
            let pic = Expression<String>("Picture")
            
            for i in try! (db?.prepare(table))!{
                
                data.append(CatEmotionData.init(image: base64Convert(base64String: i[pic]), breedName: i[breed], description: i[description]))
            }
            
        }
        
        self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: "custom")
        tableView.delegate = self
        tableView.dataSource = self
        self.tableView.register(CustomCell.self, forCellReuseIdentifier: "custom")
        self.tableView.rowHeight = UITableView.automaticDimension
        self.tableView.estimatedRowHeight = 200

    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "custom", for: indexPath) as! CustomCell
        cell.mainImage = data[indexPath.row].image
        cell.message = data[indexPath.row].breedName
        customizeCell(cell)
        //cell.layer.shadowOffset = CGSize(width: -1, height: 1)
//
        
        
        
        
        return cell
    }
    override func tableView(_ tableView: UITableView, willDisplay cell: UITableViewCell, forRowAt indexPath: IndexPath) {
        cell.backgroundColor = UIColor.clear
    }
        
    override func tableView(_ tableView: UITableView, estimatedHeightForHeaderInSection section: Int) -> CGFloat {
        return cellSpacingHeight
    }
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return data.count
    }
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        //myIndex = indexPath.row
        index = indexPath.row
    
        performSegue(withIdentifier: "catEmotionSegue", sender: self)
        
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        //Past current UIViewController to CatEmotionController
        if segue.destination is CatEmotionViewController{
            let vc = segue.destination as? CatEmotionViewController
            vc?.breed = data[index].breedName!
            vc?.catImg = data[index].image!
            vc?.descriptionText = data[index].description!
        }
    }
    
}

func setTableViewBackgroundGradient(sender: UITableViewController, _ topColor:UIColor, _ bottomColor:UIColor) {

    let gradientBackgroundColors = [topColor.cgColor, bottomColor.cgColor]
    let gradientLocations = [0.0,1.0]

    let gradientLayer = CAGradientLayer()
    gradientLayer.colors = gradientBackgroundColors
    gradientLayer.locations = gradientLocations as [NSNumber]

    gradientLayer.frame = sender.tableView.bounds
    let backgroundView = UIView(frame: sender.tableView.bounds)
    backgroundView.layer.insertSublayer(gradientLayer, at: 0)
    sender.tableView.backgroundView = backgroundView
}

