//
//  DetailViewController.swift
//  Pet Smile
//
//  Created by Junxu ZHANG on 7/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class DogDetailViewController: UIViewController {

    @IBOutlet weak var overviewLabel: UILabel!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var lifespanLabel: UILabel!
    @IBOutlet weak var maintenceLabel: UILabel!
    @IBOutlet weak var healthRiskLabel: UILabel!
    @IBOutlet weak var recommendedLabel: UILabel!
    @IBOutlet weak var temperamentLabel: UILabel!
    @IBOutlet weak var imageView: UIImageView!
    var petImage  = UIImage()
    var breedName = String()
    var recommended = String()
    var lifespan = String()
    var maintence = String()
    var temperament = String()
    var healthRisk = String()
    var breedOverview = String()

    override func viewDidLoad() {
        super.viewDidLoad()
        nameLabel.text = breedName
        imageView.image = petImage
        lifespanLabel.text = lifespan
        recommendedLabel.text = recommended
        maintenceLabel.text = maintence
        temperamentLabel.text = temperament
        healthRiskLabel.text = healthRisk
        overviewLabel.text = breedOverview
        overviewLabel.lineBreakMode = .byWordWrapping
        overviewLabel.numberOfLines = 0
        overviewLabel.adjustsFontSizeToFitWidth = true
    }
}
