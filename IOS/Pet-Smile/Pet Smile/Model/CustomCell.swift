//
//  CustomCell.swift
//  Pet Smile
//
//  Created by Junxu ZHANG on 7/2/20.
//  Copyright © 2020 Junxu ZHANG. All rights reserved.
//

import Foundation
import UIKit

let cellSpacingHeight: CGFloat = 350

func UIColorFromRGB(rgbValue: UInt) -> UIColor {
    return UIColor(
        red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
        green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
        blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
        alpha: CGFloat(1.0)
    )
}
extension UITextView{
    func centerText() {
        self.textAlignment = .center
        
        let fittingSize = CGSize(width: bounds.width, height: CGFloat.greatestFiniteMagnitude)
        let size = sizeThatFits(fittingSize)
        let topOffSet = (bounds.size.height - size.height*zoomScale) / 2
        //let leftOffSet = (bounds.size.width - size.width*zoomScale) / 2
        let positiveTopOffSet = max(1, topOffSet)
        
        contentOffset.y = -positiveTopOffSet
        
    
    }
}

func customizeCell(_ cell: CustomCell){
    cell.layer.masksToBounds = true

    cell.clipsToBounds = false
    cell.layer.masksToBounds = false
    cell.imageView!.frame = cell.frame.offsetBy(dx: 10, dy: 10);
    cell.backgroundColor = UIColor.white
    cell.layer.borderColor = UIColor.white.cgColor
    cell.layer.borderWidth = 2
    cell.layer.cornerRadius = 8
    cell.layer.shadowOpacity = 0.5
}
//Mark: -U Customize the cell in the UITableViewController
class CustomCell: UITableViewCell {
    var mainImage: UIImage? // Show the Image
    var message: String?    // Show the releated text
        
    
    var mainImageView: UIImageView = {
        var imageView = UIImageView()
        imageView.translatesAutoresizingMaskIntoConstraints = false
        //imageView.contentMode = .scaleAspectFit
        return imageView
    }()
    
    var messageView: UITextView = {
        var messageView = UITextView()
        messageView.translatesAutoresizingMaskIntoConstraints = false
        messageView.isScrollEnabled = false
        messageView.font = .systemFont(ofSize: 20)
        messageView.centerText()
        messageView.isEditable = false
        messageView.backgroundColor =  UIColorFromRGB(rgbValue: 0x50A8FF)
        return messageView
    }()
    
    
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        self.addSubview(mainImageView)
        self.addSubview(messageView)
        //self.addSubview(messageView)
        
        
        mainImageView.layer.masksToBounds = false
        mainImageView.backgroundColor = UIColor.white
        mainImageView.layer.borderColor = UIColor.white.cgColor
        mainImageView.layer.borderWidth = 1
        mainImageView.layer.cornerRadius = 8
        
        
        //mainImageView.layer.backgroundColor = CGColor(colorSpace: CGColorSpaceCreateDeviceRGB(), components: [1.0, 1.0, 1.0, 1.0])
        mainImageView.layer.shadowOffset = CGSize(width: -1, height: 1)
        //mainImageView.layer.shadowOpacity = 0.5
        
        
        
        
        mainImageView.leftAnchor.constraint(equalTo: self.leftAnchor).isActive = true
        //mainImageView.rightAnchor.constraint(equalTo: self.rightAnchor).isActive = true
        mainImageView.topAnchor.constraint(equalTo: self.topAnchor).isActive = true
        mainImageView.bottomAnchor.constraint(equalTo: self.bottomAnchor).isActive = true
        //mainImageView.bottomAnchor.constraint(equalTo: self.messageView.topAnchor).isActive = true
        mainImageView.heightAnchor.constraint(equalToConstant: 90).isActive = true
        mainImageView.widthAnchor.constraint(equalToConstant:  90).isActive = true
        
        
        // mark -u top-down desgin mode
        //        messageView.leftAnchor.constraint(equalTo: leftAnchor).isActive = true
        //        messageView.rightAnchor.constraint(equalTo: rightAnchor).isActive = true
        //        messageView.bottomAnchor.constraint(equalTo: bottomAnchor).isActive = true
        
        
        //        //mainImageView.topAnchor.constraint(equalTo: self.topAnchor).isActive = true
        //
        messageView.leftAnchor.constraint(equalTo: self.mainImageView.rightAnchor).isActive = true
        messageView.rightAnchor.constraint(equalTo: self.rightAnchor).isActive = true
        messageView.bottomAnchor.constraint(equalTo: self.bottomAnchor).isActive = true
        messageView.topAnchor.constraint(equalTo: self.topAnchor).isActive = true
        
    }
    
    override func layoutSubviews() {
        superview?.layoutSubviews()
        if let message = message{
            messageView.text = "\n \(message)"
            
        }
        if let image = mainImage{
            mainImageView.image = image 
        }
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
