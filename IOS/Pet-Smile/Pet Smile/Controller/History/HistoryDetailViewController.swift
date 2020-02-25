//
//  HistoryDetailViewController.swift
//  Pet Smile
//
//  Created by Scott on 18/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class HistoryDetailViewController: UIViewController {

    @IBOutlet weak var petLabel: UILabel!
    @IBOutlet weak var breedLabel: UILabel!
    @IBOutlet weak var emotionLabel: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    var pet = String()
    var breed = String()
    var emotion = String()
    var picture = UIImage()
    override func viewDidLoad() {
        super.viewDidLoad()
        petLabel.text = "Pet: \(pet)"
        breedLabel.text = "Breed: \(breed)"
        emotionLabel.text = "Emotion: \(emotion)"
        imageView.image = picture
        // Do any additional setup after loading the view.
    }

}
