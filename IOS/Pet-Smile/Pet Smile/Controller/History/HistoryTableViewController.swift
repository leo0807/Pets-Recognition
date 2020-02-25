//
//  HistoryTableViewController.swift
//  Pet Smile
//
//  Created by Scott on 18/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit
import SQLite
import SQLite3
struct History {
    let id: Int64?
    let pet: String?
    let breed: String?
    let emotion: String?
    let picture: UIImage?
    let date: String?
    
    
}
class HistoryTableViewController: UITableViewController {
    var index = 0
    var data = [History]()
    var length = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        do {
//            let databasePath = Bundle.main.path(forResource: "myDatabase", ofType: "db")!
//
//            let db = try? Connection(databasePath, readonly: true) //Connection(databasePath, readonly: true)
//            l\
            let path = NSSearchPathForDirectoriesInDomains(
                .documentDirectory, .userDomainMask, true
            ).first!

            let db = try? Connection("\(path)/myDatabase.db")
            let table = Table("PhotoHistory")
            //let id = Expression<Int64>("Id")
            let pet = Expression<String>("Pet")
            let breed = Expression<String>("Breed")
            let emotion = Expression<String>("Emotion")
            let picture = Expression<String>("Picture")
            let imgDate = Expression<String>("Date")
            let id = Expression<Int64>("Id")
            
            for i in try! ((db?.prepare(table))?.reversed())!{

                data.append(History.init(id: i[id], pet: i[pet], breed: i[breed], emotion: i[emotion], picture: base64Convert(base64String: i[picture]), date: i[imgDate]))
            }
            
        }
        
        self.tableView.register(CustomCell.self, forCellReuseIdentifier: "custom")
        self.tableView.rowHeight = UITableView.automaticDimension
        self.tableView.estimatedRowHeight = 200
    }
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = self.tableView.dequeueReusableCell(withIdentifier: "custom") as! CustomCell
        cell.mainImage = data[indexPath.row].picture
        cell.message = data[indexPath.row].date
        customizeCell(cell)
        return cell
    }
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return data.count
    }
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        //myIndex = indexPath.row
        index = indexPath.row
        
        performSegue(withIdentifier: "historyDetailSegue", sender: self)
        
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        print(1)
        if segue.destination is HistoryDetailViewController{
            let vc = segue.destination as? HistoryDetailViewController
            vc?.pet = data[index].pet!
            vc?.breed = data[index].breed!
            vc?.emotion = data[index].emotion!
            print(data[index].emotion!)
            vc?.picture = data[index].picture!
            //print(vc?.breed,vc?.breed)
        }
    }
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCell.EditingStyle, forRowAt indexPath: IndexPath) {
        print(111)
        print(indexPath.row)
        if editingStyle == .delete {

            let path = NSSearchPathForDirectoriesInDomains(
                .documentDirectory, .userDomainMask, true
            ).first!

            let db = try? Connection("\(path)/myDatabase.db")
            let table = Table("PhotoHistory")
            let id = Expression<Int64>("Id")
            
            // remove the item from the data model
            data.remove(at: indexPath.row)
            //print(data[indexPath.row].id)
            let delteRow = table.filter(id == data[indexPath.row].id!)
            try! db?.run(delteRow.delete())
           
            // delete the table view row
            tableView.deleteRows(at: [indexPath], with: .fade)

        } else if editingStyle == .insert {
            // Not used in our example, but if you were adding a new row, this is where you would do it.
        }
    }

    
}






