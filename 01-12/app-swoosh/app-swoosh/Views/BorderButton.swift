//
//  BorderButton.swift
//  app-swoosh
//
//  Created by Junxu ZHANG on 12/1/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class BorderButton: UIButton {
    override func awakeFromNib() {
        super.awakeFromNib()
        layer.borderWidth = 3.0
        layer.borderColor = UIColor.white.cgColor
    }
}
