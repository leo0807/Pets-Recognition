//
//  CatDetailViewController.swift
//  Pet Smile
//
//  Created by Scott on 12/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class CatDetailViewController: UIViewController {
    @IBOutlet weak var breedname: UILabel!
    
    @IBOutlet weak var img: UIImageView!
    @IBOutlet weak var breedoverview: UILabel!
    var petImage  = UIImage()
    var breedName = String()
    
    var breedOverview = String()
    override func viewDidLoad() {
        super.viewDidLoad()
        breedname.text = breedName
        img.image = petImage
        
        breedoverview.text = breedOverview
        breedoverview.adjustsFontSizeToFitWidth = true
        breedoverview.lineBreakMode = .byWordWrapping
        breedoverview.accessibilityScroll(.down)
        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
