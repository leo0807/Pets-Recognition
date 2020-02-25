//
//  DogEmotionViewController.swift
//  Pet Smile
//
//  Created by Scott on 13/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class DogEmotionViewController: UIViewController {

    @IBOutlet weak var descriptionLabel: UILabel!
    @IBOutlet weak var breedName: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    var dogImg = UIImage()
    var breed = String()
    var descriptionText = String()
    override func viewDidLoad() {
        super.viewDidLoad()
        descriptionLabel.text = descriptionText
        breedName.text = breed
        imageView.image = dogImg
        // Do any additional setup after loading the view.
    }
    



}
