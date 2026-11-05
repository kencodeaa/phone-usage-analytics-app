import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Phone Usage Analytics - Lớp 9B",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Áp dụng Custom CSS Giao diện Dark & Blue Mode
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-weight: 700;
    }
    div[data-baseweb="tab-list"] {
        background-color: #111827;
        border-radius: 8px;
        padding: 4px;
    }
    button[data-baseweb="tab"] {
        color: #9ca3af !important;
    }
    button[aria-selected="true"] {
        color: #60a5fa !important;
        background-color: #1f2937 !important;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Khai báo dữ liệu mẫu 30 học sinh (Ẩn danh, bảo mật)
INITIAL_DATA = [
    {'Mã HS': 'HS01', 'Thời gian dùng ĐT (giờ)': 1.1, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:15', 'Giờ thức dậy': '06:45', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS02', 'Thời gian dùng ĐT (giờ)': 0.5, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '23:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS03', 'Thời gian dùng ĐT (giờ)': 4.1, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:30', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS04', 'Thời gian dùng ĐT (giờ)': 3.8, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:45', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS05', 'Thời gian dùng ĐT (giờ)': 5.2, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '00:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS06', 'Thời gian dùng ĐT (giờ)': 1.8, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS07', 'Thời gian dùng ĐT (giờ)': 2.5, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:00', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS08', 'Thời gian dùng ĐT (giờ)': 4.5, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '00:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS09', 'Thời gian dùng ĐT (giờ)': 1.2, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:00', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS10', 'Thời gian dùng ĐT (giờ)': 3.0, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:30', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS11', 'Thời gian dùng ĐT (giờ)': 0.8, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS12', 'Thời gian dùng ĐT (giờ)': 4.8, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '00:00', 'Giờ thức dậy': '05:30', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS13', 'Thời gian dùng ĐT (giờ)': 2.2, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '23:00', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS14', 'Thời gian dùng ĐT (giờ)': 1.5, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:45', 'Giờ thức dậy': '06:45', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS15', 'Thời gian dùng ĐT (giờ)': 5.5, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '01:00', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS16', 'Thời gian dùng ĐT (giờ)': 3.2, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS17', 'Thời gian dùng ĐT (giờ)': 0.9, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS18', 'Thời gian dùng ĐT (giờ)': 4.2, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:45', 'Giờ thức dậy': '05:45', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS19', 'Thời gian dùng ĐT (giờ)': 2.7, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:00', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS20', 'Thời gian dùng ĐT (giờ)': 1.9, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS21', 'Thời gian dùng ĐT (giờ)': 3.6, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:30', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS22', 'Thời gian dùng ĐT (giờ)': 0.7, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:00', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS23', 'Thời gian dùng ĐT (giờ)': 4.9, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '00:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS24', 'Thời gian dùng ĐT (giờ)': 2.1, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '23:00', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS25', 'Thời gian dùng ĐT (giờ)': 1.4, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS26', 'Thời gian dùng ĐT (giờ)': 5.0, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '00:30', 'Giờ thức dậy': '06:00', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS27', 'Thời gian dùng ĐT (giờ)': 3.4, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:30', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS28', 'Thời gian dùng ĐT (giờ)': 1.0, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '22:15', 'Giờ thức dậy': '06:15', 'Đánh giá giấc ngủ': 'Có'},
    {'Mã HS': 'HS29', 'Thời gian dùng ĐT (giờ)': 4.3, 'Dùng 1h trước khi ngủ': 'Có', 'Giờ đi ngủ': '23:45', 'Giờ thức dậy': '05:45', 'Đánh giá giấc ngủ': 'Không'},
    {'Mã HS': 'HS30', 'Thời gian dùng ĐT (giờ)': 2.8, 'Dùng 1h trước khi ngủ': 'Không', 'Giờ đi ngủ': '23:00', 'Giờ thức dậy': '06:30', 'Đánh giá giấc ngủ': 'Có'}
]

@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_excel("Demo_Nhom_B.xlsx")
    except Exception:
        df = pd.DataFrame(INITIAL_DATA)
    
    # Tính thời lượng ngủ qua đêm (Excel MOD logic)
    def calc_sleep(bed, wake):
        try:
            b = datetime.strptime(str(bed), "%H:%M")
            w = datetime.strptime(str(wake), "%H:%M")
            diff = (w - b).total_seconds() / 3600
            if diff < 0:
                diff += 24
            return round(diff, 1)
        except:
            return 7.0

    df['Thời lượng ngủ (giờ)'] = df.apply(lambda r: calc_sleep(r['Giờ đi ngủ'], r['Giờ thức dậy']), axis=1)
    df['Nhóm ĐT'] = df['Thời gian dùng ĐT (giờ)'].apply(lambda x: 'Nhóm 1' if x < 2 else ('Nhóm 2' if x <= 4 else 'Nhóm 3'))
    df['Cảnh báo ĐT'] = df['Thời gian dùng ĐT (giờ)'].apply(lambda x: 'CẦN XEM LẠI THÓI QUEN' if x > 4 else 'DUY TRÌ CÂN BẰNG')
    df['Cảnh báo giấc ngủ'] = df.apply(
        lambda r: 'CẦN QUAN TÂM GIẤC NGỦ' if r['Thời lượng ngủ (giờ)'] < 8 
        else ('LƯU Ý MÀN HÌNH TRƯỚC NGỦ' if r['Dùng 1h trước khi ngủ'] == 'Có' else 'THEO DÕI THÓI QUEN'), 
        axis=1
    )
    # Loại bỏ cột tên nếu tồn tại
    if 'Họ và Tên' in df.columns:
        df = df.drop(columns=['Họ và Tên'])
    return df

df = load_and_process_data()

# Header
st.title("📱 PHONE USAGE ANALYTICS")
st.caption("Hệ thống Khảo sát Thời gian Sử dụng Điện thoại & Giấc ngủ - Lớp 9B (30 Học sinh - Bảo mật ẩn danh)")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Tổng Quan", "📋 Bảng Dữ Liệu Khảo Sát", "⚙️ Công Thức Excel", "📄 Báo Cáo & Xuất Dữ Liệu"])

# TAB 1: DASHBOARD
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    total_students = len(df)
    avg_screen = round(df['Thời gian dùng ĐT (giờ)'].mean(), 1)
    avg_sleep = round(df['Thời lượng ngủ (giờ)'].mean(), 1)
    screen_before_bed = len(df[df['Dùng 1h trước khi ngủ'] == 'Có'])
    alert_count = len(df[(df['Nhóm ĐT'] == 'Nhóm 3') | (df['Thời lượng ngủ (giờ)'] < 8)])

    col1.metric("Tổng Học Sinh", f"{total_students} HS")
    col2.metric("Thới Gian Dùng ĐT TB", f"{avg_screen} h")
    col3.metric("Thời Lượng Ngủ TB", f"{avg_sleep} h")
    col4.metric("Dùng ĐT Trước Ngủ", f"{screen_before_bed} HS")
    col5.metric("Cảnh Báo Lưu Ý", f"{alert_count} HS")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Phân Phối Theo Nhóm ĐT")
        group_counts = df['Nhóm ĐT'].value_counts().reset_index()
        group_counts.columns = ['Nhóm ĐT', 'Số lượng']
        fig_bar = px.bar(group_counts, x='Nhóm ĐT', y='Số lượng', color='Nhóm ĐT',
                         color_discrete_map={'Nhóm 1': '#3b82f6', 'Nhóm 2': '#60a5fa', 'Nhóm 3': '#ef4444'},
                         template="plotly_dark")
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Dùng Điện Thoại 1h Trước Khi Ngủ")
        fig_pie = px.pie(df, names='Dùng 1h trước khi ngủ', color='Dùng 1h trước khi ngủ',
                         color_discrete_map={'Có': '#f59e0b', 'Không': '#3b82f6'},
                         template="plotly_dark")
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Tương Quan Thời Gian Dùng ĐT & Giấc Ngủ")
    fig_corr = go.Figure()
    fig_corr.add_trace(go.Bar(x=df['Mã HS'], y=df['Thời gian dùng ĐT (giờ)'], name='Dùng ĐT (h)', marker_color='#ef4444'))
    fig_corr.add_trace(go.Scatter(x=df['Mã HS'], y=df['Thời lượng ngủ (giờ)'], name='Thời lượng ngủ (h)', line=dict(color='#3b82f6', width=3)))
    fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_corr, use_container_width=True)

# TAB 2: DATA TABLE
with tab2:
    st.subheader("Bảng Dữ Liệu Tương Tác Bảo Mặt (Không hiển thị Họ tên)")
    search_kw = st.text_input("Tìm kiếm theo Mã HS:")
    filtered_df = df.copy()
    if search_kw:
        filtered_df = filtered_df[filtered_df['Mã HS'].str.contains(search_kw, case=False)]
    st.dataframe(filtered_df, use_container_width=True)

# TAB 3: FORMULAS
with tab3:
    st.subheader("Ánh Xạ Công Thức Excel Sang Python / JS")
    st.code("""
# Excel COUNTIF
len(df[df['Nhóm ĐT'] == 'Nhóm 1'])

# Excel SUMIF
df[df['Nhóm ĐT'] == 'Nhóm 1']['Thời gian dùng ĐT (giờ)'].sum()

# Excel MOD (Tính thời gian ngủ qua đêm)
diff = (wake_time - bed_time).seconds / 3600
if diff < 0: diff += 24
    """, language="python")

# TAB 4: REPORT
with tab4:
    st.subheader("Xuất Báo Cáo")
    st.download_button(
        label="📥 Tải Báo Cáo (.CSV)",
        data=df.to_csv(index=False).encode('utf-8-sig'),
        file_name=f"Anonymized_Phone_Usage_Analytics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )