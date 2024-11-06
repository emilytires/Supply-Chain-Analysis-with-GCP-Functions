from google.cloud import storage
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import glob
import os
import config

def download_csv_from_gcs(bucket_name, source_blob_name, destination_file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"File downloaded from GCS bucket '{bucket_name}' as '{destination_file_name}'.")

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")


def clean_data(file_path):
    data = pd.read_csv(file_path)

    fig = px.scatter(data, x='Price', y='Revenue generated',
                     color='Product type',
                     hover_data=['Number of products sold'],
                     trendline='ols'
                     )
    # Metni birkaç satır olarak manuel bölme
    annotations = [
        "Thus, the company derives more revenue from skincare products,",
        "and the higher the price of skincare products,",
        "the more revenue they generate."
    ]
    # Her satır için bir annotation ekleme
    for i, line in enumerate(annotations):
        fig.add_annotation(
            x=0.5,  # Ortada konumlandırmak için
            y=-0.15 - (i * 0.05),  # Her satırı biraz daha aşağı yerleştirmek için
            xref="paper",
            yref="paper",
            text=line,
            showarrow=False,
            font=dict(size=6)
        )
    fig.write_image("/tmp/plot1.png")

    sales_data = data.groupby('Product type')['Number of products sold'].sum().reset_index()
    pie_chart = px.pie(sales_data, values='Number of products sold', names='Product type',
                       title='Sales by Product Type',
                       hover_data=['Number of products sold'],
                       hole=0.45,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    pie_chart.update_traces(textposition='inside', textinfo='percent')
    pie_chart.write_image("/tmp/plot2.png")

    trans_data = data.groupby('Transportation modes')['Number of products sold'].sum().reset_index()
    pie_chart = px.pie(trans_data, values='Number of products sold', names='Transportation modes',
                       title='Sales by Transportation modes',
                       hover_data=['Number of products sold'],
                       hole=0.5)
    pie_chart.update_traces(textposition='inside', textinfo='percent+label')
    pie_chart.write_image("/tmp/plot3.png")

    total_revenue = data.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_revenue['Shipping carriers'],
                         y=total_revenue['Revenue generated']))
    fig.update_layout(title='Total revenue by shipping carrier',
                      xaxis_title='Shipping carrier',
                      yaxis_title='Revenue Generated')
    fig.write_image("/tmp/plot4.png")

    total_revenue = data.groupby('Location')['Revenue generated'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_revenue['Location'],
                         y=total_revenue['Revenue generated']))
    fig.update_layout(title='Total Revenue based on location',
                      xaxis_title='Locations',
                      yaxis_title='Revenue generated')
    fig.write_image("/tmp/plot5.png")

    total_revenue = data.groupby('Transportation modes')['Revenue generated'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=total_revenue['Transportation modes'],
                         y=total_revenue['Revenue generated']))
    fig.update_layout(title='Total Revenue based on Transportation modes',
                      xaxis_title='Transportation modes',
                      yaxis_title='Revenue generated')
    fig.write_image("/tmp/plot6.png")

    stock_chart = px.line(data, x='SKU',
                          y='Stock levels',
                          title='Stock Levels by SKU')
    stock_chart.write_image("/tmp/plot7.png")

    order_quantity_chart = px.bar(data, x='SKU',
                                  y='Order quantities',
                                  title='Order Quantity by SKU')
    order_quantity_chart.write_image("/tmp/plot8.png")

    shipping_cost_chart = px.bar(data, x='Shipping carriers',
                                 y='Shipping costs',
                                 title='Shipping Costs by Carrier')
    shipping_cost_chart.write_image("/tmp/plot9.png")

    transportation_chart = px.pie(data,
                                  values='Costs',
                                  names='Transportation modes',
                                  title='Cost Distribution by Transportation Mode',
                                  hole=0.5,
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
    transportation_chart.update_traces(textposition='inside', textinfo='percent+label')
    transportation_chart.write_image("/tmp/plot10.png")

    defect_rate_by_product = data.groupby('Product type')['Defect rates'].mean().reset_index()
    fig = px.bar(defect_rate_by_product, x='Product type', y='Defect rates',
                 title='Average defect rates by product type')
    fig.write_image("/tmp/plot11.png")

    trans = data.groupby('Transportation modes')['Defect rates'].mean().reset_index()
    trans_chart = px.pie(trans, values='Defect rates',
                         names='Transportation modes',
                         title='Defect Rates by Transportation Mode',
                         hole=0.5,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
    trans_chart.update_traces(textposition='inside', textinfo='label+percent')
    trans_chart.write_image("/tmp/plot12.png")

    # Tüm PNG dosyalarını PDF'ye ekle
    image_files = glob.glob("/tmp/*.png")
    image_list = [Image.open(img).convert("RGB") for img in image_files]
    pdf_path = "/tmp/SupplyChainAnalysis.pdf"
    image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
    print(f"All plots combined into {pdf_path}")

    # PNG dosyalarını temizle
    for file_path in image_files:
        os.remove(file_path)
        print(f"Deleted {file_path}")

    return pdf_path


# Ana işlev
def main(event, context):
    bucket_name = "supplychain_gcp"
    source_blob_name = "supply_chain_data.csv"
    destination_file_name = "/tmp/downloaded_file.csv"

    # GCS'den dosya indir
    download_csv_from_gcs(bucket_name, source_blob_name, destination_file_name)

    # Veriyi temizle ve PDF'yi döndür
    pdf_path = clean_data(destination_file_name)
    print("Data cleaned and saved to PDF.")

    # PDF dosyasını Cloud Storage'a geri yükle
    upload_to_gcs(bucket_name, pdf_path, "SupplyChainAnalysis.pdf")