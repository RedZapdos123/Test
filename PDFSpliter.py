import os
from PyPDF2 import PdfReader, PdfWriter

#Define input PDF file and output folder paths.
input_pdf_path = r"C:\Users\Xeron\OneDrive\Desktop\TextDocuments\Narasimha Karumanchi - Data structures and algorithms made easy (0, CareerMonk).pdf"
output_folder = r"C:\Users\Xeron\OneDrive\Desktop\TextDocuments"

#Ensure that the output directory exists.
os.makedirs(output_folder, exist_ok=True)

#Define the number of parts and pages per part.
NUM_PARTS = 5
PAGES_PER_PART = 50

#Read the input PDF.
reader = PdfReader(input_pdf_path)
total_pages = len(reader.pages)

#Split the PDF into parts.
for part_num in range(1, NUM_PARTS + 1):
    writer = PdfWriter()
    start_idx = (part_num - 1) * PAGES_PER_PART
    
    #If it's the last part, include all the remaining pages
    if part_num == NUM_PARTS:
        end_idx = total_pages
    else:
        end_idx = min(start_idx + PAGES_PER_PART, total_pages)

    for page_idx in range(start_idx, end_idx):
        writer.add_page(reader.pages[page_idx])

    output_path = os.path.join(output_folder, f'part_{part_num}.pdf')
    with open(output_path, 'wb') as out_file:
        writer.write(out_file)
    print(f'Written {output_path} (pages {start_idx+1} to {end_idx})')

print('PDF splitting complete.')
