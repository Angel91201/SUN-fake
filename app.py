import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Chỉnh thông tin dưới CLIENTE", layout="centered")
st.title("Chỉnh thông tin dưới CLIENTE trong PDF")

uploaded_file = st.file_uploader("Tải file PDF", type="pdf")

# Nội dung mới cần thêm vào
NEW_TEXT = """SUNFLOWER LOGISTIC SL
C.I.F.: B09775438
CALLE SANDALIO LOPEZ, 20, ENTREGA 10-14H
28034 SPAIN
MADRID, MADRID"""

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    replaced_any = False

    for page in doc:
        blocks = page.get_text("blocks")  # mỗi block là (x0, y0, x1, y1, text, block_no, block_type)
        for i, b in enumerate(blocks):
            text_block = b[4].strip()

            if text_block.upper().startswith("CLIENTE:"):
                # Lấy tọa độ khối "CLIENTE:"
                cliente_x0, cliente_y0, cliente_x1, cliente_y1 = b[:4]

                # Xác định khối text kế tiếp (thông tin cần xóa)
                if i + 1 < len(blocks):
                    next_block = blocks[i + 1]
                    x0, y0, x1, y1 = next_block[:4]

                    # Xóa nội dung cũ
                    page.add_redact_annot(fitz.Rect(x0, y0, x1, y1 + 60))  # mở rộng một chút chiều cao
                    page.apply_redactions()

                    # Chèn nội dung mới ngay vị trí khối cũ
                    page.insert_text(
                        (x0, y0),  # vị trí bắt đầu
                        NEW_TEXT,
                        fontsize=11,
                        fontname="helv",
                        fill=(0, 0, 0)
                    )
                    replaced_any = True
                break

    if replaced_any:
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        st.success("Đã thay thông tin dưới CLIENTE thành công!")
        st.download_button(
            "📥 Tải PDF đã chỉnh sửa",
            data=output,
            file_name="pdf_chinh_sua.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Không tìm thấy chữ 'CLIENTE:' trong file PDF.")
