import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Chỉnh CLIENTE PDF", layout="centered")
st.title("Chỉnh thông tin CLIENTE trong PDF")

uploaded_file = st.file_uploader("Tải file PDF (1 trang hoặc nhiều trang)", type="pdf")

# Nội dung thay thế
NEW_TEXT = """SUNFLOWER LOGISTIC SL
C.I.F.: B09775438
CALLE SANDALIO LOPEZ, 20, ENTREGA 10-14H
28034 SPAIN
MADRID, MADRID"""

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    replaced_any = False
    for page in doc:
        blocks = page.get_text("blocks")
        for b in blocks:
            block_text = b[4]
            if "CLIENTE:" in block_text.upper():
                x0, y0, x1, y1 = b[:4]
                rect = fitz.Rect(x0, y0, x1, y1)
                page.add_redact_annot(rect)
                page.apply_redactions()
                page.insert_textbox(
                    rect,
                    NEW_TEXT,
                    fontsize=12,
                    fontname="helv",
                    align=0,
                    color=(0, 0, 0)
                )
                replaced_any = True
                break

    if not replaced_any:
        st.warning("Không tìm thấy 'CLIENTE:' trong file PDF.")
    else:
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        st.success("Đã thay thế thành công!")
        st.download_button(
            "📥 Tải PDF đã chỉnh sửa",
            data=output,
            file_name="pdf_chinh_sua.pdf",
            mime="application/pdf"
        )
