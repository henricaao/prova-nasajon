import csv
import requests

# estatísticas
total_municipios = 0
total_ok = 0
total_nao = 0
total_erro = 0
pop_total_ok = 0

regioes = {}

# ler input.csv
dados = []

with open("input.csv", newline='', encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        dados.append(linha)

# buscar municipios IBGE
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
resposta = requests.get(url)

municipios_ibge = resposta.json()

# criar resultado.csv
with open("resultado.csv", "w", newline="", encoding="utf-8") as saida:

    campos = [
        "municipio_input",
        "populacao_input",
        "municipio_ibge",
        "uf",
        "regiao",
        "id_ibge",
        "status"
    ]

    writer = csv.DictWriter(saida, fieldnames=campos)
    writer.writeheader()

    for item in dados:

        total_municipios += 1

        municipio_input = item["municipio"]
        populacao = int(item["populacao"])

        encontrado = False

        for m in municipios_ibge:

            if municipio_input.lower() in m["nome"].lower():

                regiao = m["microrregiao"]["mesorregiao"]["UF"]["regiao"]["nome"]

                linha = {
                    "municipio_input": municipio_input,
                    "populacao_input": populacao,
                    "municipio_ibge": m["nome"],
                    "uf": m["microrregiao"]["mesorregiao"]["UF"]["sigla"],
                    "regiao": regiao,
                    "id_ibge": m["id"],
                    "status": "OK"
                }

                writer.writerow(linha)

                total_ok += 1
                pop_total_ok += populacao

                if regiao not in regioes:
                    regioes[regiao] = []

                regioes[regiao].append(populacao)

                encontrado = True
                break

        if not encontrado:

            linha = {
                "municipio_input": municipio_input,
                "populacao_input": populacao,
                "municipio_ibge": "",
                "uf": "",
                "regiao": "",
                "id_ibge": "",
                "status": "NAO_ENCONTRADO"
            }

            writer.writerow(linha)

            total_nao += 1

# calcular médias por região
medias = {}

for regiao in regioes:

    lista = regioes[regiao]
    media = sum(lista) / len(lista)

    medias[regiao] = media

print("Estatísticas:")

print("total_municipios:", total_municipios)
print("total_ok:", total_ok)
print("total_nao_encontrado:", total_nao)
print("pop_total_ok:", pop_total_ok)

print("medias_por_regiao:", medias)

import requests
import json

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImR0TG03UVh1SkZPVDJwZEciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL215bnhsdWJ5a3lsbmNpbnR0Z2d1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIwYjY5NGQ4Ny1kNGE4LTRjMDQtOWRkZS02ZDNhNjhkY2ViYjEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzczMzUwMDA2LCJpYXQiOjE3NzMzNDY0MDYsImVtYWlsIjoiaGVucmlxdWVhbmRlcjZAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJlbWFpbCI6ImhlbnJpcXVlYW5kZXI2QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJub21lIjoiSGVucmlxdWUgR29tZXMiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInN1YiI6IjBiNjk0ZDg3LWQ0YTgtNGMwNC05ZGRlLTZkM2E2OGRjZWJiMSJ9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzczMzQ2NDA2fV0sInNlc3Npb25faWQiOiJmMWZmZTMxMC1lYzhkLTQxNzYtOWEyOC02NmZiMTA2YzZlM2MiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.BV2uNz2C_yA0-m4dH1LNOa1HMmvEmCd9Fmcr6mD_nlU"

url = "https://mynxlubykylncinttggu.functions.supabase.co/ibge-submit"

medias_por_regiao = {"Sudeste": pop_total_ok}

payload = {
    "stats": {
        "total_municipios": total_municipios,
        "total_ok": total_ok,
        "total_nao_encontrado": total_municipios - total_ok,
        "total_erro_api": 0,
        "pop_total_ok": pop_total_ok,
        "medias_por_regiao": medias_por_regiao
    }
}

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

print(response.json())