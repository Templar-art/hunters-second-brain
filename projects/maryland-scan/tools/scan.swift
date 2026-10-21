// Photogrammetry with Apple's Object Capture (RealityKit), free and on-device.
//   swiftc -O scan.swift -o scan && ./scan <image folder> <out.usdz> [preview|reduced|medium|full|raw]
// Drone frames are an ordered sequence; high feature sensitivity helps on flat roofs and lawns.
import Foundation
import RealityKit

let a = CommandLine.arguments
guard a.count >= 3 else { print("usage: scan <images> <out.usdz> [detail]"); exit(1) }
let input = URL(fileURLWithPath: a[1], isDirectory: true)
let output = URL(fileURLWithPath: a[2])
let detail: PhotogrammetrySession.Request.Detail = {
    switch a.count > 3 ? a[3] : "medium" {
    case "preview": return .preview
    case "reduced": return .reduced
    case "full": return .full
    case "raw": return .raw
    default: return .medium
    }
}()

var cfg = PhotogrammetrySession.Configuration()
cfg.sampleOrdering = .sequential
cfg.featureSensitivity = .high

let session = try PhotogrammetrySession(input: input, configuration: cfg)
Task {
    for try await out in session.outputs {
        switch out {
        case .requestProgress(_, let f): print(String(format: "progress %.0f%%", f * 100)); fflush(stdout)
        case .requestError(_, let e): print("ERROR \(e)"); exit(2)
        case .requestComplete(_, _): print("SCAN_OK \(output.path)")
        case .processingComplete: exit(0)
        case .invalidSample(let id, let why): print("invalid sample \(id): \(why)")
        case .skippedSample(let id): print("skipped sample \(id)")
        default: break
        }
    }
}
try session.process(requests: [.modelFile(url: output, detail: detail)])
RunLoop.main.run()
