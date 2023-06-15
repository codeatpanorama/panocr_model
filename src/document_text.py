
from __future__ import annotations

from collections.abc import Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

import os

# TODO(developer): Uncomment these variables before running the sample.
project_id = 'firm-circlet-389805'
location = 'us' # Format is 'us' or 'eu'
processor_id = '68dcba16f1138886' # Create processor before running sample
processor_version = 'pretrained-ocr-v1.0-2020-09-23' # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
file_path = './Data/mht/01.png'
mime_type = 'image/tiff' # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types


def process_document_ocr_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> None:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    # For a full list of Document object attributes, please reference this page:
    # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document

    text = document.text

    '''
    print(f"Full document text: {text}\n")
    print(f"There are {len(document.pages)} page(s) in this document.\n")

    for page in document.pages:
        print(f"Page {page.page_number}:")
        print_page_dimensions(page.dimension)
        print_detected_langauges(page.detected_languages)
        print_paragraphs(page.paragraphs, text)
        print_blocks(page.blocks, text)
        print_lines(page.lines, text)
        print_tokens(page.tokens, text)

        # Currently supported in version pretrained-ocr-v1.1-2022-09-12
        if page.image_quality_scores:
            print_image_quality_scores(page.image_quality_scores)
    '''
    return text

png_dir = './Data/marathi_handwritten_text/tif-300-dpi'


def create_files():
    count = 0
    for tif_file in os.listdir(png_dir):
        if tif_file.endswith(".tif"):
            gt_file = os.path.join(png_dir, tif_file.replace(".tif", ".gt.txt"))
            tif_path = os.path.join(png_dir, tif_file)
            if not os.path.exists(gt_file):
                print(f"Missing .gt.txt file for {tif_file}")
                count = count +1
                text = process_document_ocr_sample(project_id, location, processor_id, processor_version, tif_path, mime_type)
                # Construct the output file path
                output_file = os.path.join(tif_path.replace('.tif', '.gt.txt'))

                # Write the text to the output file
                with open(output_file, 'w') as file:
                    file.write(text)


    '''
    for filename in os.listdir(png_dir):
        if filename.endswith('.png'):
            # Construct the full path to the PNG file
            png_path = os.path.join(png_dir, filename)

            text = process_document_ocr_sample(project_id, location, processor_id, processor_version, png_path, mime_type)

            # Construct the output file path
            output_file = os.path.join(png_dir, filename.replace('.png', '.gt.txt'))

            # Write the text to the output file
            with open(output_file, 'w') as file:
                file.write(text)
    '''



#result = process_document_ocr_sample(project_id, location, processor_id, processor_version, file_path, mime_type)
#print(result)


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g. projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}
    # You must create processors before running sample code.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    return result.document


def print_page_dimensions(dimension: documentai.Document.Page.Dimension) -> None:
    print(f"    Width: {str(dimension.width)}")
    print(f"    Height: {str(dimension.height)}")


def print_detected_langauges(
    detected_languages: Sequence[documentai.Document.Page.DetectedLanguage],
) -> None:
    print("    Detected languages:")
    for lang in detected_languages:
        code = lang.language_code
        print(f"        {code} ({lang.confidence:.1%} confidence)")


def print_paragraphs(
    paragraphs: Sequence[documentai.Document.Page.Paragraph], text: str
) -> None:
    print(f"    {len(paragraphs)} paragraphs detected:")
    first_paragraph_text = layout_to_text(paragraphs[0].layout, text)
    print(f"        First paragraph text: {repr(first_paragraph_text)}")
    last_paragraph_text = layout_to_text(paragraphs[-1].layout, text)
    print(f"        Last paragraph text: {repr(last_paragraph_text)}")


def print_blocks(blocks: Sequence[documentai.Document.Page.Block], text: str) -> None:
    print(f"    {len(blocks)} blocks detected:")
    first_block_text = layout_to_text(blocks[0].layout, text)
    print(f"        First text block: {repr(first_block_text)}")
    last_block_text = layout_to_text(blocks[-1].layout, text)
    print(f"        Last text block: {repr(last_block_text)}")


def print_lines(lines: Sequence[documentai.Document.Page.Line], text: str) -> None:
    print(f"    {len(lines)} lines detected:")
    first_line_text = layout_to_text(lines[0].layout, text)
    print(f"        First line text: {repr(first_line_text)}")
    last_line_text = layout_to_text(lines[-1].layout, text)
    print(f"        Last line text: {repr(last_line_text)}")


def print_tokens(tokens: Sequence[documentai.Document.Page.Token], text: str) -> None:
    print(f"    {len(tokens)} tokens detected:")
    first_token_text = layout_to_text(tokens[0].layout, text)
    first_token_break_type = tokens[0].detected_break.type_.name
    print(f"        First token text: {repr(first_token_text)}")
    print(f"        First token break type: {repr(first_token_break_type)}")
    last_token_text = layout_to_text(tokens[-1].layout, text)
    last_token_break_type = tokens[-1].detected_break.type_.name
    print(f"        Last token text: {repr(last_token_text)}")
    print(f"        Last token break type: {repr(last_token_break_type)}")


def print_image_quality_scores(
    image_quality_scores: documentai.Document.Page.ImageQualityScores,
) -> None:
    print(f"    Quality score: {image_quality_scores.quality_score:.1%}")
    print("    Detected defects:")

    for detected_defect in image_quality_scores.detected_defects:
        print(f"        {detected_defect.type_}: {detected_defect.confidence:.1%}")


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document's text. This function converts
    offsets to a string.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in layout.text_anchor.text_segments:
        start_index = int(segment.start_index)
        end_index = int(segment.end_index)
        response += text[start_index:end_index]
    return response

#create_files()

for filename in os.listdir(png_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(png_dir, filename)
        
        with open(file_path, "r+") as file:
            lines = file.readlines()
            file.seek(0)  # Move the file pointer to the beginning of the file
            
            for line in lines:
                if line.strip():  # Check if the line is not empty after stripping whitespace
                    line = line.rstrip("\n")  # Remove trailing newline character
                    file.write(line)
                    
            
            file.truncate()  # Remove any remaining content after the modified lines

