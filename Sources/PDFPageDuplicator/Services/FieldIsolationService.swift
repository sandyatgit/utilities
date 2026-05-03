import Foundation
import PDFKit

/// Handles field updates for each duplicated page so values are not implicitly linked.
///
/// Note: PDFKit has limited support for low-level AcroForm manipulation.
/// This service is intentionally small and isolated so it can be replaced with
/// a dedicated PDF SDK implementation for robust field-renaming.
final class FieldIsolationService {
    func applyTemplateValues(
        to page: PDFPage,
        values: [String: String],
        context: PageCopyContext
    ) {
        guard let annotations = page.annotations as [PDFAnnotation]? else { return }

        for annotation in annotations where annotation.widgetFieldType != nil {
            guard let originalName = annotation.fieldName else { continue }

            // Make field names unique per copy to avoid linked values.
            let uniqueName = "\(originalName)__p\(context.sourcePageIndex + 1)_c\(context.copyIndex + 1)"
            annotation.setValue(uniqueName, forAnnotationKey: .widgetFieldName)

            if let baseValue = values[originalName] {
                let resolved = baseValue
                    .replacingOccurrences(of: "{copy}", with: String(context.copyIndex + 1))
                    .replacingOccurrences(of: "{page}", with: String(context.sourcePageIndex + 1))
                annotation.widgetStringValue = resolved
            }
        }
    }
}
