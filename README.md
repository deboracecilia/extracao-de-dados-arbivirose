# 🦟 Análise Epidemiológica de Arboviroses e Variáveis Climáticas no Espírito Santo

## 📌 Sobre o Projeto

Este projeto tem como objetivo realizar a coleta, tratamento, armazenamento e análise de dados relacionados às arboviroses **Dengue, Chikungunya e Zika** no estado do Espírito Santo, integrando informações epidemiológicas com variáveis climáticas.

A solução foi desenvolvida utilizando **Python para ETL**, banco de dados **MySQL** para armazenamento estruturado e **Power BI** para criação de dashboards interativos, permitindo análises sobre distribuição dos casos, características dos pacientes e possíveis relações com fatores climáticos.

---

# 🎯 Objetivos

- Coletar dados públicos de notificações de arboviroses.
- Integrar dados de Dengue, Chikungunya e Zika.
- Obter informações climáticas dos municípios analisados.
- Realizar tratamento e padronização dos dados.
- Armazenar os dados em banco relacional MySQL.
- Criar visualizações analíticas no Power BI.
- Auxiliar na identificação de padrões epidemiológicos no Espírito Santo.

---

# 🏗️ Arquitetura do Projeto

```
APIs Públicas
      |
      |
      ↓
Python (ETL)
      |
      |
      ├── Dados SINAN
      |
      ├── Dados Climáticos Open-Meteo
      |
      ↓
Tratamento e Padronização
      |
      |
      ↓
Banco MySQL
      |
      |
      ↓
Power BI Dashboard
```

---

# 🛠️ Tecnologias Utilizadas

## Linguagens

- Python

## Bibliotecas Python

- Pandas
- Requests
- SQLAlchemy
- PyMySQL
- OpenPyXL

## Banco de Dados

- MySQL

## Ferramentas de Análise

- Power BI

---

# 🌧️ Coleta de Dados Climáticos

Os dados meteorológicos foram coletados utilizando a API pública da:

**Open-Meteo Historical Weather API**

Foram coletadas informações diárias dos municípios:

- Precipitação (mm)
- Horas de chuva
- Temperatura média
- Temperatura máxima
- Temperatura mínima

Período analisado:

```
2024 até a data atual
```

Os dados foram armazenados no arquivo:

```
clima_espirito_santo_2024_2026.csv
```

---

# 🦟 Coleta de Dados Epidemiológicos

Os dados de notificações foram obtidos através do:

**SINAN - Sistema de Informação de Agravos de Notificação**

Agravos analisados:

- Dengue
- Chikungunya
- Zika Vírus

Período:

```
2024, 2025 e 2026
```

Filtros aplicados:

- Estado: Espírito Santo
- Municípios selecionados
- Variáveis epidemiológicas relevantes

---

# 🧹 Tratamento dos Dados

Durante o processo ETL foram realizadas:

✔ Conversão e padronização de datas  
✔ Tratamento de valores inválidos  
✔ Seleção das colunas necessárias  
✔ Ajuste dos tipos de dados  
✔ Remoção de inconsistências  
✔ Organização das tabelas dimensionais  

---

# 🗄️ Banco de Dados

Os dados foram armazenados em MySQL.

Banco utilizado:

```
doencas_arbivirose_2026_2024
```

Principais tabelas:

### Fato

```
dengue_2022_2026
```

Contém:

- Data da notificação
- Município
- Sexo
- Ano de nascimento
- Agravo
- Região
- Raça
- Escolaridade


### Tabelas auxiliares

```
tb_cs_escol_n
tb_id_municip
tb_id_agravo
tb_id_regiona
tb_cs_raca
```

Essas tabelas permitem melhorar os relacionamentos e análises no Power BI.

---

# 📊 Dashboard Power BI

O dashboard foi desenvolvido para análise dos casos epidemiológicos e sua relação com variáveis climáticas.

Acesse a visualização:

🔗 https://app.powerbi.com/view?r=eyJrIjoiZjgzZDk4Y2UtNTgzZi00MjczLThmYTItOWY2ZGVmMmVhMTQ5IiwidCI6ImZlODc4N2JjLWM5MTQtNDY2NS04NTQ3LTI2OGUxNWNiMGQ5YSJ9&pageName=447200ad7cc8e0b3c96e

---

# 📈 Análises Disponíveis

O dashboard apresenta informações como:

## Visão Geral

- Total de notificações
- Distribuição dos casos
- Evolução temporal

## Análise Epidemiológica

- Casos por município
- Comparação entre doenças
- Perfil dos pacientes

## Dados Climáticos

- Volume de chuva
- Temperatura média
- Relação entre clima e notificações

## Distribuição Geográfica

- Municípios com maior concentração de casos
- Análise espacial dos registros

---

# 👩‍💻 

Projeto desenvolvido para análise de dados públicos utilizando técnicas de:

- Engenharia de Dados
- ETL
- Banco de Dados
- Business Intelligence
- Visualização de Dados

---