//
//  AudioViewController.swift
//  Clima
//
//  Created by Junxu ZHANG on 5/2/20.
//  Copyright © 2020 App Brewery. All rights reserved.
//

import UIKit
import AVKit
import Vision
import AVFoundation
class AudioViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var infoLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let captureSession = AVCaptureSession()
        //captureSession.sessionPreset = .photo
        guard let captureDevice = AVCaptureDevice.default(for: .video) else {return }
        guard let input = try? AVCaptureDeviceInput(device: captureDevice) else {return }
        captureSession.addInput(input)
        captureSession.startRunning()
        let previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        imageView.layer.addSublayer(previewLayer)
        previewLayer.frame = imageView.frame
        
        let dataOutput = AVCaptureVideoDataOutput()
        dataOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
        captureSession.addOutput(dataOutput)
    }
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard let pixelBuffer: CVPixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {return }
        guard let model = try? VNCoreMLModel(for: Resnet50().model) else {return }
        let request = VNCoreMLRequest(model: model) { (finishedRq, err) in
            guard let results = finishedRq.results as? [VNClassificationObservation] else {return }
            guard let firstObservation = results.first else{return }
            DispatchQueue.main.async {
//                guard let number = firstObservation.confidence else{return }
                self.infoLabel.text = firstObservation.identifier + " " + String(format: "%.2f", firstObservation.confidence * 100) + "%"
            }
        }
        try? VNImageRequestHandler(cvPixelBuffer: pixelBuffer, options: [:]).perform([request])
    }
}
