import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow import keras
from toolz import pluck
from toolz.functoolz import compose, pipe

from src.ResidualMaskingNetwork import RMN


class Imagem:
    """Classe para manipulação de imagens

    Attrs:
        mtcnn (MTCNN): O detector de faces MTCNN
        rmn (RMN): O classificador de emoções RMN
        rotulos (dict): O dicionário de rótulos de emoções
    """

    mtcnn = MTCNN()
    rmn = RMN()

    rotulos = {
        0: "Raiva",
        1: "Nojo",
        2: "Medo",
        3: "Feliz",
        4: "Triste",
        5: "Surpreso",
        6: "Neutro",
    }

    def detecta_faces(self, imagem):
        """Detecta faces em uma imagem

        Args:
            imagem (Mat): A imagem a ser processada

        Returns:
            np.ndarray: Array de faces detectadas
        """

        def __converter_coordenadas(bounding_boxes):
            """Converte as coordenadas das caixas delimitadoras para um array numpy de inteiros"""

            def convert_box(box):
                return tuple(map(int, box))

            return np.array(list(map(compose(convert_box), bounding_boxes)))

        return pipe(
            imagem,
            lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
            lambda img: self.mtcnn.detect_faces(img),
            lambda deteccoes: pluck("box", deteccoes),
            lambda deteccoes: list(deteccoes),
            lambda bounding_boxes: __converter_coordenadas(bounding_boxes)
            if bounding_boxes is not None
            else [],
        )

    def regiao_interesse(self, imagem, x, y, w, h):
        """
        Extrai a região de interesse (ROI) da imagem fornecida com base nas coordenadas fornecidas.

        Args:
            image (numpy.ndarray): A imagem de entrada.
            x (int): A coordenada x inicial da ROI.
            y (int): A coordenada y inicial da ROI.
            w (int): A largura da ROI.
            h (int): A altura da ROI.

        Returns:
            numpy.ndarray: O ROI extraído.
        """

        return imagem[y : y + h, x : x + w]

    def redimensiona(self, imagem, tamanho):
        """
        Redimensiona a imagem fornecida para o tamanho especificado.

        Args:
            image (numpy.ndarray): A imagem de entrada.
            tamanho (tuple): O tamanho desejado no formato (largura, altura).

        Returns:
            numpy.ndarray: A imagem redimensionada.
        """

        return cv2.resize(imagem, tamanho, interpolation=cv2.INTER_AREA)

    def normaliza(self, imagem):
        """
        Normaliza os valores de pixel da imagem fornecida.

        Args:
            image (numpy.ndarray): A imagem de entrada.

        Returns:
            numpy.ndarray: A imagem normalizada.
        """

        imagem_normalizada = pipe(
            imagem,
            lambda _: imagem.astype("float") / 255,
            lambda img: keras.utils.img_to_array(img),
            lambda img: np.expand_dims(img, axis=0),
        )

        return imagem_normalizada

    def predizer_emocoes(self, roi):
        """
        Prevê as emoções do ROI fornecido usando o classificador fornecido.

        Args:
            roi (numpy.ndarray): O ROI de entrada.

        Returns:
            str: Rótulo da emoção predita.
        """

        def rotula_emocoes(emocao):
            """Cria um dicionário com os rótulos de emoções e suas respectivas pontuações"""

            return {
                self.rotulos[indice]: round(float(score), 2)
                for indice, score in enumerate(emocao)
            }

        predicoes = self.rmn.classificar(roi)
        emocoes_rotuladas = list(map(compose(rotula_emocoes), predicoes))[0]

        return max(emocoes_rotuladas, key=emocoes_rotuladas.get)
