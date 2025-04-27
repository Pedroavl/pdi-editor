# Instruções do Projeto
## Criação de Ambiente env com o conda 
`
conda create -n sin392 python=3.10
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

- [ ] Convolução no domínio da frequência
- [ ] Espectro de Fourier
- [ ] Morfologia matemática:
  - Erosão
  - Dilatação
  - Segmentação com Otsu

- [ ] (Opcional) Descritores com métodos de agrupamento e tipos: cor, textura e forma




