import SwiftUI

struct ContentView: View {
    @ObservedObject var viewModel: PDFDuplicationViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("PDF Page Duplicator")
                .font(.title2)
                .bold()

            HStack {
                Button("Select Input PDF") { viewModel.chooseInput() }
                Text(viewModel.selectedInputURL?.path ?? "No file selected")
                    .font(.caption)
                    .lineLimit(1)
            }

            HStack {
                Button("Select Output PDF") { viewModel.chooseOutput() }
                Text(viewModel.selectedOutputURL?.path ?? "No destination selected")
                    .font(.caption)
                    .lineLimit(1)
            }

            HStack {
                Text("Source Page Index")
                TextField("0", text: $viewModel.pageIndexText)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 80)

                Text("Copies")
                TextField("1", text: $viewModel.copiesText)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 80)
            }

            Text("Field Overrides (one per line: key=value)")
            TextEditor(text: $viewModel.fieldsBlob)
                .font(.system(.body, design: .monospaced))
                .frame(height: 220)
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(.gray.opacity(0.25)))

            Text("Tokens: {copy}, {page}")
                .font(.caption)
                .foregroundStyle(.secondary)

            HStack {
                Button("Duplicate") { viewModel.runDuplication() }
                    .keyboardShortcut(.defaultAction)
                Text(viewModel.status)
                    .font(.caption)
            }

            Spacer()
        }
        .padding(16)
    }
}
