import cv2
import numpy as np
import pyautogui
from cytoolz import filter


def captura_tela():
    """Captura a tela e retorna um array numpy"""

    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)


def busca_emocao(emocao):
    """Busca a emoção em um dicionário de emoções

    Args:
        emocao (str): A emoção a ser buscada

    Returns:
        str | None: A chave da emoção encontrada ou None
    """

    emocoes = {
        "Positivo": ["Feliz", "Surpreso"],
        "Negativo": ["Raiva", "Nojo", "Medo", "Triste"],
        "Neutro": ["Neutro"],
    }

    return next(filter(lambda key: emocao in emocoes[key], emocoes), None)


def busca_cor(rotulo):
    return {
        "Positivo": (0, 255, 0),
        "Negativo": (0, 0, 255),
        "Neutro": (255, 0, 0),
    }.get(rotulo, (255, 0, 0))
