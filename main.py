import requests
import json

USER = "imunizacao_public"
PASSWORD = "qlto5t&7r_@+#Tlstigi"

URL = 'https://imunizacao-es.saude.gov.br/_search'

payload = {"size": 1000}

resultadoJson = {}
municipios = {}


def requisicao_api():
    reposta = requests.get(URL, auth=(USER, PASSWORD), params=payload)
    dados = json.loads(reposta.content)
    return dados


def totalDosesAplicadas(requisicao):
    totalDoses = requisicao
    contador = 0
    for i in totalDoses:
        contador += 1
    return contador


def dosesPorFabricante(requisicao):
    dadosAPI = requisicao

    doses_janssen = 0
    doses_pfizer = 0
    doses_astrazeneca = 0
    doses_sinovac = 0

    for i in dadosAPI:
        fabricante_nome = i['_source']['vacina_fabricante_nome']

        if fabricante_nome == 'JANSSEN':
            doses_janssen += 1
        elif fabricante_nome == 'PFIZER' or fabricante_nome == 'PFIZER - PEDIÁTRICA':
            doses_pfizer += 1
        elif fabricante_nome == 'ASTRAZENECA/FIOCRUZ' or fabricante_nome == 'ASTRAZENECA':
            doses_astrazeneca += 1
        elif fabricante_nome == 'SINOVAC/BUTANTAN' or fabricante_nome == 'SINOVAC':
            doses_sinovac += 1 
        

    return [doses_janssen, doses_pfizer ,doses_astrazeneca, doses_sinovac]


def totalPorMunicipio(requisicao):
    dadosAPI = requisicao

    for i in dadosAPI:

        janssen_municipio = 0
        pfizer_municipio = 0
        astrazeneca_municipio = 0
        sinovac_municipio = 0

        nmMunicipio = i['_source']['paciente_endereco_nmMunicipio']
        nmVacina = i['_source']['vacina_fabricante_nome']
        nmUf = i['_source']['paciente_endereco_uf']

        if nmMunicipio in municipios:
            if municipios[nmMunicipio][1] != 0:
                janssen_municipio = municipios[nmMunicipio][1]
            if municipios[nmMunicipio][2] != 0:
                pfizer_municipio = municipios[nmMunicipio][2]
            if municipios[nmMunicipio][3] != 0:
                astrazeneca_municipio = municipios[nmMunicipio][3]
            if municipios[nmMunicipio][4] != 0:
                sinovac_municipio = municipios[nmMunicipio][4]

        if nmVacina == 'JANSSEN':
            janssen_municipio += 1
        elif nmVacina == 'PFIZER' or nmVacina == 'PFIZER - PEDIÁTRICA':
            pfizer_municipio += 1
        elif nmVacina == 'ASTRAZENECA/FIOCRUZ' or nmVacina == 'ASTRAZENECA':
            astrazeneca_municipio += 1
        elif nmVacina == 'SINOVAC/BUTANTAN' or nmVacina == 'SINOVAC':
            sinovac_municipio += 1

        municipios[nmMunicipio] = [nmUf, janssen_municipio, pfizer_municipio, astrazeneca_municipio, sinovac_municipio]

    return municipios


def criaJSON():
    cidades_janssen = []
    cidades_pfizer = []
    cidades_astrazeneca = []
    cidades_sinovac = []

    requisicao = requisicao_api()['hits']['hits']

    totalDoses = totalDosesAplicadas(requisicao)
    dicionarioMunicipio = totalPorMunicipio(requisicao)
    dosesFabricante = dosesPorFabricante(requisicao)

    for i in dicionarioMunicipio:
        cidades_janssen.append({"municipio": i, "uf": dicionarioMunicipio[i][0], "total": dicionarioMunicipio[i][1]})
        cidades_pfizer.append({"municipio": i, "uf": dicionarioMunicipio[i][0], "total": dicionarioMunicipio[i][2]})
        cidades_astrazeneca.append({"municipio": i, "uf": dicionarioMunicipio[i][0], "total": dicionarioMunicipio[i][3]})
        cidades_sinovac.append({"municipio": i, "uf": dicionarioMunicipio[i][0], "total": dicionarioMunicipio[i][4]})


    resultadoJson["total_doses_aplicadas"] = totalDoses
    resultadoJson["JANSSEN"] = {
        "total_doses": dosesFabricante[0],
        "total_por_municipio": cidades_janssen
    }
    resultadoJson["PFIZER"] = {
        "total_doses": dosesFabricante[1],
        "total_por_municipio": cidades_pfizer
    }
    resultadoJson["ASTRAZENECA"] = {
        "total_doses": dosesFabricante[2],
        "total_por_municipio": cidades_astrazeneca
    }
    resultadoJson["SINOVAC"] = {
        "total_doses": dosesFabricante[3],
        "total_por_municipio": cidades_sinovac
    }

    return json.dumps(resultadoJson)


if __name__ == '__main__':
    print(criaJSON())
