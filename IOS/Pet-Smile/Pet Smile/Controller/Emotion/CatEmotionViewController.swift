//
//  CatEmotionViewController.swift
//  Pet Smile
//
//  Created by Scott on 13/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class CatEmotionViewController: UIViewController {
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var breedName: UILabel!
    @IBOutlet weak var descriptionLabel: UILabel!
    var catImg = UIImage()
    var breed = String()
    var descriptionText = String()
    override func viewDidLoad() {
        super.viewDidLoad()

        imageView.image = catImg
        breedName.text = breed
        descriptionLabel.text = descriptionText
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
