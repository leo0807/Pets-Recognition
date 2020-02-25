//
//  SubTabBarViewController.swift
//  Pet Smile
//
//  Created by Scott on 12/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import UIKit

class SubTabBarViewController: UITabBarController {

    @IBOutlet weak var subTabBar: UITabBar!
    override func viewDidLoad() {
        super.viewDidLoad()
        //UIApplication.shared.statusBarFrame.size.height
        //self.tabBar.frame = CGRect( x: 0, y: 0, width: 320, height: 50)
        
        subTabBar.frame = CGRect(x: 0, y: 0, width: subTabBar.frame.size.width, height: subTabBar.frame.size.height)
        // Do any additional setup after loading the view.
    }
    

}
