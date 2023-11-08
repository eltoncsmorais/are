import argparse
import pandas as pd
import plotly.express as px
from jinja2 import Template

class Graficos:
    @staticmethod
    def gerar(log_path):
        
        data = pd.read_csv(f"{log_path}/log.csv", header=0)

        data["timestamp"] = pd.to_datetime(data["timestamp"])

        pd.options.plotting.backend = "plotly"

        data_emocao = (
            data.groupby(["timestamp", "emocao"]).size().reset_index(name="frequency")
        )
        data_grupo = (
            data.groupby(["timestamp", "grupo"]).size().reset_index(name="frequency")
        )

        fig1 = px.line(
            data_emocao,
            x="timestamp",
            y="frequency",
            color="emocao",
            title="Frequência de Emoções ao Longo do Tempo",
            facet_col="emocao",
            facet_col_wrap=1,
        )

        fig2 = px.line(
            data_grupo,
            x="timestamp",
            y="frequency",
            color="grupo",
            title="Frequência de Grupos de Emoções ao Longo do Tempo",
            facet_col="grupo",
            facet_col_wrap=1,
        )

        fig3 = (
            data["emocao"]
            .value_counts()
            .plot.bar(
                title="Frequência de Emoções",
            )
        )

        fig4 = (
            data["grupo"]
            .value_counts()
            .plot.bar(
                title="Frequência de Grupos de Emoções",
            )
        )

        """fig5 = px.scatter(
            data_emocao,
            x="timestamp",
            y="frequency",
            color="emocao",
            trendline="lowess",
            title="Tendência de Emoções ao Longo do Tempo",
        )

        fig6 = px.scatter(
            data_grupo,
            x="timestamp",
            y="frequency",
            color="grupo",
            trendline="lowess",
            title="Tendência de Grupos de Emoções ao Longo do Tempo",
        )"""

        emocao_mais_comum = data["emocao"].mode()[0]
        grupo_mais_comum = data["grupo"].mode()[0]
        mean_emocao = data_emocao["frequency"].mean().round(3)
        mean_grupo = data_grupo["frequency"].mean().round(3)
        mad_emocao = (data_emocao["frequency"] - mean_emocao).abs().mean().round(3)
        mad_grupo = (data_grupo["frequency"] - mean_grupo).abs().mean().round(3)
        std_emocao = data_emocao["frequency"].std().round(3)
        std_grupo = data_grupo["frequency"].std().round(3)

        percentis_emocao = (
            data["emocao"].value_counts(normalize=True).mul(100).round(1).astype(str)
            + "%"
        )

        percentis_grupo = (
            data["grupo"].value_counts(normalize=True).mul(100).round(1).astype(str)
            + "%"
        )

        total = len(data)
        total_emocao = data["emocao"].value_counts()
        total_grupo = data["grupo"].value_counts()

        with open("templates/relatorio.j2", "r", encoding="utf-8") as template:
            template = Template(template.read())

        with open(f"{log_path}/output.html", "w", encoding="utf-8") as relatorio:
            relatorio.write(
                template.render(
                    emocao_mais_comum=emocao_mais_comum,
                    grupo_mais_comum=grupo_mais_comum,
                    std_emocao=std_emocao,
                    std_grupo=std_grupo,
                    mean_emocao=mean_emocao,
                    mean_grupo=mean_grupo,
                    mad_emocao=mad_emocao,
                    mad_grupo=mad_grupo,
                    total=total,
                    percentis_emocao=percentis_emocao,
                    percentis_grupo=percentis_grupo,
                    total_emocao=total_emocao,
                    total_grupo=total_grupo,
                    fig1=fig1.to_html(full_html=False),
                    fig2=fig2.to_html(full_html=False, include_plotlyjs=False),
                    fig3=fig3.to_html(full_html=False, include_plotlyjs=False),
                    fig4=fig4.to_html(full_html=False, include_plotlyjs=False),
                    #fig5=fig5.to_html(full_html=False, include_plotlyjs=False),
                    #fig6=fig6.to_html(full_html=False, include_plotlyjs=False),
                )
            )

"""if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_path", help="Caminho para o arquivo de log", type=str)
    args = parser.parse_args()
    path = args.log_path
    Graficos.gerar(path)"""
