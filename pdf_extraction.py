#%%
import camelot as cm
import os

#%%
directory_path = 'data/'
output_dir ="output/"
pdf_files = [file for file in os.listdir(directory_path) if file.lower().endswith('.pdf')]
final_tables = []
# %%
for file in pdf_files:
    print(file)
    tables = cm.read_pdf(f"data/{file}",
                         pages='all', 
                         #flavor='stream'
                         )
    print(tables)
    final_tables.extend(tables)
# %%
for idx, tables in enumerate(final_tables):
    # tables.to_excel(f"{idx}.xlsx") 
# %%
final_tables[0].df.to_html(index=False)
# %%
tables = cm.read_pdf(f"data/Handbook Medical Insurance Policy Benefits and Claim Process FY 24.pdf",
                         pages='4', 
                         #flavor='stream'
                         )
# %%
tables[0].df.to_html(index=False)
# %%
# import tabula
# tables = tabula.read_pdf("data/Handbook Medical Insurance Policy Benefits and Claim Process FY 24.pdf", pages='7')
with open('my-table.html', 'w') as f:
    f.write(tables[0].df.to_html(index=False))

# %%
tables = cm.read_pdf(
    'data/Handbook Medical Insurance Policy Benefits and Claim Process FY 24.pdf',
     pages='4', 
    line_scale=20,
     backend="poppler",
    #  flavor='stream'
    )
cm.plot(tables[0], kind='grid').show()
# %%
from pdf2image import convert_from_path
pdf_path = "data/Handbook Medical Insurance Policy Benefits and Claim Process FY 24.pdf"
output_folder="data/"
# def convert_pdf_to_images(pdf_path, output_folder):
images = convert_from_path(pdf_path)

for i, image in enumerate(images):
    image.save(f'{output_folder}/output_{i}.jpg')
# %%
