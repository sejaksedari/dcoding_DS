
# MEMBUAT STATIC DASHBOARD (Local) - Submisi Fuad Azaim Siraj - Dicoding

# README
# Setup Environment - Anaconda
    # conda create --name main-ds python=3.10.6
    # conda activate main-ds
    # pip install -r requirements.txt

# Setup Environment - Powershell
    # mkdir submission
    # cd submission
    # pip install -r requirements.txt

# Run Streamlit app
    # streamlit run dashboard.py


# Import Libraries ///////////////////////////
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
from babel.numbers import format_currency

# Set seaborn style
sns.set(style='dark')


# PREPARING DataFrame ///////////////////////////
# monthly_orders_df
def create_monthly_orders_df(df):

    # Ensure 'order_purchase_timestamp' is datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Resample and aggregate
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })

    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    # Calculate order count difference for highlighting
    monthly_orders_df['order_count_difference'] = monthly_orders_df['order_count'].diff()
    
    return monthly_orders_df


# orderByCity
def create_orderByCity(df):

    orderByCity = (
        df
        .groupby(by="customer_city")
        .order_id.nunique()
        .sort_values(ascending=False)
        .reset_index()
    )

    # hitung jumlah unique orders
    total_orders = df.order_id.nunique()

    # tambahkan kolom persentase unique orders
    orderByCity['order_percentage'] = (orderByCity['order_id'] / total_orders) * 100

    return orderByCity


# orderByState
def create_orderByState(df):

    orderByState = (
        df
        .groupby(by="customer_state")
        .order_id.nunique()
        .sort_values(ascending=False)
        .reset_index()
    )

    # hitung jumlah unique orders
    total_orders = df.order_id.nunique()

    # tambahkan kolom persentase unique orders
    orderByState['order_percentage'] = (orderByState['order_id'] / total_orders) * 100

    return orderByState


#rfm_df
def create_rfm_df(df):

    # persent day
    present_day = df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    # Buat dataFrame Recency
    recency_df= pd.DataFrame(df.groupby(by='customer_unique_id', as_index=False)['order_purchase_timestamp'].max())
    recency_df['Recency']= recency_df['order_purchase_timestamp'].apply(lambda x: (present_day - x).days)
    # Buat dataFrame Frequency
    frequency_df = pd.DataFrame(df.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index())
    frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
    # Buat dataFrame Monetary
    monetary_df = df.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
    monetary_df.columns = ['customer_unique_id', 'Monetary']

    # dataframe rfm
    rfm_df = recency_df.merge(frequency_df, on='customer_unique_id')
    rfm_df = rfm_df.merge(monetary_df, on='customer_unique_id')
    rfm_df["recent_date"] = present_day
    rfm_df = rfm_df.drop(columns=['order_purchase_timestamp', 'recent_date'])

    return rfm_df


# # load berkas data CSV
# all_df = pd.read_csv("all_data.csv")



# Ensure the current working directory is correct
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, "all_data.csv")

# Load the CSV file
try:
    all_df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    st.error(f"File not found: {csv_file_path}")
    st.stop()



# /// PLOT FUNCTION BELOW //////////////////////////////

# Function to plot Monthly Orders Trend
def plot_monthly_orders_trend():
    fig, ax = plt.subplots(figsize=(10, 7))
    x_values = range(len(monthly_orders_df))
    ax.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["order_count"], marker='o', linewidth=1, color="#72BCD4")

    # Cari index bulan dengan highest increase dan lowest drop
    max_increase_index = monthly_orders_df['order_count_difference'].idxmax()
    min_decrease_index = monthly_orders_df['order_count_difference'].idxmin()

    # Regression line
    regression_coefficients = np.polyfit(x_values, monthly_orders_df['order_count'], 1)
    regression_line = np.polyval(regression_coefficients, x_values)
    ax.plot(monthly_orders_df['order_purchase_timestamp'], regression_line, color='green', linestyle='--', label='Regression Line')

    # Cari bulan dengan highest increase in order_count
    max_increase_month = monthly_orders_df.loc[max_increase_index, 'order_purchase_timestamp']
    max_increase = monthly_orders_df['order_count_difference'].max()

    # Cari bulan dengan lowest drop di order_count
    min_decrease_month = monthly_orders_df.loc[min_decrease_index, 'order_purchase_timestamp']
    min_decrease = monthly_orders_df['order_count_difference'].min()

    # Beri anotasi global top order_count
    max_order_count = monthly_orders_df['order_count'].max()
    max_order_month = monthly_orders_df.loc[monthly_orders_df['order_count'].idxmax(), 'order_purchase_timestamp']
    plt.annotate(f'Highest Count: {max_order_count} @ {max_order_month}', xy=(max_order_month, max_order_count), xytext=(-200, -50),
                textcoords='offset points', arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='black'))

    # Beri anotasi lowest drop value
    plt.annotate(f'Lowest Drop: {min_decrease}', xy=(min_decrease_month, monthly_orders_df.loc[monthly_orders_df['order_purchase_timestamp'] == min_decrease_month, 'order_count'].iloc[0]), xytext=(50, -50),
                textcoords='offset points', arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='black'))

    # Beri anotasi highest rising value
    plt.annotate(f'Highest Rising: +{max_increase}', xy=(max_increase_month, monthly_orders_df.loc[max_increase_index, 'order_count']), xytext=(-200, -100),
                textcoords='offset points', arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', color='black'))

    # highlight green red highest rising dan lowest drop
    if max_increase_index > 0:  # Pastikan tidak di luar bounds
        highlight_start = monthly_orders_df['order_purchase_timestamp'].iloc[max_increase_index - 1]
        highlight_end = monthly_orders_df['order_purchase_timestamp'].iloc[max_increase_index]
        ax.axvspan(highlight_start, highlight_end, color='lightgreen', alpha=0.5)
    if min_decrease_index > 0:  # Pastikan tidak di luar bounds
        highlight_start = monthly_orders_df['order_purchase_timestamp'].iloc[min_decrease_index - 1]
        highlight_end = monthly_orders_df['order_purchase_timestamp'].iloc[min_decrease_index]
        ax.axvspan(highlight_start, highlight_end, color='red', alpha=0.3)

    ax.set_xlabel('Year - Month')
    ax.set_ylabel('Order Count')
    ax.set_title("Monthly Orders Trend", fontsize=20)
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)



# Function to plot Customer Order by Region
def plot_customer_order_by_region():
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(13, 12))
    colors = ["#F47174", "#F47174", "#F47174", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
    plt.grid(True)

    # ORDER BY CITY
    sns.barplot(x="order_id", y="customer_city", data=orderByCity.sort_values(by="order_id", ascending=False).head(10), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Order by City (Top Ten)", fontsize=15)
    for p in ax[0].patches:
        width = p.get_width()
        ax[0].annotate(f'{width:.0f}\n({width/orderByCity["order_id"].sum():.1%})', (p.get_x() + width, p.get_y() + p.get_height() / 2), ha='left', va='center', fontsize=10, color='black', xytext=(5, 0), textcoords='offset points')

    # ORDER BY STATE
    sns.barplot(x="order_id", y="customer_state", data=orderByState.sort_values(by="order_id", ascending=False).head(10), palette=colors, ax=ax[1])
    ax[1].set_ylabel('State Abbreviation')
    ax[1].set_xlabel(None)
    ax[1].set_title("Order By State (Top Ten)", fontsize=15)
    for p in ax[1].patches:
        width = p.get_width()
        ax[1].annotate(f'{width:.0f}\n({width/orderByState["order_id"].sum():.1%})', (p.get_x() + width, p.get_y() + p.get_height() / 2), ha='left', va='center', fontsize=10, color='black', xytext=(5, 0), textcoords='offset points')

    st.pyplot(fig)


# Function to plot Best Customer based on RFM parameters
def plot_best_customers_rfm():
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(13, 12))
    colors = ["#F47174", "#F47174", "#F47174", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
    # colors = ["#72BCD4"] * 10

    # RECENCY
    sns.barplot(x="Recency", y="customer_unique_id", data=rfm_df.sort_values(by="Recency", ascending=True).head(10), palette=colors, ax=ax[0])
    ax[0].set_ylabel('customer_unique_id')
    ax[0].set_xlabel(None)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=15)
    ax[0].tick_params(axis ='y', labelsize=10)
    ax[0].grid(True)

    # FREQUENCY
    sns.barplot(x="Frequency", y="customer_unique_id", data=rfm_df.sort_values(by="Frequency", ascending=False).head(10), palette=colors, ax=ax[1])
    ax[1].set_ylabel('customer_unique_id')
    ax[1].set_xlabel(None)
    ax[1].set_title("By Frequency", loc="center", fontsize=15)
    ax[1].tick_params(axis ='y', labelsize=10)
    ax[1].grid(True)

    # MONETARY
    sns.barplot(x="Monetary", y="customer_unique_id", data=rfm_df.sort_values(by="Monetary", ascending=False).head(10), palette=colors, ax=ax[2])
    ax[2].set_ylabel('customer_unique_id')
    ax[2].set_xlabel(None)
    ax[2].set_title("By Monetary", loc="center", fontsize=15)
    ax[2].tick_params(axis ='y', labelsize=10)
    ax[2].grid(True)
    for p in ax[2].patches:
        width = p.get_width()
        ax[2].annotate(f'{format_currency(width, "USD", locale="en_US")}', (p.get_x() + width, p.get_y() + p.get_height() / 2), ha='left', va='center', fontsize=10, color='black', xytext=(5, 0), textcoords='offset points')

    st.pyplot(fig)



# Streamlit app structure
st.title("Static Dashboard E-Commerce")

st.subheader("Description :fire:")

multi = '''Selamat Datang di halaman ***Static Dashboard E-Commerce***!
Di sini, Anda dapat melihat hasil visualisasi data yang telah diproses untuk melihat
beberapa *insight* dari dataset E-Commerce. Ini merupakan tugas akhir pada Course Dicoding 
**"Belajar Analisis Data dengan Python,"** di mana kita bisa belajar mengaplikasikan ilmu dasar
mengenai *Data Science* dan penerapannya di berbagai sektor.

Berikut pertanyaan umum yang diajukan saat proses Exploratory Data Analysis (EDA):
1. Bagaimana Tren Penjualan secara umum?
2. Bagaimana Demografi Pembeli jika didasarkan pada Wilayah?
3. Kapan, seberapa sering, dan seberapa banyak pelanggan bertransaksi? Siapa pelanggan ini?

Setelah melalui Data wrangling (gathering, assessing, cleaning) & EDA, langkah terakhir
adalah membuat visualisasi guna menjawab pertanyaan sebelumnya. Untuk saat ini, dashboard yang
dikembangkan masih berupa dashboard statis.

Kedepannya, akan ada pengembangan lanjutan baik dalam proses EDA seperti penggunaan teknik lanjutan
seperti geoanalysis, clustering, dsb. serta pengembangan dari segi dashboard yang interaktif.

Salam Hangat & Terima Kasih, :muscle: 

Fuad Azaim Siraj

'''
st.markdown(multi)
st.subheader('   ', divider='rainbow')

# Panggil monthly_orders_df
monthly_orders_df = create_monthly_orders_df(all_df)
st.subheader("Monthly Orders Trend")
multi = '''
***Monthly Orders Trend***
* Grafik menunjukkan kenaikan jumlah order bulanan, kecuali pada 8 bulan terakhir (stagnansi di order range 6000-7000)
* Jumlah order terbanyak di November 2017 (7288 order)
* Peningkatan tertinggi terjadi antara Oktober-November 2017 (+2810)
* Penurunan tertinggi terjadi sebulan setelahnya antara November-Desember (-1775)

'''
st.markdown(multi)
plot_monthly_orders_trend()
st.subheader('   ', divider='rainbow')


orderByCity = create_orderByCity(all_df)
orderByState = create_orderByState(all_df)
st.subheader("Customer Order by Region")
multi = '''
***Top 3 order by city***
* sao paulo = 15044, 15.59%
* rio de janeiro = 6603, 6.84%
* belo horizonte = 2697, 2.79%

***Top 3 order by state***
*	SP (Sao Paulo) =	40489,	41.97 %
*	RJ (Rio de Janeiro)=	12351,	12.80 %
*	MG (Minas Gerais) =	11352,	11.76 %

'''
st.markdown(multi)
plot_customer_order_by_region()
st.subheader('   ', divider='rainbow')


rfm_df = create_rfm_df(all_df)
st.subheader("Best Customer based on RFM Parameters")
multi = '''
Dari visualisasi data 'Best Customer Based on RFM Parameters. Kita bisa menemukan 10 sampel customer terbaik dari segi:

* Recency
    * Menggunakan asumsi present_date adalah 1 hari setelah tanggal terakhir yang ada di dataset, kita bisa melihat 10 customer yang melakukan transaksi terakhir (2018-08-29 15:00:37)
* Frequency
    * Terlihat pada bar chart, ada 10 sampel customer yang paling sering bertransaksi dan pada urutan teratas ada 1 customer yang sangat loyal karena dia telah melakukan 14 kali purchase.
* Monetary
    * Secara nominal transaksi, terdapat 1 customer yang mungkin cocok dijadikan sebagai customer prioritas karena dia telah melakukan transaksi dengan total nominal 100.000 (asumsi unit currency = BRL atau Brazilian Real)

'''
st.markdown(multi)
plot_best_customers_rfm()
st.subheader('   ', divider='rainbow')

st.caption('Final Project by Dicoding Student - Fuad Azaim Siraj 2024')