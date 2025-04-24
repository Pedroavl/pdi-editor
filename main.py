import streamlit as st
from PIL import Image
import numpy as np
import os

# Configurações da interface
st.set_page_config(page_title="Editor de Imagens - Processamento Digital de Imagens", layout="centered")
st.title("🖼️ Carregamento e Salvamento de Imagens")

# Criação da pasta de saída
os.makedirs("output", exist_ok=True)

# Upload
uploaded_file = st.file_uploader("📂 Selecione uma imagem", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Imagem Recebida")
    st.image(image, use_container_width=True)

    # Verifica se é RGB, converte para tons de cinza
    if image.mode == "RGB":
        gray_image = image.convert("L")
        st.subheader("Convertida para Tons de Cinza")
        st.image(gray_image, use_container_width=True)
    else:
        gray_image = image

    # BTN salvar a imagem
    if st.button("💾 Salvar imagem processada"):
        base_name = "imagem_salva"
        ext = ".png"
        count = 0
        output_path = os.path.join("output", f"{base_name}{ext}")


        # Adiciona um incrementador caso a imagem exista
        while os.path.exists(output_path):
            count+=1
            output_path = os.path.join("output", f"{base_name}-{count}{ext}")

        gray_image.save(output_path)
        st.success(f"✅ Imagem salva com sucesso como: `{os.path.basename(output_path)}`")