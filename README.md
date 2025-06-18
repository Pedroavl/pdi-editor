# Instruções do Projeto
##Video Youtube: **https://youtu.be/umBkYjVjg_Q**

## Criação de Ambiente env com o conda  
`
conda create -n sin392 python=3.12.4
conda activate sin392
pip install streamlit numpy matplotlib scikit-image opencv-python
`

### Importante rodar o comando de ativação do env
Toda vez que quiser inicializar o projeto, por exemplo:
`
conda activate sin392
`

## Como rodar o projeto web
`
streamlit run main.py
`

# Objetivo

Criar um software educacional para edição e análise de imagens, contemplando todos os principais conceitos estudados na disciplina.

## Interface Gráfica

A aplicação utiliza a biblioteca **Streamlit** com uma interface simples, intuitiva e interativa. Os botões acionam os filtros e exibem o resultado imediatamente com histograma e possibilidade de salvar a imagem.

- Bibliotecas utilizadas:

  - streamlit
  - numpy
  - matplotlib
  - opencv-python
  - pillow
  - scikit-image

## Ou você pode empacotar o e rodar sem o uso do python 

### Empacotamento (opcional)

Você pode empacotar a aplicação com PyInstaller para rodar sem precisar do Python instalado:

O executável ficará na pasta dist/pdiEditor.

# Para o empacotamento foi usado 
`pip install streamlit-desktop-app`

depois rode:

`streamlit-desktop-app build main.py --name pdiEditor`

Em todo caso é necessário instalar por preucação o streamlit

---
# TO-DO

- [x] Interface para carregar e salvar imagens (RGB e tons de cinza)
- [x] Conversão automática para tons de cinza
- [x] Histograma: Cálculo e exibição
- [x] Transformações de intensidade:
  - Alargamento de contraste
  - Equalização do histograma

- [x] Filtros passa-baixa:
  - Média
  - Mediana
  - Gaussiano
  - Máximo
  - Mínimo

- [x] Filtros passa-alta:
  - Laplaciano
  - Roberts
  - Prewitt
  - Sobel

- [x] Convolução no domínio da frequência
- [x] Espectro de Fourier
- [x] Morfologia matemática:
  - Erosão
  - Dilatação
  - Segmentação com Otsu

- [x] (Opcional) Descritores com métodos de agrupamento e tipos: cor, textura e forma

---

#### Aluno: Pedro Emanuel de Avelar Sousa de Almeida, 6965 - Sistemas de Informação UFV (Universidade Federal de Viçosa)




