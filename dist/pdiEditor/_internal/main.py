import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

from PIL import Image

from skimage import exposure
from skimage.filters import gaussian, median, roberts, prewitt, threshold_otsu
from skimage.morphology import disk
from skimage.feature import graycomatrix, graycoprops
import numpy.fft as fft

# Função para salvar imagem processada com nome incremental
def salvar_imagem_processada(imagem_np, nome_base="imagem_processada"):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    ext = ".png"
    count = 0
    output_path = os.path.join(output_dir, f"{nome_base}{ext}")

    while os.path.exists(output_path):
        count += 1
        output_path = os.path.join(output_dir, f"{nome_base}-{count}{ext}")

    imagem_pil = Image.fromarray(imagem_np)
    imagem_pil.save(output_path)
    st.success(f"✅ Imagem salva como: `{os.path.basename(output_path)}`")

# Configurações da interface
st.set_page_config(page_title="SIN 392 - Projeto final PDI", layout="centered")
st.title("Editor de Imagens - SIN 392")

os.makedirs("output", exist_ok=True)

uploaded_file = st.file_uploader("Selecione uma imagem", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Imagem Recebida")
    st.image(image, use_container_width=True)

    if image.mode == "RGB":
        gray_image = image.convert("L")
        st.subheader("Convertida para Tons de Cinza")
        st.image(gray_image, use_container_width=True)
    else:
        gray_image = image

    img_array = np.array(gray_image)

    # Histograma
    st.subheader("Histograma da Imagem")
    hist, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    fig, ax = plt.subplots()
    ax.plot(hist, color='black')
    ax.set_title("Histograma")
    st.pyplot(fig)

    # Transformacoes
    st.subheader("Transformações de Intensidade")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Alargamento de Contraste**")
        if st.button("Aplicar Alargamento"):
            img_stretch = exposure.rescale_intensity(img_array, in_range='image', out_range=(0, 255)).astype(np.uint8)
            st.session_state['imagem_processada'] = img_stretch
            st.session_state['ultima_operacao'] = "Alargamento de Contraste"
            st.image(img_stretch, caption="Imagem com Alargamento de Contraste", use_container_width=True)

    with col2:
        st.markdown("**Equalização de Histograma**")
        if st.button("Aplicar Equalização"):
            img_eq = exposure.equalize_hist(img_array)
            img_eq = (img_eq * 255).astype(np.uint8)
            st.session_state['imagem_processada'] = img_eq
            st.session_state['ultima_operacao'] = "Equalização de Histograma"
            st.image(img_eq, caption="Imagem com Equalização de Histograma", use_container_width=True)

    # Filtros Passa-Baixa
    st.subheader("Filtros Passa-Baixa")
    filtro = st.selectbox("Filtro Passa-Baixa:", ("Média", "Mediana", "Gaussiano", "Máximo", "Mínimo"))
    if st.button("Aplicar Filtro Passa-Baixa"):
        if filtro == "Média":
            img_filtered = cv2.blur(img_array, (5, 5))
        elif filtro == "Mediana":
            img_filtered = median(img_array, disk(3))
        elif filtro == "Gaussiano":
            img_filtered = gaussian(img_array, sigma=1)
            img_filtered = (img_filtered * 255).astype(np.uint8)
        elif filtro == "Máximo":
            img_filtered = cv2.dilate(img_array, np.ones((3, 3), np.uint8))
        elif filtro == "Mínimo":
            img_filtered = cv2.erode(img_array, np.ones((3, 3), np.uint8))

        st.session_state['imagem_processada'] = img_filtered
        st.session_state['ultima_operacao'] = f"Filtro Passa-Baixa {filtro}"
        st.image(img_filtered, caption=f"Filtro {filtro}", use_container_width=True)

    # Filtros Passa-Alta
    st.subheader("Filtros Passa-Alta")
    filtro_alta = st.selectbox("Filtro Passa-Alta:", ("Laplaciano", "Roberts", "Prewitt", "Sobel"))
    if st.button("Aplicar Filtro Passa-Alta"):
        if filtro_alta == "Laplaciano":
            img_filtered = cv2.Laplacian(img_array, ddepth=cv2.CV_64F)
            img_filtered = cv2.convertScaleAbs(img_filtered)
        elif filtro_alta == "Roberts":
            img_filtered = roberts(img_array)
            img_filtered = (img_filtered * 255).astype(np.uint8)
        elif filtro_alta == "Prewitt":
            img_filtered = prewitt(img_array)
            img_filtered = (img_filtered * 255).astype(np.uint8)
        elif filtro_alta == "Sobel":
            img_filtered = cv2.Sobel(img_array, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
            img_filtered = cv2.convertScaleAbs(img_filtered)

        st.session_state['imagem_processada'] = img_filtered
        st.session_state['ultima_operacao'] = f"Filtro Passa-Alta {filtro_alta}"
        st.image(img_filtered, caption=f"Filtro {filtro_alta}", use_container_width=True)

    # Filtros no Domínio da Frequência
    st.subheader("Domínio da Frequência")
    tipo_filtro_freq = st.selectbox("Filtro no Domínio da Frequência:", ("Passa-Baixa Ideal", "Passa-Alta Ideal"))
    if st.button("Aplicar Filtro no Domínio da Frequência"):
        f = fft.fft2(img_array)
        fshift = fft.fftshift(f)
        rows, cols = img_array.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        raio = 30

        for i in range(rows):
            for j in range(cols):
                dist = np.sqrt((i - crow)**2 + (j - ccol)**2)
                if tipo_filtro_freq == "Passa-Baixa Ideal" and dist <= raio:
                    mask[i, j] = 1
                elif tipo_filtro_freq == "Passa-Alta Ideal" and dist > raio:
                    mask[i, j] = 1

        fshift_filtered = fshift * mask
        img_back = fft.ifft2(fft.ifftshift(fshift_filtered))
        img_back = np.abs(img_back)
        img_back = np.clip(img_back, 0, 255).astype(np.uint8)
        st.session_state['imagem_processada'] = img_back
        st.session_state['ultima_operacao'] = f"Filtro Frequência {tipo_filtro_freq}"
        st.image(img_back, caption=f"Filtro {tipo_filtro_freq}", use_container_width=True)

    # Espectro de Fourier
    st.subheader("Espectro de Fourier")
    if st.button("Exibir Espectro de Fourier"):
        f = fft.fft2(img_array)
        fshift = fft.fftshift(f)
        magnitude = 20 * np.log(np.abs(fshift) + 1)
        fig_fft, ax_fft = plt.subplots()
        ax_fft.imshow(magnitude, cmap='gray')
        ax_fft.set_title("Espectro de Magnitude (log)")
        ax_fft.axis("off")
        st.pyplot(fig_fft)

    # Morfologia
    st.subheader("Morfologia Matemática")
    op_morf = st.selectbox("Operação Morfológica:", ("Erosão", "Dilatação"))
    if st.button("Aplicar Morfologia"):
        kernel = np.ones((3, 3), np.uint8)
        if op_morf == "Erosão":
            morf_img = cv2.erode(img_array, kernel, iterations=1)
        else:
            morf_img = cv2.dilate(img_array, kernel, iterations=1)
        st.session_state['imagem_processada'] = morf_img
        st.session_state['ultima_operacao'] = f"Morfologia {op_morf}"
        st.image(morf_img, caption=f"Imagem após {op_morf}", use_container_width=True)

    # Segmentação Otsu
    st.subheader("Segmentação - Otsu")
    if st.button("Aplicar Otsu"):
        limiar = threshold_otsu(img_array)
        img_seg = (img_array > limiar).astype(np.uint8) * 255
        st.session_state['imagem_processada'] = img_seg
        st.session_state['ultima_operacao'] = "Segmentação Otsu"
        st.image(img_seg, caption=f"Segmentada (limiar = {limiar:.2f})", use_container_width=True)

    # Descritores
    st.subheader("Descritores de Cor, Textura e Forma")
    if st.button("Extrair Descritores"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Cor (Histograma RGB)**")
            if image.mode == "RGB":
                r, g, b = image.split()
                fig_c, ax_c = plt.subplots()
                ax_c.hist(np.array(r).flatten(), bins=256, color='red', alpha=0.5, label='R')
                ax_c.hist(np.array(g).flatten(), bins=256, color='green', alpha=0.5, label='G')
                ax_c.hist(np.array(b).flatten(), bins=256, color='blue', alpha=0.5, label='B')
                ax_c.legend()
                st.pyplot(fig_c)
            else:
                st.info("Imagem não RGB para extração de descritor de cor.")

        with col2:
            st.markdown("**Textura (GLCM)**")
            img_glcm = (img_array / 4).astype(np.uint8)
            glcm = graycomatrix(img_glcm, [1], [0], 256, symmetric=True, normed=True)
            contraste = graycoprops(glcm, 'contrast')[0, 0]
            energia = graycoprops(glcm, 'energy')[0, 0]
            homogeneidade = graycoprops(glcm, 'homogeneity')[0, 0]
            st.write(f"Contraste: {contraste:.4f}")
            st.write(f"Energia: {energia:.4f}")
            st.write(f"Homogeneidade: {homogeneidade:.4f}")

        with col3:
            st.markdown("**Forma (Momentos de Hu)**")
            edges = cv2.Canny(img_array, 100, 200)
            hu = cv2.HuMoments(cv2.moments(edges)).flatten()
            st.image(edges, caption="Contornos detectados", use_container_width=True)
            for i, val in enumerate(hu):
                st.write(f"Hu[{i+1}]: {val:.4e}")

    # Botão salvar imagem processada global
    if 'imagem_processada' in st.session_state:
        legenda = st.session_state.get('ultima_operacao', "imagem processada")
        if st.button(f"Salvar {legenda}"):
            salvar_imagem_processada(st.session_state['imagem_processada'], legenda.replace(" ", "_").lower())
