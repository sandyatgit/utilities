#!/usr/bin/env python3
"""macOS desktop app wrapper for PDF page duplication."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from pdf_page_duplicator import DuplicateInstruction, duplicate_pdf, _parse_field_pairs


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PDF Page Duplicator")
        self.geometry("760x520")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.source_page = tk.StringVar(value="0")
        self.copies = tk.StringVar(value="1")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Input PDF").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.input_path, width=72).grid(row=1, column=0, sticky="we")
        tk.Button(frame, text="Browse", command=self.pick_input).grid(row=1, column=1, padx=6)

        tk.Label(frame, text="Output PDF").grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Entry(frame, textvariable=self.output_path, width=72).grid(row=3, column=0, sticky="we")
        tk.Button(frame, text="Browse", command=self.pick_output).grid(row=3, column=1, padx=6)

        row = tk.Frame(frame)
        row.grid(row=4, column=0, sticky="w", pady=(12, 4))
        tk.Label(row, text="Source page (0-based):").pack(side="left")
        tk.Entry(row, textvariable=self.source_page, width=8).pack(side="left", padx=(6, 14))
        tk.Label(row, text="Copies:").pack(side="left")
        tk.Entry(row, textvariable=self.copies, width=8).pack(side="left", padx=(6, 0))

        tk.Label(frame, text="Field overrides (one per line: key=value)").grid(row=5, column=0, sticky="w")
        self.fields_text = tk.Text(frame, height=14, width=84)
        self.fields_text.insert("1.0", "name=John {copy}\ninvoice=INV-{page}-{copy}\n")
        self.fields_text.grid(row=6, column=0, columnspan=2, sticky="nsew")

        tk.Button(frame, text="Duplicate PDF", command=self.run).grid(row=7, column=0, sticky="w", pady=(10, 0))

        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def pick_input(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.input_path.set(path)

    def pick_output(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path:
            self.output_path.set(path)

    def run(self) -> None:
        try:
            input_path = Path(self.input_path.get())
            output_path = Path(self.output_path.get())
            source_page = int(self.source_page.get())
            copies = int(self.copies.get())

            raw_lines = self.fields_text.get("1.0", "end").strip().splitlines()
            fields = _parse_field_pairs([line for line in raw_lines if line.strip()])

            instruction = DuplicateInstruction(
                source_page_index=source_page,
                copies=copies,
                field_templates=fields,
            )
            duplicate_pdf(input_path, output_path, instruction)
            messagebox.showinfo("Success", f"Saved: {output_path}")
        except Exception as exc:  # UI boundary
            messagebox.showerror("Error", str(exc))


if __name__ == "__main__":
    App().mainloop()
