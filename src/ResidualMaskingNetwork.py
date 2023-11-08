from tensorflow.keras.models import load_model


class RMN:
    """Uma classe usada para representar uma Rede Neural Recorrente (RMN) para classificação de emoções.

    Attrs:
        modelo(str): O caminho para o arquivo de modelo salvo.
        tamanho_alvo_modelo(tuple): O tamanho alvo para a entrada do modelo.
    """

    modelo = "data/emotion_model.hdf5"
    tamanho_alvo_modelo = None

    def __init__(self):
        """Inicializa o objeto RMN carregando o modelo salvo e definindo o tamanho alvo.

        O modelo salvo é carregado usando a função `load_model` de `tensorflow.keras.models`.
        O tamanho alvo é definido como a forma de entrada do modelo carregado ou o tamanho alvo fornecido.
        """

        self.classificar = load_model(self.modelo, compile=False)
        self.classificar.make_predict_function()
        self.tamanho_alvo_modelo = (
            self.classificar.input_shape[1:3]
            if not self.tamanho_alvo_modelo
            else self.tamanho_alvo_modelo
        )
