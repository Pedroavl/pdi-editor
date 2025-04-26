import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

from PIL import Image
from skimage import exposure


# Configurações da interface
st.set_page_config(page_title="Editor de Imagens - Processamento Digital de Imagens", layout="centered")
st.title("Carregamento e Salvamento de Imagens")

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

    # Mostra o histograma da imagem em tons de cinza
    if gray_image:
        st.subheader("Histograma da Imagem")

        # Converte a imagem para array NumPy
        img_array = np.array(gray_image)

        # print(img_array)

        # Calculo do histograma
        hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])

        fig, ax = plt.subplots()
        ax.plot(hist, color='black')
        ax.set_title("Histograma")
        ax.set_xlabel("Níveis de intensidade")
        ax.set_ylabel("Número de pixels")
        st.pyplot(fig)

    st.subheader("Transformações de Intensidade")

    col1, col2 = st.columns(2)

    # Alargamento de contraste
    with col1:
        st.markdown("**Alargamento de Contraste**")
        if st.button("Aplicar Alargamento"):
            img_stretch = exposure.rescale_intensity(img_array, in_range='image', out_range=(0, 255)).astype(np.uint8)
            st.image(img_stretch, caption="Imagem com Alargamento de Contraste", use_container_width=True)

            # Histograma após alargamento
            hist_stretch, _ = np.histogram(img_stretch.flatten(), bins=256, range=[0, 256])
            fig1, ax1 = plt.subplots()
            ax1.plot(hist_stretch, color='green')
            ax1.set_title("Histograma - Alargamento de Contraste")
            st.pyplot(fig1)

    # Equalização de histograma
    with col2:
        st.markdown("**Equalização de Histograma**")
        if st.button("Aplicar Equalização"):
            img_eq = exposure.equalize_hist(img_array)
            img_eq = (img_eq * 255).astype(np.uint8)
            st.image(img_eq, caption="Imagem com Equalização de Histograma", use_container_width=True)

            # Histograma equalizado
            hist_eq, _ = np.histogram(img_eq.flatten(), bins=256, range=[0, 256])
            fig2, ax2 = plt.subplots()
            ax2.plot(hist_eq, color='blue')
            ax2.set_title("Histograma - Equalização")
            st.pyplot(fig2)

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