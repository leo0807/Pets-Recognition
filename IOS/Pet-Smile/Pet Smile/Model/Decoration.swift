//
//  Decoration.swift
//  Pet Smile
//
//  Created by Junxu ZHANG on 6/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import Foundation
import UIKit
//Customisze the tapped button
class Decoration{
    func buttonDecoration(_ button: UIButton){
        button.layer.borderWidth = 1.0
        button.layer.masksToBounds = false
        button.layer.borderColor = UIColor.gray.cgColor
        button.layer.cornerRadius = 10
        button.clipsToBounds = true
        button.backgroundColor = .white
        button.frame.size = CGSize(width: 100, height: 30)
        
    }
}
