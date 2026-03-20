# app.py
import streamlit as st
from underthesea import word_tokenize, pos_tag

st.set_page_config(page_title="Demo POS Tagging Tiếng Việt", layout="wide")

st.title("Demo POS Tagging Tiếng Việt với Streamlit")
st.write("Nhập một câu tiếng Việt, ứng dụng sẽ tách từ và gán nhãn từ loại.")

# Input
text = st.text_area(
    "Nhập câu tiếng Việt ở đây:",
    "Hệ thống phân loại bình luận tiếng Việt rất chính xác.",
    height=100
)

analyze_clicked = st.button("Phân tích", type="primary", width="stretch")

col1, col2 = st.columns(2)

import pandas as pd
import base64

# Bảng giải thích nhãn từ loại
POS_TAGS_EXPLANATION = {
    "N": "Danh từ",
    "Np": "Danh từ riêng",
    "Nc": "Danh từ chỉ loại",
    "Nu": "Danh từ đơn vị",
    "V": "Động từ",
    "A": "Tính từ",
    "P": "Đại từ",
    "R": "Phó từ",
    "L": "Định từ",
    "M": "Số từ",
    "E": "Giới từ",
    "C": "Liên từ",
    "I": "Thán từ",
    "T": "Trợ từ, tiểu từ",
    "B": "Từ gốc Hán-Việt",
    "Y": "Từ viết tắt",
    "S": "Từ ngoại lai",
    "X": "Từ không phân loại",
    "CH": "Dấu câu",
}

# Màu cho từng loại từ loại
POS_COLORS = {
    "N": "#FF6B6B",
    "Np": "#FF4444",
    "Nc": "#FF8888",
    "Nu": "#FFAAAA",
    "V": "#4ECDC4",
    "A": "#FFE66D",
    "P": "#A8E6CF",
    "R": "#95E1D3",
    "L": "#DDA0DD",
    "M": "#87CEEB",
    "E": "#FFA07A",
    "C": "#98D8C8",
    "I": "#F7DC6F",
    "T": "#BB8FCE",
    "B": "#F0B27A",
    "Y": "#AED6F1",
    "S": "#F5B7B1",
    "X": "#D5DBDB",
    "CH": "#BDC3C7",
}

# Nhiệm vụ 6: Highlight màu cho từng loại từ loại khác nhau
def get_highlighted_text(words_tags):
    html = '<div style="line-height: 2.5;">'
    for word, tag in words_tags:
        color = POS_COLORS.get(tag, "#CCCCCC")
        html += f'<span style="background-color: {color}; padding: 0.2rem 0.5rem; margin: 0.2rem; border-radius: 0.3rem; display: inline-block; color: #333; font-weight: 500;">{word} <span style="font-size: 0.7em; font-weight: bold; opacity: 0.7;">[{tag}]</span></span> '
    html += '</div>'
    return html

st.divider()

if analyze_clicked:
    # Nhiệm vụ 4: Xử lý lỗi khi input rỗng
    if not text.strip():
        st.warning("Vui lòng nhập văn bản để phân tích!")
    else:
        # Chạy NLP pipeline
        tokens = word_tokenize(text)
        tags = pos_tag(text)
        
        # Nhiệm vụ 1: Xử lý tokenize và hiển thị kết quả ở col1
        with col1:
            st.subheader("1. Kết quả Tách Từ (Tokenize)")
            st.write(tokens)
            
        # Nhiệm vụ 2: Xử lý POS tagging và hiển thị kết quả ở col2
        with col2:
            st.subheader("2. Kết quả Gán Nhãn (POS Tagging)")
            df_tags = pd.DataFrame(tags, columns=["Từ (Token)", "Nhãn POS"])
            # Thêm cột giải thích
            df_tags["Từ loại"] = df_tags["Nhãn POS"].map(POS_TAGS_EXPLANATION).fillna("Không xác định")
            st.dataframe(df_tags, use_container_width=True)
            
        st.divider()
        
        st.subheader("3. Đoạn văn Highlight theo Từ Loại")
        st.markdown(get_highlighted_text(tags), unsafe_allow_html=True)
        
        st.divider()
        
        # Nhiệm vụ 5: Export kết quả ra file CSV
        st.subheader("4. Xuất Dữ Liệu")
        csv_data = df_tags.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="Tải xuống kết quả CSV",
            data=csv_data,
            file_name="pos_tag_result.csv",
            mime="text/csv"
        )

st.divider()
# Nhiệm vụ 3: Bảng giải thích các nhãn từ loại (POS tags)
st.subheader("Bảng tra cứu nhãn Từ loại (POS Tags)")

def get_color_box(tag):
    color = POS_COLORS.get(tag, "#CCCCCC")
    return f'<div style="background-color: {color}; width: 20px; height: 20px; border-radius: 3px; border: 1px solid #999;"></div>'

df_explanation = pd.DataFrame(list(POS_TAGS_EXPLANATION.items()), columns=["Nhãn POS", "Ý nghĩa"])
df_explanation["Màu gán"] = df_explanation["Nhãn POS"].apply(get_color_box)
st.write(df_explanation.to_html(escape=False, index=False), unsafe_allow_html=True)