import Foundation
import AppKit

@MainActor
final class PDFDuplicationViewModel: ObservableObject {
    @Published var selectedInputURL: URL?
    @Published var selectedOutputURL: URL?
    @Published var pageIndexText: String = "0"
    @Published var copiesText: String = "1"
    @Published var fieldsBlob: String = "name=John {copy}\ninvoice=INV-{page}-{copy}"
    @Published var status: String = "Ready"

    private let service = PDFDuplicationService()

    func chooseInput() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.pdf]
        panel.allowsMultipleSelection = false

        if panel.runModal() == .OK {
            selectedInputURL = panel.url
            status = "Loaded: \(panel.url?.lastPathComponent ?? "")"
        }
    }

    func chooseOutput() {
        let panel = NSSavePanel()
        panel.allowedContentTypes = [.pdf]
        panel.nameFieldStringValue = "output.pdf"

        if panel.runModal() == .OK {
            selectedOutputURL = panel.url
            status = "Output: \(panel.url?.lastPathComponent ?? "")"
        }
    }

    func runDuplication() {
        guard let input = selectedInputURL, let output = selectedOutputURL else {
            status = "Please select input and output files."
            return
        }

        guard let pageIndex = Int(pageIndexText), let copies = Int(copiesText), copies > 0 else {
            status = "Invalid page index/copies value."
            return
        }

        let fields = parseFields(from: fieldsBlob)
        let instruction = DuplicationInstruction(sourcePageIndex: pageIndex, copies: copies, fieldTemplateValues: fields)

        do {
            try service.duplicatePages(inputURL: input, outputURL: output, instruction: instruction)
            status = "Done. Saved \(output.lastPathComponent)"
        } catch {
            status = error.localizedDescription
        }
    }

    private func parseFields(from text: String) -> [String: String] {
        var result: [String: String] = [:]

        for line in text.split(separator: "\n") {
            let parts = line.split(separator: "=", maxSplits: 1).map(String.init)
            if parts.count == 2 {
                result[parts[0].trimmingCharacters(in: .whitespaces)] = parts[1].trimmingCharacters(in: .whitespaces)
            }
        }

        return result
    }
}
