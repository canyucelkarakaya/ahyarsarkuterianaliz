import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Birleştirilmiş Excel dosyasını oku
combined_df = pd.read_excel('combined_excel.xlsx')

# Streamlit uygulamasını başlat
st.title("2022 ve 2023 Yıllarına Ait Dosyalardaki Ürün Miktarları")

# 'Tarih' sütunundaki değerlerin sayısını hesapla
counts = combined_df['Tarih'].value_counts()

# Sonuçları göster
st.write("2022 ve 2023 Yıllarına Ait Ürün Miktarları:")
st.write(counts)

# Birleştirilmiş Excel dosyasını oku
combined_df = pd.read_excel('combined_excel.xlsx')

# Streamlit uygulamasını başlat
st.title("Dosya İçerisinde Eşleşen ve Eşleşmeyen Ürün Miktarları")

# Eşleşen ve eşleşmeyen ürünleri bulmak için gruplama yapın
grouped = combined_df.groupby('Kodu')

matching_count = 0
non_matching_count = 0

for code, group in grouped:
    if len(group['Tarih'].unique()) == 2:
        matching_count += 1
    else:
        non_matching_count += 1

# Sonuçları göster
st.write(f"Eşleşen {matching_count} ürün var.")
st.write(f"Eşleşmeyen {non_matching_count} ürün var.")

# Excel dosyasını oku
@st.cache_data
def load_data():
    return pd.read_excel('eşleşen_ürünler.xlsx')

# Streamlit uygulamasını başlat
st.title("Ürün Karşılaştırma Uygulaması")

# Veriyi yükle
data = load_data()

# Ürün açıklamalarını al
unique_aciklamalar = data['Açıklama'].unique()

# Açıklama seçimini kullanıcıya bırak
selected_aciklama = st.selectbox("Ürün Açıklaması Seçin:", unique_aciklamalar)

# Seçilen açıklama için filtrele
selected_data = data[data['Açıklama'] == selected_aciklama]

# İlgili yılların miktarlarını ve açıklamayı al
miktar_2022 = selected_data['2022'].values[0]
miktar_2023 = selected_data['2023'].values[0]
aciklama = selected_data['Açıklama'].values[0]

# Artış veya azalışı hesapla
artis_azalis = miktar_2023 - miktar_2022
renk = 'green' if artis_azalis > 0 else 'red'

# Verileri bir çubuk grafikte göster
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(['2022', '2023'], [miktar_2022, miktar_2023], color=['blue', 'green'])
ax.text('2022', miktar_2022, str(miktar_2022), ha='center', va='bottom', fontsize=12)
ax.text('2023', miktar_2023, str(miktar_2023), ha='center', va='bottom', fontsize=12)
ax.set_xlabel('Yıl')
ax.set_ylabel('Miktar')
ax.set_title(f'{aciklama} Ürününün 2022 ve 2023 Miktar Karşılaştırması')
ax.bar('Artış/Azalış', artis_azalis, color=renk)
ax.text('Artış/Azalış', artis_azalis, f'{artis_azalis} ({artis_azalis/miktar_2022:.2%})', ha='center', va='bottom', fontsize=12)
plt.xticks(rotation=45)

# Streamlit'e görseli göster
st.pyplot(fig)

