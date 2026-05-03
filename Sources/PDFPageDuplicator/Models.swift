import Foundation

struct DuplicationInstruction {
    let sourcePageIndex: Int
    let copies: Int
    let fieldTemplateValues: [String: String]
}

struct PageCopyContext {
    let copyIndex: Int
    let sourcePageIndex: Int
}
