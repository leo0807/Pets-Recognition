//
//  CatTableViewController.swift
//  Pet Smile
//
//  Created by Scott on 12/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit
struct CatData {
    let breedName: String?

    let breedOverview: String?
    let image: UIImage?
}
class CatTableViewController: UITableViewController {
    var data = [CatData]()
    var index = 0
    override func viewDidLoad() {
        super.viewDidLoad()
        let filePath = "CatBreedsBowWowMeowP"
        let inputData = CSVparser(filePath)
        for i in inputData{
           // print(i.count)
           // print(i)
            let url = URL(string: i[3])// img_src
            let dataImg = try? Data(contentsOf: url!)
            data.append(CatData.init(breedName: i[0], breedOverview: i[2], image: UIImage(data: dataImg!)))//breed name
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
        performSegue(withIdentifier: "catSegue", sender: self)
        //let storyBoard = UIStoryboard(name: "main", bundle: nil)
        
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.destination is CatDetailViewController{
            let vc = segue.destination as? CatDetailViewController
            vc?.breedName = data[index].breedName!
            vc?.petImage = data[index].image!
            if let breedoverview = data[index].breedOverview{
                vc?.breedOverview = breedoverview
            }

        }
    }
}
