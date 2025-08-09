import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Chỉnh CLIENTE PDF", layout="centered")
st.title("Chỉnh thông tin dưới CLIENTE giống mẫu")

uploaded_file = st.file_uploader("Tải file PDF", type="pdf")

# Nội dung mới
NEW_LINES = [
    ("CLIENTE:", (0, 0, 0), True),  # text, màu, in đậm
    ("SUNFLOWER LOGISTIC SL", (0.4, 0.4, 0.4), False),
    ("CALLE SANDALIO LOPEZ, 20, ENTREGA 10-14H", (0.4, 0.4, 0.4), False),
    ("MADRID, MADRID", (0.4, 0.4, 0.4), False),
    ("28034 SPAIN", (0.4, 0.4, 0.4), False),
    ("C.I.F.: B09775438", (0.4, 0.4, 0.4), False)
]

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    replaced_any = False

    for page in doc:
        blocks = page.get_text("blocks")
        for i, b in enumerate(blocks):
            if "CLIENTE:" in b[4].upper():
                x0, y0, x1, y1 = b[:4]

                # Xóa toàn bộ nội dung cũ phía dưới CLIENTE
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y0 + 90))
                page.apply_redactions()

                # Vẽ lại theo mẫu
                line_height = 14  # khoảng cách dòng
                for idx, (text, color, bold) in enumerate(NEW_LINES):
                    fontname = "helv"
                    if bold:
                        fontname = "helvb"  # Helvetica Bold
                    page.insert_text(
                        (x0, y0 + idx * line_height),
                        text,
                        fontsize=12,
                        fontname=fontname,
                        fill=color
                    )

                replaced_any = True
                break

    if replaced_any:
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        st.success("Đã thay thông tin dưới CLIENTE giống mẫu!")
        st.download_button(
            "📥 Tải PDF đã chỉnh sửa",
            data=output,
            file_name="pdf_chinh_sua.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Không tìm thấy 'CLIENTE:' trong file PDF.")
