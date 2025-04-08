import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# ---- CẤU HÌNH GIAO DIỆN ----
st.set_page_config(page_title="Gợi Ý Bất Động Sản Dựa Trên Trường Học", layout="wide")

st.title("🏡 Gợi Ý Bất Động Sản Dựa Trên Trường Học")

# ---- HƯỚNG DẪN SỬ DỤNG ----
st.markdown("""
🔎 **Hướng dẫn sử dụng:**
- Chọn một trường THPT từ danh sách bên trái.
- Hệ thống sẽ hiển thị các bất động sản nằm trong cùng khu vực với trường đó.
- Nhập mức giá mong muốn (tính theo *tỷ đồng*).
- Ứng dụng sẽ gợi ý những bất động sản có giá gần nhất với mức bạn nhập.

💡 *Mẹo:* Hãy thử nhiều mức giá để khám phá thêm lựa chọn phù hợp!
""")

# ---- TẢI DỮ LIỆU ----
df_school = pd.read_csv("cleaned-hcmc-schools.csv")  # Dữ liệu trường học
df_real_estate = pd.read_csv("processed_mogi_hcm.csv")  # Dữ liệu bất động sản từ mogi
df_real_estate_bds = pd.read_csv("processed_bds.com_hcm.csv")  # Dữ liệu bất động sản từ bds.com


# ---- GIAO DIỆN CHỌN TRƯỜNG ----
st.sidebar.header("🔍 Chọn phần thông tin bạn muốn tìm")
selected_school = st.sidebar.selectbox("Chọn trường học", df_school["Tên đơn vị"].unique())

# Tìm khu vực của trường được chọn
selected_khu_vuc = df_school[df_school["Tên đơn vị"] == selected_school]["Khu vực"].values[0]

# Lọc danh sách bất động sản trong khu vực trường học
df_selected_area = df_real_estate[df_real_estate["Quận/Huyện"] == selected_khu_vuc]
df_selected_area_bds = df_real_estate_bds[df_real_estate_bds["Quận/Huyện"] == selected_khu_vuc]


if df_selected_area.empty:
    st.warning("❌ Không có dữ liệu bất động sản cho khu vực này.")
    st.stop()

# Hiển thị danh sách BĐS tại khu vực trường học
st.subheader(f"📍 Bất động sản tại khu vực: {selected_khu_vuc}")
st.dataframe(df_selected_area[["Tiêu đề", "Quận/Huyện", "Giá (tỷ)", "Diện tích (m2)", "Phòng ngủ", "Nhà tắm"]])

# ---- NGƯỜI DÙNG CHỌN MỨC GIÁ ----
# st.sidebar.header("💰 Chọn Mức Giá Mong Muốn")
# selected_price = st.sidebar.slider(
#     "Chọn mức giá (triệu/m²)", 
#     min_value=float(df_real_estate["Giá bán (triệu/m2)"].min()), 
#     max_value=float(df_real_estate["Giá bán (triệu/m2)"].max()), 
#     value=10.0,  # Giá mặc định
#     step=0.1
# )
selected_price = st.sidebar.number_input(
    "Nhập mức giá mong muốn (tỷ)", 
    min_value=0.01, 
    max_value=100.0, 
    value=10.0,  # Giá mặc định
    step=0.01
)

st.subheader(f"⭐ Gợi Ý Bất Động Sản Có Giá Gần {selected_price:.2f} Tỷ Từ Mogi")

# ---- ÁP DỤNG HỌC MÁY: TÌM BẤT ĐỘNG SẢN TƯƠNG TỰ ----
X = df_selected_area[["Giá (tỷ)"]]
if len(X) > 5:  # Kiểm tra có đủ dữ liệu để tìm hàng xóm không
    knn = NearestNeighbors(n_neighbors=5, metric="euclidean")
    knn.fit(X)
    distances, indices = knn.kneighbors([[selected_price]])

    # Lấy danh sách bất động sản gợi ý
    df_suggested_bds = df_selected_area.iloc[indices[0]]
    st.write("🔹 Các bất động sản trong khu vực có giá gần với mức mong muốn:")
    st.dataframe(df_suggested_bds[["Tiêu đề", "Quận/Huyện", "Giá (tỷ)", "Diện tích (m2)", "Phòng ngủ", "Nhà tắm"]])
else:
    st.warning("⚠️ Không đủ dữ liệu để tìm bất động sản tương tự trong khu vực.")

# # ---- Hiển thị gợi ý bất động sản từ bds.com gần với giá đã nhập ----
# st.subheader(f"⭐ Gợi Ý Bất Động Sản Có Giá Gần {selected_price:.2f} Tỷ Từ BDS.com")

# X_bds = df_selected_area_bds[["Giá (tỷ)"]]

# if len(X_bds) > 5:
#     knn_bds = NearestNeighbors(n_neighbors=5, metric="euclidean")
#     knn_bds.fit(X_bds)
#     distances_bds, indices_bds = knn_bds.kneighbors([[selected_price]])

#     df_suggested_bds_com = df_selected_area_bds.iloc[indices_bds[0]]
#     st.write("🔹 Các bất động sản từ BDS.com có giá gần với mức mong muốn:")
#     st.dataframe(df_suggested_bds_com[["Tiêu đề", "Quận/Huyện", "Giá (tỷ)", "Diện tích (m2)", "Phòng ngủ", "Nhà tắm"]])
# else:
#     st.warning("⚠️ Không đủ dữ liệu từ BDS.com để tìm bất động sản tương tự trong khu vực.")

