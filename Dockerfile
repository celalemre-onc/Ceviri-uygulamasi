# Python 3.9 slim tabanlı imaj kullan
FROM python:3.9-slim

# Çalışma dizinini belirle
WORKDIR /app

# Argos Translate için kullanılacak dizini belirt
ENV ARGOSTRANSLATE_HOME=/app/.argos_translate

# Pip ile yüklenen CLI betiklerinin bulunduğu dizini PATH'e ekle
ENV PATH="/root/.local/bin:${PATH}"

# Sadece requirements.txt dosyasını kopyala (bağımlılıkların cache'lenmesi için)
COPY requirements.txt /app/requirements.txt

# Gerekli Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Argos Translate için model dosyalarını saklayacağımız dizini oluştur
RUN mkdir -p /app/.argos_translate

# Model indeksini güncelle
RUN python -c "import argostranslate.package as pkg; pkg.update_package_index()"

# Eğer model dosyanız yerel olarak varsa, kopyalayın
COPY en_tr.argosmodel /app/.argos_translate/en_tr.argosmodel

# Modeli yükle (elle kopyalanan model dosyasını kur)
RUN python -c "import argostranslate.package as pkg; pkg.install_from_path('/app/.argos_translate/en_tr.argosmodel')"

# Uygulama dosyalarını kopyala
COPY . /app

# Çeviri scriptini çalıştır (örn. konteynır başlatıldığında)
CMD ["python", "translate_po.py"]
