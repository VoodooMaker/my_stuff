path = ''
new_path = ''

from PyPDF2 import PdfReader, PdfWriter
import sys

# adds a number of pages to meet a certain multiple of 'reference_number'
def booklet_add_pages(file_path: str, reference_number: int, new_path: str):
    from PyPDF2 import PdfReader, PdfWriter
    if reference_number <= 0:
        err = 'Reference number must be greater than zero.'
        return err
    contents = PdfReader(file_path)
    page_number = len(contents.pages)
    if (page_number / reference_number) != (page_number // reference_number):
        add_page = reference_number - page_number % reference_number
        writer = PdfWriter()
        for existing_page in contents.pages:
            writer.add_page(existing_page)
        for i in range(add_page):
            writer.add_blank_page()
        if new_path != '':
            with open(new_path, 'wb') as new_file:
                writer.write(new_file)
        else:
            with open(file_path, 'wb') as new_file:
                writer.write(new_file)

# produces a list of page numbers in the same order as a booklet
# composed of double sided, two pages per side, booklet
def booklet_sequence(page: int):
    sequence = []
    err = ''
    if page <= 0:
        err = 'Parameter must be greater than zero.'
    elif page % 4 != 0:
        err = 'Parameter must be a multiple of four.'
    if err != '':
        return err
    sequence = list(range(1, page // 2 + 1))
    half_seq = list(range(page // 2, 0, - 1))
    for num in half_seq:
        sequence.insert(num - 1, - num)
    half_seq.reverse()
    half_seq = [element * 2 -2 for element in half_seq]
    for num in half_seq:
        if sequence[num] % 2 == 0:
            sequence[num] = - sequence[num]
            sequence[num + 1] = - sequence[num]
    incremental_list = list(range(1, len(sequence) + 1))
    for num in sequence:
        if num < 0:
            sequence[sequence.index(num)] = incremental_list[num]
    return sequence

# finds all instances of 'search' in 'contents', including overlapping entries
def findall(search, contents):
    i = contents.find(search)
    while i != -1:
        yield i
        i = contents.find(search, i+1)

if path == '':
    print('No path specified.')
    sys.exit()

# tests if file is a .txt
if path.find('.txt', -5) > path.find('/'):

    # if 'new_path' is empty, names it 'path' with '_new' before the file extension
    if new_path == '':
        new_path = '{}{}{}'.format(path[:-4], '_new', path[-4:])

    if new_path.find('.txt', -5) <= new_path.find('/'):
        print('Original and new filetypes must be the same.')
        sys.exit()

    # makes a list of all single return characters
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

# test if file is a .pdf
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
