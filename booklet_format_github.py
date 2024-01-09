from PyPDF2 import PdfReader, PdfWriter
import sys
sys.path.append('/mnt/chromeos/MyFiles/Python Programs/functions')
from functions import booklet_sequence, booklet_add_pages
def findall(search, contents):
    i = contents.find(search)
    while i != -1:
        yield i
        i = contents.find(search, i+1)

path = '/mnt/chromeos/MyFiles/Documents/metaphysics_one.pdf'
new_path = ''

if path == '':
    print('No path specified.')
    sys.exit()

if path.find('.txt', -5) > path.find('/'):

    if new_path == '':
        new_path = '{}{}{}'.format(path[:-4], '_new', path[-4:])

    if new_path.find('.txt', -5) <= new_path.find('/'):
        print('Original and new filetypes must be the same.')
        sys.exit()

    with open(path, 'r+') as file:
        contents = file.read()
        reference_locations = [i for i in findall('\n\n', contents)]
        entry_locations = [i for i in findall('\n', contents) if i not in reference_locations if i not in [x + 1 for x in reference_locations]]

    with open(new_path, 'w+') as new_file:
        new_file.truncate(0)
        new_file.write(contents)
        for entry in entry_locations:
            new_file.seek(entry)
            new_file.write(' ')

elif path.find('.pdf', -5) > path.find('/'):

    if new_path == '':
        new_path = '{}{}{}'.format(path[:-4], '_new', path[-4:])

    if new_path.find('.pdf', -5) <= new_path.find('/'):
        print('Original and new filetypes must be the same.')
        sys.exit()

    pdf_contents = PdfReader(path)
    page = len(pdf_contents.pages)

    booklet_add_pages(path, 4, new_path)

    pdf_contents = PdfReader(new_path)

    page = len(pdf_contents.pages)
    sequence = booklet_sequence(page)

    reordered_writer = PdfWriter()
    for page_num in sequence:
        reordered_writer.add_page(pdf_contents.pages[page_num - 1])

    with open(new_path, 'wb') as booklet_file:
        reordered_writer.write(booklet_file)
else:
    err = 'Unsupported filetype(s).'
    print(err)