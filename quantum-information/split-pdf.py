from PyPDF2 import PdfReader, PdfWriter

input_path = "QIT_talks_3_4_tail_bounds_convergence_in_probability.pdf"
reader = PdfReader(input_path)

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    output_path = f"page_{i+1}.pdf"
    with open(output_path, "wb") as f:
        writer.write(f)

print("PDF split complete!")
