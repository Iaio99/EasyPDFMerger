#!/usr/bin/env python3

import argparse
import os
import sys
from PyPDF2 import PdfReader, PdfWriter

parser = argparse.ArgumentParser(prog = "MergePDF")
parser.add_argument('-f', '--files', nargs='+')
parser.add_argument('-o', '--output-file', type=str, default='output.pdf')
parser.add_argument('-a', '--append', action='store_true')
parser.add_argument('-b', '--no-bookmarks', dest='bookmarks', action='store_false')

def merge_pdfs_with_bookmark(pdf_files: list, output_file: str, bookmarks = True):
    # Inizializza l'oggetto PdfWriter
    pdf_writer = PdfWriter()
    
    bookmark_page = 0
    # Itera sui file PDF e aggiungi ciascun PDF al writer
    for pdf_file in pdf_files:
        f = open(pdf_file, 'rb')
        pdf_reader = PdfReader(f)
        
        # Aggiungi il PDF al writer
        for p in pdf_reader.pages:
            pdf_writer.add_page(p)
        # Aggiungi un segnalibro per il nuovo PDF
        if bookmarks:
            pdf_writer.add_bookmark(pdf_file.split('.pdf')[0], bookmark_page)
            bookmark_page += len(pdf_reader.pages)

    # Scrivi il PDF di output
    with open(output_file, 'wb') as out_pdf:
        print("Writing output")
        pdf_writer.write(out_pdf)

# Esempio di utilizzo
if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.append:
        args.output_file = args.files[0]

    merge_pdfs_with_bookmark(args.files, args.output_file, args.bookmarks)
