#%%
import os
import datetime
from pdf2image import convert_from_path
import layoutparser as lp
import streamlit as st
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import io
import pdfplumber
import fitz
from layoutparser import draw_box


#%%
@st.cache_resource
def process_pdf(pdf_path):
    model = lp.Detectron2LayoutModel(
                                    "lp://TableBank/faster_rcnn_R_50_FPN_3x/config",
                                    label_map={0: "Table"},
                                    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.9],
                                    )

    images = convert_from_path(pdf_path)
    output = {

    }
    for i, image in enumerate(images):
        layout = model.detect(image)
        table_blocks = [b for b in layout if b.type=='Table']

        if len(table_blocks):
            image_with_rectangles = draw_box(image, table_blocks,box_color="red")  # Customize color and thickness as needed
            output[i]={
            "orginal":image_with_rectangles,
            "tables":[],
            "coordinates":[]
            }
            for table in table_blocks:
                x_min, y_min, x_max, y_max = table.coordinates
                table_image = image.crop((x_min, y_min, x_max, y_max))
                output[i]["tables"].append(table_image)
                output[i]["coordinates"].append((x_min, y_min, x_max, y_max))
    return output
       
def get_text(page_dict, page_number,table_index):
    page = pdf_document.load_page(page_number)
    page_width, page_height = page.rect.width, page.rect.height
    Image_width, page_height = page_dict[page_number]["orginal"].size 
    multiplier_factor = page_width/Image_width
    page = pdf_document.load_page(page_number)
    ix_min, iy_min, ix_max, iy_max = [co_or*multiplier_factor for co_or in page_dict[page_number]["coordinates"][table_index]]
    text_array = []
    for text_obj in page.get_text("dict")["blocks"]:
            for line in text_obj.get("lines",[]):
                for span in line["spans"]:
                    x_min, y_min, width, height  = span["bbox"]
                    font_size = span["size"]
                    text = span["text"]
                if (ix_min <= x_min and iy_min <= y_min) and (ix_max >= x_min and iy_max >= y_min):
                    print(f"Text: {text} X: {x_min} height:{height} bbox:{span['bbox']}")
                    text_array.append([text,x_min, y_min, font_size])
    return text_array

output_folder="data/"

pdf_path = f"{output_folder}Medical insurance FAQ FY 24.pdf"#f"{output_folder}Medical insurance FAQ FY 24.pdf"
pdf_document = fitz.open(pdf_path)
output = process_pdf(pdf_path)
#%%
def showPhoto(index):
    key = pathsImages[index]
    st.header(f"Showing {index+1} out of {len(pathsImages)}" )
    # with st.container():Prepare
    # total_tables = len(output[key]['tables'])
        # cols = st.columns(total_tables+1) 
    st.write(f"Found {len(output[key]['tables'])} tables in page {key}")
    st.image(output[key]["orginal"], caption=f'Page No. {key}')#,use_column_width=True)
    for idx, table in enumerate(output[key]["tables"]):
        extracted_text = get_text(output,key, idx)
        st.image(table, caption=f'Table {idx+1}')
        st.write(extracted_text)
        # st.image(created_image, caption=f'Table {idx+1}')#,use_column_width=True)
    st.session_state.counter += 1
    if st.session_state.counter >= len(pathsImages):
        st.session_state.counter = 0
if 'counter' not in st.session_state: 
    st.session_state.counter = 0
pathsImages = list(output.keys())
#%%
index = st.session_state.counter
show_btn = st.button(f"{index}\/{len(pathsImages)} Next",on_click=showPhoto, args= ([index]))


# with pdfplumber.open(pdf_path) as pdf:
#     page = pdf.pages[1]
#     print(page.extract_text().split('\n'))
#     # for text_obj in page.extract_text().split('\n'):
#     #     x, y, width, height = text_obj.split(',')
#     #     print(f"X: {x}, Y: {y}, Width: {width}, Height: {height}")
#%%
# def ocr_engine(cropped_image):
#     width, height = cropped_image.size
#     white_image = Image.new('RGB', (width, height), (255, 255, 255))
#     draw = ImageDraw.Draw(white_image)
#     gray_image = cropped_image.convert('L')
#     font_size = None
#     recognized_data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)
#     for i, word_info in enumerate(zip(recognized_data['text'], recognized_data['left'], recognized_data['top'],
#                                    recognized_data['width'], recognized_data['height'])):
#         word, left, top, width, height = word_info
#         if word.strip() == "":
#             continue
#         # if not font_size:
#         font_size = int(height * 1.0)
#         font = ImageFont.truetype("Arial.ttf", size = font_size)
#         try:
#             word.encode('latin-1', 'replace')
#             print((left,top), word)
#             draw.text((left,top), word, fill="black", spacing=0, font= font)
#         except:
#             continue
#     output_buffer = io.BytesIO()
#     white_image.save(output_buffer, format="JPEG")
#     return output_buffer




 
#  #%%
#     # print(recognized_data)
#     # for line in recognized_data.splitlines():
#     # # Split the line into individual data elements
#     #     data = line.split()
#     #     character, x, y, w, h = data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4])
#     #     print(character)




# # %%

# %%
