//
//  CSVParser.swift
//  Pet Smile
//
//  Created by Scott on 9/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import Foundation
import CSV

//Drop the headers in the first row of database
extension Array{
    var tail: Array{
        return Array(self.dropFirst())
    }
}
//Parse the csv file
func CSVparser(_ inputFilePath: String) -> [[String]]{
    if let filePath = Bundle.main.path(forResource: inputFilePath, ofType: "csv", inDirectory:  "Scraper"){
        let stream = InputStream(fileAtPath: filePath)!
        var result = [[String]]()
        let csv = try! CSVReader(stream: stream)
        
        while let row = csv.next(){
            result.append(row)
        }
        
        return result.tail
    }else{
        print("file not found")
        return [[""]]
    }
}



