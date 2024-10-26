import zipfile
import os


def extract_epub(epub_path, output_dir):

    if not zipfile.is_zipfile(epub_path):
        print(f"{epub_path} is not a valid EPUB file.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(epub_path, 'r') as epub_file:
        epub_file.extractall(output_dir)

    print(f"EPUB extracted to: {output_dir}")


if __name__ == "__main__":
    epub_file_path = 'data/docx/epub/output_file.epub'
    output_directory = 'data/decompiled_epub/book3'

    extract_epub(epub_file_path, output_directory)
