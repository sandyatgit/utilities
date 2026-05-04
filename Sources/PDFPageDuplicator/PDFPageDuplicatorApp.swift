import SwiftUI

@main
struct PDFPageDuplicatorApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView(viewModel: PDFDuplicationViewModel())
                .frame(minWidth: 980, minHeight: 680)
        }
    }
}
