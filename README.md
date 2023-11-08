# Reconhecimento de Emoções em Tempo Real

Este projeto é um programa de reconhecimento de emoções em tempo real, que utiliza a biblioteca OpenCV para detectar rostos em uma imagem e, em seguida, classificar a emoção do rosto detectado. O programa é capaz de detectar sete emoções diferentes: raiva, nojo, medo, felicidade, tristeza, surpresa e neutro.

## Configuração do ambiente

Para executar o programa, é necessário configurar um ambiente Conda com as dependências necessárias. Siga os passos abaixo para configurar o ambiente:

1. Instale o [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou o [Anaconda](https://www.anaconda.com/products/individual) em seu sistema.

2. Abra o terminal e navegue até o diretório raiz do projeto.

3. Crie um novo ambiente Conda a partir do arquivo `environment.yml` fornecido: `conda env create -f environment.yml`

4. Ative o ambiente Conda: `conda activate emotion-recognition`

5. Execute o programa: `python app.py`

## Como usar

Ao executar o programa, uma janela será aberta mostrando a captura da sua tela. O programa detectará automaticamente os rostos na imagem e exibirá um retângulo em torno de cada rosto, juntamente com um rótulo indicando o grupo de emoção detectado (Positivo, Negativo ou Neutro).

Para sair do programa, basta fechar a janela do visualizador.

## Referências

Este aplicativo utiliza algoritmos estado-da-arte para detecção de rostos e classificação de emoções. As referências para os algoritmos utilizados estão listadas abaixo:

1. [Challenges in Representation Learning: A report on three machine learning contests](https://arxiv.org/pdf/1307.0414.pdf)
2. [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/pdf/1604.02878.pdf)

### Informações adicionais

Você pode encontrar o ranking dos melhores algoritmos de reconhecimento de emoções para o dataset FER2013 [aqui](https://paperswithcode.com/sota/facial-expression-recognition-on-fer2013)
