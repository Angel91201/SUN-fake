import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Xóa nội dung dưới CLIENTE", layout="centered")
st.title("Xóa toàn bộ nội dung dưới CLIENTE trong PDF")

uploaded_file = st.file_uploader("Tải file PDF", type="pdf")

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    removed_any = False

    for page in doc:
        blocks = page.get_text("blocks")

        for i, b in enumerate(blocks):
            if "CLIENTE:" in b[4].upper():
                x0, y0, x1, y1 = b[:4]

                # Lấy các block bên dưới CLIENTE để xóa
                for j in range(i + 1, len(blocks)):
                    bx0, by0, bx1, by1 = blocks[j][:4]

                    # Nếu block cách xa (>150 điểm) thì dừng (đoạn nội dung khác)
                    if by0 - y1 > 150:
                        break

                    # Xóa block này
                    page.add_redact_annot(fitz.Rect(bx0, by0, bx1, by1))
                    y1 = by1  # cập nhật vùng cuối đã xóa
                    removed_any = True

                page.apply_redactions()
                break  # chỉ xử lý CLIENTE đầu tiên trên trang

    if removed_any:
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        st.success("Đã xóa toàn bộ nội dung dưới CLIENTE!")
        st.download_button(
            "📥 Tải PDF đã chỉnh sửa",
            data=output,
            file_name="pdf_xoa_cliente.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Không tìm thấy 'CLIENTE:' trong file PDF.")
