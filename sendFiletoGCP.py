import os
from google.cloud import storage

# Kimlik doğrulama dosyasının yolunu belirt
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creating-data-1234566778.json"

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    try:
        # Google Cloud Storage istemcisi oluştur
        client = storage.Client()

        # Belirtilen bucket'ı al
        bucket = client.bucket(bucket_name)

        # Bucket içinde yeni bir blob oluştur ve dosyayı yükle
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Parametreleri doldur ve çalıştır
bucket_name = "supplychain_gcp"  # Kendi bucket adını buraya ekle
source_file_name = "supply_chain_data.csv"  # Yüklemek istediğin dosyanın yolunu ekle
destination_blob_name = "supplychain_gcp/supply_chain_data.csv"  # Dosya adı veya bucket içindeki klasörle birlikte dosya yolu

upload_to_gcs(bucket_name, source_file_name, destination_blob_name)