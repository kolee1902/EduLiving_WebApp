import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.neighbors import NearestNeighbors

# Cấu hình giao diện chính
st.set_page_config(page_title="Phân Tích Dữ Liệu BĐS & Giáo Dục", layout="wide")

# Sidebar for navigation
sidebar_options = [
    "Phân Tích BĐS & Giáo Dục",
    "Gợi Ý BĐS Dựa Trên Trường Học"
]
sidebar_selection = st.sidebar.selectbox("Chọn Phần", sidebar_options)

# ======================== DASHBOARD 1 ========================
if sidebar_selection == "Phân Tích BĐS & Giáo Dục":

    st.title("📈 Phân Tích Dữ Liệu Bất Động Sản & Giáo Dục")
    st.markdown("---")

    # ======================== DASHBOARD 1 ========================
    st.header("1️⃣ Xu hướng Giá BĐS và Điểm Chuẩn qua các năm")

    df_school = pd.read_csv("hcmc-high-schools.csv")
    df_real_estate = pd.read_csv("processed_mogi_hcm.csv")
    df_real_estate = df_real_estate[df_real_estate['Loại BĐS'] != 'Biệt thự']

    df_real_estate['Năm'] = df_real_estate['Ngày đăng'].astype(str).str[-4:]
    df_real_estate = df_real_estate[df_real_estate["Năm"].str.isnumeric()]
    df_real_estate["Năm"] = df_real_estate["Năm"].astype(int)
    # Lọc lại dữ liệu bất động sản
    df_real_estate = df_real_estate[df_real_estate["Năm"].isin([2021, 2022, 2023, 2024])]

    df_real_estate_grouped = df_real_estate.groupby("Năm", as_index=False)["Giá (tỷ)"].mean()
    df_real_estate_grouped.rename(columns={"Giá (tỷ)": "Giá BĐS trung bình"}, inplace=True)

    df_trend = df_school.groupby("Khu vực")[["2021_Điểm chuẩn nguyện vọng 1", "2022_Điểm chuẩn nguyện vọng 1",
                                            "2023_Điểm chuẩn nguyện vọng 1", "2024_Điểm chuẩn nguyện vọng 1",
                                            "2021_Điểm chuẩn nguyện vọng 2", "2022_Điểm chuẩn nguyện vọng 2",
                                            "2023_Điểm chuẩn nguyện vọng 2", "2024_Điểm chuẩn nguyện vọng 2",
                                            "2021_Điểm chuẩn nguyện vọng 3", "2022_Điểm chuẩn nguyện vọng 3",
                                            "2023_Điểm chuẩn nguyện vọng 3", "2024_Điểm chuẩn nguyện vọng 3"]].mean().reset_index()
    df_trend = df_trend.melt(id_vars=["Khu vực"], var_name="Năm", value_name="Điểm chuẩn trung bình")
    df_trend["Năm"] = df_trend["Năm"].str.extract("(\d+)").astype(int)

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    # Vẽ biểu đồ
    sns.lineplot(data=df_trend, x="Năm", y="Điểm chuẩn trung bình", marker="o", color="blue", label="Điểm chuẩn trung bình", ax=ax1)
    sns.lineplot(data=df_real_estate_grouped, x="Năm", y="Giá BĐS trung bình", marker="s", color="red", label="Giá BĐS trung bình", ax=ax2)

    # Thiết lập nhãn và màu
    ax1.set_xlabel("\nNăm", weight='bold', fontsize=12)
    ax1.set_ylabel("Điểm chuẩn trung bình", color="blue")
    ax2.set_ylabel("Giá BĐS trung bình (triệu/m2)", color="red")

    # Sửa định dạng trục x về số nguyên
    years = sorted(df_trend["Năm"].unique())
    plt.xticks(ticks=years, labels=[str(year) for year in years])

    # Hiển thị chú thích và tiêu đề
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    # ax2.grid(False)
    ax2.grid(True, linestyle='--', alpha=0.4)
    plt.title("Xu hướng Giá BĐS & Điểm Chuẩn qua các năm", weight='bold', fontsize=15)

    # Vẽ lên Streamlit
    st.pyplot(fig1)
    # Insight cho biểu đồ
    insight1 = """
    - Có sự tương quan giữa giá bất động sản và giáo dục
    - Điểm chuẩn đầu vào của các trường phổ thông có mối quan hệ **đồng biến** với giá bất động sản 
    """

    # Hiển thị insight
    st.markdown("### 💡 Insight:")
    st.markdown(insight1)
    st.markdown("---")

    # ======================== DASHBOARD 3 ========================
    st.header("2️⃣ Giá BĐS Theo Khoảng Cách Trường Học")

    guide3 = """
    - Hãy cùng khám phá xem khoảng cách từ trường đến các bất động sản trong khu vực bạn đã chọn có ảnh hưởng đến nhau và chênh lệch giá như thế nào !!!
    
    ⭐ Các bất động sản **gần** là các bđs cách trường dưới **2km**, còn **xa** là cách hơn **4km**. 
    """

    # Hiển thị insight
    st.markdown("#### 🔍 Guide:")
    st.markdown(guide3)

    df_distance = pd.read_csv('distance_data.csv', encoding='utf-8')

    def categorize_distance(distance):
        if distance < 2.0:
            return 'Gần'
        elif distance < 4.0:
            return 'Vừa'
        else:
            return 'Xa'

    df_distance['Khoảng cách loại'] = df_distance['Khoảng cách'].apply(categorize_distance)
    average_price_by_distance = df_distance.groupby(['Quận/Huyện', 'Khoảng cách loại'])['Giá (tỷ)'].mean().reset_index()

    selected_quan = st.selectbox("Chọn Quận/Huyện để hiển thị khoảng cách:", df_distance['Quận/Huyện'].unique())
    data_quan = average_price_by_distance[average_price_by_distance['Quận/Huyện'] == selected_quan]

    color = ['#8de5a1', '#ff9f9b', '#a1c9f4']
    fig3, ax5 = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Khoảng cách loại', y='Giá (tỷ)', data=data_quan, ax=ax5, palette=color,linewidth=2,edgecolor='k')

    ax5.grid(True, linestyle='--', alpha=0.4)
    ax5.xaxis.grid(False)  
    ax5.set_title(f'Giá Trung Bình Theo Khoảng Cách Tại {selected_quan}', weight='bold', fontsize=15)
    ax5.set_xlabel('Khoảng Cách', weight='bold', fontsize=12)
    ax5.set_ylabel('Giá Bán Trung Bình (Tỷ)', weight='bold', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig3)

    # Insight cho biểu đồ
    insight2 = """
    - Các bất động sản **càng gần trường học** thì giá sẽ **càng đắt** và ngược lại.
    """

    # Hiển thị insight
    st.markdown("### 💡 Insight:")
    st.markdown(insight2)
    st.markdown("---")

    # ======================== DASHBOARD 2 ========================
    st.header("3️⃣ Giá BĐS và Số Lượng Trường Theo Quận/Huyện")
    guide2 = """
    - Bạn có một mức giá đã định ra và đang phân vân không biết với mức giá đó thì có thể lựa chọn ở khu vực nào.
    - Biểu đồ bên dưới sẽ giúp bạn so sánh giá bất động sản với số lượng trường học để bạn có thể chọn ra được khu vực phù hợp với bạn nhất.
    """

    # Hiển thị insight
    st.markdown("#### 🔍 Guide:")
    st.markdown(guide2)


    truong_theo_quan = df_school.groupby('Khu vực')['Tên đơn vị'].nunique().reset_index()
    truong_theo_quan.rename(columns={'Tên đơn vị': 'Số Lượng Trường'}, inplace=True)
    bds_theo_quan = df_real_estate.groupby('Quận/Huyện')['Giá bán (triệu/m2)'].mean().reset_index()
    bds_theo_quan.rename(columns={'Giá bán (triệu/m2)': 'Giá BĐS Trung Bình (triệu/m2)'}, inplace=True)

    df_combined = pd.merge(bds_theo_quan, truong_theo_quan, left_on='Quận/Huyện', right_on='Khu vực', how='inner')
    df_combined = df_combined.sort_values(by='Giá BĐS Trung Bình (triệu/m2)', ascending=False)

    quans = st.multiselect("Chọn Quận/Huyện để hiển thị:", options=df_combined['Quận/Huyện'].unique(), default=df_combined['Quận/Huyện'].unique())
    df_filtered = df_combined[df_combined['Quận/Huyện'].isin(quans)]

    # st.markdown("---")
    fig2, ax3 = plt.subplots(figsize=(12,7))

    # Bar chart bên trái
    ax3.bar(
        df_filtered['Quận/Huyện'],
        df_filtered['Giá BĐS Trung Bình (triệu/m2)'],
        color='navy',
        #alpha=0.7,
        label='Giá BĐS Trung Bình'  # 
    )
    ax3.set_ylabel("Giá BĐS Trung Bình (triệu/m²)", color='navy')
    ax3.tick_params(axis='y', labelcolor='navy')
    ax3.set_xlabel("Khu vực", weight='bold', fontsize=12)
    ax3.set_ylim(0, 410)  # 👉 Giới hạn trục y
    ax3.set_xticklabels(df_filtered['Quận/Huyện'], rotation=45, ha='right')
    ax3.legend(loc='upper left')  
    ax3.grid(True, linestyle='--', alpha=0.4)


    # Line chart bên phải
    ax4 = ax3.twinx()
    ax4.plot(
        df_filtered['Quận/Huyện'],
        df_filtered['Số Lượng Trường'],
        color='orange',
        marker='o',
        #linewidth=2,
        label='Số Lượng Trường'  # 
    )
    ax4.set_ylabel("Số Lượng Trường", color='orange')
    ax4.tick_params(axis='y', labelcolor='orange')
    ax4.legend(loc='upper right')  # 

    plt.title("So Sánh Giữa Giá BĐS và Số Lượng Trường Học Theo Khu Vực", weight='bold', fontsize=15)
    plt.tight_layout()
    st.pyplot(fig2)

    guide2_1 = """
    - Sau khi bạn đã chọn được khu vực phù hợp mà bạn muốn mua nhất thì sau đây chúng ta hãy cùng tìm hiểu xem tình hình giáo dục tại khu vực này nào !!!
    """

    # Hiển thị insight
    st.markdown("#### 🔍 Guide:")
    st.markdown(guide2_1)

    # them
    def load_data(path: str):
        df = pd.read_excel(path)
        return df

    df = load_data('./processed_thpt_hcm.xlsx')

    # ======= 🎯 Chọn Quận/Huyện dùng chung =======
    if 'Quận/Huyện' in df.columns:
        selected_district = st.selectbox("📍 Chọn Quận/Huyện:", sorted(df['Quận/Huyện'].unique()))
    else:
        st.error("❌ Dữ liệu không có cột 'Quận/Huyện'.")
        st.stop()

    # ======= Tạo layout 2 cột =======
    col1, col2 = st.columns(2)
    # 🎨 Màu tùy chỉnh cho từng loại trường
    color_maps = {
        'Công lập': '#0571b0',       
        'Tư thục': '#92c5de',        
        'Trường chuyên': '#ca0020',  
        'Dân lập': '#f4a582'         
    }



    # ======= 🧁 Cột 1: Pie chart loại trường theo Quận/Huyện =======
    with col1:
        st.subheader("📌 Tỷ lệ Loại trường tại khu vực đã chọn")

        if 'Loại trường' in df.columns:
            filtered_df = df[df['Quận/Huyện'] == selected_district]

            type_counts = filtered_df['Loại trường'].value_counts().reset_index()
            type_counts.columns = ['Loại trường', 'Số lượng']

            fig_pie = px.pie(
                type_counts,
                names='Loại trường',
                values='Số lượng',
                title=f"Phân bố loại trường tại {selected_district}",
                hole=0.3,
                color='Loại trường',
                color_discrete_map=color_maps
            )
            fig_pie.update_layout(margin=dict(t=60, b=40, l=0, r=0))
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.error("❌ Dữ liệu không có cột 'Loại trường'.")

    # ======= 📊 Cột 2: Bar chart top 5 trường có điểm chuẩn cao nhất =======
    with col2:
        st.subheader("🏫 Top các trường có điểm chuẩn cao nhất tại khu vực")

        score_cols = [
            '2024_Điểm chuẩn nguyện vọng 1', '2023_Điểm chuẩn nguyện vọng 1', '2022_Điểm chuẩn nguyện vọng 1', '2021_Điểm chuẩn nguyện vọng 1',
            '2024_Điểm chuẩn nguyện vọng 2', '2023_Điểm chuẩn nguyện vọng 2', '2022_Điểm chuẩn nguyện vọng 2', '2021_Điểm chuẩn nguyện vọng 2',
            '2024_Điểm chuẩn nguyện vọng 3', '2023_Điểm chuẩn nguyện vọng 3', '2022_Điểm chuẩn nguyện vọng 3', '2021_Điểm chuẩn nguyện vọng 3'
        ]

        if all(col in df.columns for col in score_cols) and 'Tên đơn vị' in df.columns and 'Loại trường' in df.columns:
            df_district = df[df['Quận/Huyện'] == selected_district].copy()
            df_district['Điểm chuẩn TB'] = df_district[score_cols].mean(axis=1, skipna=True).round(2)
            df_district = df_district.dropna(subset=['Điểm chuẩn TB'])

            top5 = df_district[['Tên đơn vị', 'Loại trường', 'Điểm chuẩn TB']].sort_values(by='Điểm chuẩn TB', ascending=False).head(5)
            top5['Tên đơn vị'] = top5['Tên đơn vị'].str.title()


            # 🎨 Tạo color map giống bên pie chart
            unique_types = df['Loại trường'].dropna().unique()
            color_palette = px.colors.qualitative.Plotly
            color_map = {school_type: color_palette[i % len(color_palette)] for i, school_type in enumerate(unique_types)}

            # Ánh xạ màu cho từng trường theo loại trường
            top5['color'] = top5['Loại trường'].map(color_maps)

            # 🧱 Vẽ bar chart với màu tùy theo loại trường
            fig_bar = px.bar(
                top5,
                x='Điểm chuẩn TB',
                y='Tên đơn vị',
                orientation='h',
                color='Loại trường',
                color_discrete_map=color_maps,
                title=f"Top các trường có điểm chuẩn cao nhất tại {selected_district} ",
                labels={'Tên đơn vị': 'Tên trường'}
            )

            fig_bar.update_layout(
                yaxis_title=None,
                yaxis=dict(autorange='reversed'),
                margin=dict(t=60, b=40, l=0, r=0),
                showlegend=False,
                bargap=0.4,         # 👈 Tăng khoảng cách giữa các bar
                bargroupgap=0.2, 
                xaxis=dict(
                range=[top5['Điểm chuẩn TB'].min() - 1, top5['Điểm chuẩn TB'].max() + 1],
                showgrid=True,)  
            )

            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.error("❌ Thiếu cột 'Tên đơn vị', 'Loại trường' hoặc các cột điểm chuẩn.")

    guide = """
        ⭐**Mẹo**: Bạn có thể chọn 1 trường bất kì trong top các trường có điểm chuẩn cao từ biểu đồ bên trên và
        hãy cùng xem có các bất động sản nào đang rao bán xung quanh ngôi trường này bằng cách nhấn chọn 
        hệ thống gợi ý trong phần "Chọn phần" phía bên trái màn hình nhé !!!
        """

        # Hiển thị insight
    st.markdown("#### 🔍 Guide:")
    st.markdown(guide)

    
# ======================== GỢI Ý BĐS DỰA TRÊN TRƯỜNG HỌC ========================
elif sidebar_selection == "Gợi Ý BĐS Dựa Trên Trường Học":
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


