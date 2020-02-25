//
//  TableViewController.swift
//  Pet Smile
//
//  Created by Junxu ZHANG on 7/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

struct DogData {
    let image: UIImage?
    let breedName: String?
    let recommended:String?
    let lifeSpan: String?
    let maintence:String?
    let temperament:String?
    let healthRisk:String?
    let breedOverview:String?
}



//var myIndex = 0
class DogTableViewController: UITableViewController {
    
    var data = [DogData]()
    var index = 0
    override func viewDidLoad() {
        super.viewDidLoad()
        let filePath = "DogBreedsInformation"
        let inputData = CSVparser(filePath)
        for i in inputData{
            let url = URL(string: i[6])// img_src
            let dataImg = try? Data(contentsOf: url!)
            data.append(DogData.init(image: UIImage(data: dataImg!), breedName: i[0], recommended: i[1],lifeSpan: i[3], maintence: i[2],temperament: i[4], healthRisk: i[5], breedOverview: i[7]))//breed name
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
        performSegue(withIdentifier: "segue", sender: self)
        //let storyBoard = UIStoryboard(name: "main", bundle: nil)
        
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is DogDetailViewController{
            let vc = segue.destination as? DogDetailViewController
            vc?.breedName = data[index].breedName!
            vc?.petImage = data[index].image!
            if let healthrisk = data[index].healthRisk{
                vc?.healthRisk = healthrisk
            }
            if let breedoverview = data[index].breedOverview{
                vc?.breedOverview = breedoverview
            }
            if let maintence = data[index].maintence{
                vc?.maintence = maintence
            }
            if let lifespan = data[index].lifeSpan{
                vc?.lifespan = lifespan
            }
            if let recomended = data[index].recommended{
                vc?.recommended = recomended
            }
            if let temperament = data[index].temperament{
                vc?.temperament = temperament
            }
        }
}
}
