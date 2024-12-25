import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    all_data_df = pd.read_csv('all_data.csv')
    return all_data_df

# Fungsi untuk menghitung harga rata-rata per kategori produk
def plot_avg_price_by_category(all_data_df):
    avg_price_by_category = all_data_df.groupby('product_category_name')['price'].mean().sort_values(ascending=False)
    top_10_categories = avg_price_by_category.head(10)
    
    plt.figure(figsize=(12, 8))
    top_10_categories.plot(kind='bar', color='skyblue')
    plt.title('Harga Rata-Rata per Kategori Produk (10 Teratas)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Harga Rata-Rata')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.write("10 Kategori Produk dengan Harga Rata-Rata Tertinggi:")
    st.write(top_10_categories)

    bottom_10_categories = avg_price_by_category.tail(10)
    plt.figure(figsize=(12, 8))
    bottom_10_categories.plot(kind='bar', color='lightcoral')
    plt.title('Harga Rata-Rata per Kategori Produk (10 Terbawah)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Harga Rata-Rata')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.write("10 Kategori Produk dengan Harga Rata-Rata Terendah:")
    st.write(bottom_10_categories)

# Fungsi untuk visualisasi jumlah produk per kota
def plot_city_product_purchase(all_data_df):
    city_product_purchase = all_data_df.groupby('customer_city')['order_id'].count()
    top_5_cities = city_product_purchase.nlargest(5)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_5_cities.index, y=top_5_cities.values, palette='viridis')
    plt.title('5 Kota Teratas dengan Pembelian Produk Terbanyak', fontsize=16)
    plt.xlabel('Kota Pengiriman', fontsize=12)
    plt.ylabel('Jumlah Pembelian Produk', fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.write("5 Kota dengan Pembelian Produk Terbanyak:")
    st.write(top_5_cities)

# Fungsi untuk visualisasi produk terbanyak per kategori di kota tertentu
def plot_top_categories_by_city(all_data_df, city_name):
    sp_df = all_data_df[all_data_df['customer_city'] == city_name]
    category_counts_sp = sp_df['product_category_name'].value_counts()
    top_10_categories_sp = category_counts_sp.head(10)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_categories_sp.values, y=top_10_categories_sp.index, palette='viridis')
    plt.title(f'10 Kategori Produk Paling Banyak Dibeli di Kota {city_name.title()}', fontsize=16)
    plt.xlabel('Jumlah Pembelian Produk', fontsize=12)
    plt.ylabel('Kategori Produk', fontsize=12)
    st.pyplot(plt)

    st.write(f"10 Kategori Produk Paling Banyak Dibeli di Kota {city_name.title()}:")
    st.write(top_10_categories_sp)

# Layout Streamlit
st.title("Dashboard Penjualan Produk")

# Load data
all_data_df = load_data()

# Pilihan sidebar untuk fitur interaktif
st.sidebar.title("Pilih Opsi untuk Visualisasi")

# Pilih jenis visualisasi
option = st.sidebar.selectbox(
    'Pilih Visualisasi',
    ('Harga Rata-Rata per Kategori Produk', 'Pembelian Produk per Kota', 'Top Kategori Produk per Kota')
)

if option == 'Harga Rata-Rata per Kategori Produk':
    plot_avg_price_by_category(all_data_df)

elif option == 'Pembelian Produk per Kota':
    plot_city_product_purchase(all_data_df)

elif option == 'Top Kategori Produk per Kota':
    city_name = st.sidebar.selectbox(
        'Pilih Kota',
        ('sao paulo', 'rio de janeiro', 'belo horizonte', 'brasilia', 'curitiba')
    )
    plot_top_categories_by_city(all_data_df, city_name)
