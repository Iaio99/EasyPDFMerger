#!/usr/bin/env python3

import argparse
import os
from PyPDF2 import PdfReader, PdfWriter

parser = argparse.ArgumentParser(prog = "MergePDF")
parser.add_argument('-f', '--files', nargs='+')
parser.add_argument('-o', '--output-file', type=str, default='output.pdf')
parser.add_argument('-a', '--append', action='store_true')
parser.add_argument('-b', '--no-bookmarks', dest='bookmarks', action='store_false')
parser.add_argument('-i', '--import-bookmarks', action='store_true')


def yes_or_no(question: str):
    answer = input(f"{question} [y/N]: ")
    if answer.lower() == "yes" or answer.lower() == "y":
        return True
    else:
        return False


def get_bookmarks(pdf_file: PdfReader):
    bookmarks = {}
    
    for b in pdf_file.outlines:
        bookmarks[b['/Title']] = pdf_file.get_destination_page_number(b)

    return bookmarks


def merge_pdfs_with_bookmark(pdf_files: list, output_file: str, bookmarks = True, import_bookmarks = False):
    pdf_writer = PdfWriter()
    
    bookmark_page = 0

    for pdf_file in pdf_files:
        pdf_name = os.path.basename(pdf_file)
        f = open(pdf_file, 'rb')
        pdf_reader = PdfReader(f)
        
        for p in pdf_reader.pages:
            pdf_writer.add_page(p)

        if bookmarks:
            new_bookmark = pdf_writer.add_bookmark(pdf_name.split('.pdf')[0], bookmark_page)
            bookmark_page += len(pdf_reader.pages)

        if import_bookmarks:
            old_bookmarks = get_bookmarks(pdf_reader)
            for b in old_bookmarks.keys():
                pdf_writer.add_bookmark(b, old_bookmarks[b] + len(pdf_writer.pages) - len(pdf_reader.pages), parent = new_bookmark)

    if output_file in pdf_files:
        os.remove(output_file)

    with open(output_file, 'wb') as out_pdf:
        print("Writing output")
        pdf_writer.write(out_pdf)

    if yes_or_no("Do you want to remove the original files?"):
        for p in pdf_files:
            os.remove(p)


if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.append:
        args.output_file = args.files[0]

    if args.import_bookmarks:
        args.bookmarks = True

    merge_pdfs_with_bookmark(args.files, args.output_file, args.bookmarks, args.import_bookmarks)
