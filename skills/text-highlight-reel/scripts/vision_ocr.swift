// Reads an image path, prints JSON: [{"text": "...", "x":N, "y":N, "w":N, "h":N}, ...]
// Coordinates are in PIXELS with origin at top-left.
// Usage:  swift vision_ocr.swift /path/to/image.png

import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2 else {
    FileHandle.standardError.write("usage: vision_ocr.swift <image>\n".data(using: .utf8)!)
    exit(2)
}
let path = args[1]
let url = URL(fileURLWithPath: path)
guard let nsImage = NSImage(contentsOf: url),
      let cgImage = nsImage.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    FileHandle.standardError.write("failed to load image\n".data(using: .utf8)!)
    exit(1)
}
let imgW = CGFloat(cgImage.width)
let imgH = CGFloat(cgImage.height)

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try handler.perform([request])

struct Word: Codable { let text: String; let x: Int; let y: Int; let w: Int; let h: Int }
var words: [Word] = []

for obs in (request.results ?? []) {
    guard let top = obs.topCandidates(1).first else { continue }
    let lineString = top.string
    // Split the line into tokens and get per-token boxes via candidate range
    var idx = lineString.startIndex
    let tokens = lineString.split(separator: " ", omittingEmptySubsequences: false)
    for token in tokens {
        if token.isEmpty {
            // advance idx past the space
            if idx < lineString.endIndex { idx = lineString.index(after: idx) }
            continue
        }
        let start = lineString.range(of: token, range: idx..<lineString.endIndex)?.lowerBound ?? idx
        let end = lineString.index(start, offsetBy: token.count, limitedBy: lineString.endIndex) ?? lineString.endIndex
        idx = end
        if let box = try? top.boundingBox(for: start..<end) {
            // box.boundingBox is normalized, origin bottom-left
            let r = box.boundingBox
            let x = r.minX * imgW
            let y = (1 - r.maxY) * imgH
            let w = r.width * imgW
            let h = r.height * imgH
            words.append(Word(text: String(token),
                              x: Int(x.rounded()),
                              y: Int(y.rounded()),
                              w: Int(w.rounded()),
                              h: Int(h.rounded())))
        }
    }
    // skip past any trailing space
    if idx < lineString.endIndex { idx = lineString.index(after: idx) }
}

let data = try JSONEncoder().encode(words)
FileHandle.standardOutput.write(data)
FileHandle.standardOutput.write("\n".data(using: .utf8)!)
