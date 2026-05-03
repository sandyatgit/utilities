import Foundation
import PDFKit

enum PDFDuplicationError: LocalizedError {
    case loadFailed
    case invalidPageIndex
    case cloneFailed
    case writeFailed

    var errorDescription: String? {
        switch self {
        case .loadFailed: return "Unable to load PDF document."
        case .invalidPageIndex: return "Selected page index is invalid."
        case .cloneFailed: return "Unable to duplicate source page."
        case .writeFailed: return "Unable to save output PDF."
        }
    }
}

final class PDFDuplicationService {
    private let fieldIsolation = FieldIsolationService()

    func duplicatePages(
        inputURL: URL,
        outputURL: URL,
        instruction: DuplicationInstruction
    ) throws {
        guard let source = PDFDocument(url: inputURL) else { throw PDFDuplicationError.loadFailed }
        guard instruction.sourcePageIndex >= 0,
              instruction.sourcePageIndex < source.pageCount else {
            throw PDFDuplicationError.invalidPageIndex
        }

        let result = PDFDocument()

        // Copy all original pages first.
        for i in 0..<source.pageCount {
            if let page = source.page(at: i), let clone = page.copy() as? PDFPage {
                result.insert(clone, at: result.pageCount)
            }
        }

        // Append duplicated copies with unique field identity/value overrides.
        guard let selected = source.page(at: instruction.sourcePageIndex) else {
            throw PDFDuplicationError.invalidPageIndex
        }

        for copyIndex in 0..<instruction.copies {
            guard let duplicate = selected.copy() as? PDFPage else {
                throw PDFDuplicationError.cloneFailed
            }

            let context = PageCopyContext(copyIndex: copyIndex, sourcePageIndex: instruction.sourcePageIndex)
            fieldIsolation.applyTemplateValues(to: duplicate, values: instruction.fieldTemplateValues, context: context)
            result.insert(duplicate, at: result.pageCount)
        }

        guard result.write(to: outputURL) else {
            throw PDFDuplicationError.writeFailed
        }
    }
}
