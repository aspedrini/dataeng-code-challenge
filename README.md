<h1 align="center"> Indicium Code Challenge - Data Engineer </h1>

# Desafio
O desafio está localizado em https://github.com/techindicium/code-challenge/tree/main

# Como executar
Para dar início ao processo, é necessário ter o Docker e Python instalados. Opcional: uma ferramenta para acessar os bancos de dados, como o Dbeaver.

1 - Numa pasta vazia à sua escolha, abra um terminal Git e clone este repositório:
```git clone (link aqui)```

Dentro desta pasta clonada devem estar os seguintes itens:
```
Pastas:
∟ data
  ∟ csv
    ∟ order_details.csv
  ∟ postgres
∟ docker
  ∟ docker-compose.yaml
∟ extract
  ∟ final_query.sql

Arquivos:
∟ requirements.txt
∟ csv_extract.py
∟ sql_extract.py
∟ upload_mysql.py
```
A pasta "postgres" dentro de "data" é uma pasta vazia. Caso ela não seja carregada, crie-a por favor.

2 - Crie a pasta do Virtual Environment (venv) digitando no terminal da IDE:
```
python -m venv .venv
```
e ative-o:
```
.venv/scripts/activate
```

3 - No seu software de IDE, abra a pasta clonada de forma a ter essa visualização:

![image](https://github.com/aspedrini/dataeng-code-challenge/assets/103280317/bdb65d29-a4a2-4ff0-9d9c-4325e47e75b0)


4 - No terminal do IDE, ative o virtual environment através do comando:
```
.venv/scripts/activate
```

5 - Instale as bibliotecas de requisitos digitando em seu terminal:
```
pip install -r requirements.txt
```

6 - Execute o docker-compose.yaml:
```
cd docker
docker-compose up -d
```

Com o Virtual Environment ativado, requeriments.txt instalado e o docker-compose up, é possivel prosseguir à execução da pipeline.

# Execução
Os dois scripts de sufixo "_extract.py" devem rodar, independente da ordem, antes da task final "upload_mysql.py".

![image](https://github.com/aspedrini/dataeng-code-challenge/assets/103280317/5006cd23-2f87-41b7-af2c-d4f587202415)

O script "sql_extract.py" realiza as extrações das tabelas do PostgreSQL fornecido no arquivo original do docker-compose.yml pela Indicium, e já vem populado com os dados do banco Northwind com exceção da order_details.
O "csv_extract.py" extrai os dados do csv "order_details.csv" localizado dentro de "data", sendo seus dados estáticos.
Todos os scripts pedem um input do usuário para a data alvo da extraçao. É possível escolher a opção "1" para o dia de hoje e "2" para digitar outra data (YYYY-MM-DD). Antes do upload, o último script faz uma verificação no nome das pastas dentro de data/csv e data/postgres para checar se a data escolhida existe em ambas, e apenas em caso positivo é realizado o upload.

Diagrama final:
![image](https://github.com/aspedrini/dataeng-code-challenge/assets/103280317/ad9371ae-143e-4031-9837-31571acf546c)


# Acessando o MySQL
Através da ferramenta para acessar bancos de dados, adicione o banco do MySQL que foi inicializado através do Docker. Suas informações de login estão no arquio docker-compose.yml.
Na pasta "extract" está disponibilizada um script em .sql para realizar a query final:

![image](https://github.com/aspedrini/dataeng-code-challenge/assets/103280317/abcd5e54-9f48-4547-b6dd-b14f36d81b0b)


# Considerações finais
Para realização do projeto, aproveitei para subir no docker-compose.yml o banco do MySQL, por alguns motivos: o primeiro é relativo à complexidade da tarefa, e creio que não seria de bom grado utilizar o mesmo banco de dados disponibilizado para o consumo na primeira etapa; o segundo motivo é por estar aprendendo Docker junto com Airflow, para me habituar melhor com a estrutura de seu arquivo.
Infelizmente faltou tempo para instanciar o Airflow neste projeto, tive um pouco de dificuldade para fazê-lo reconhecer meu sistema local de arquivos, e preferi seguir o desafio sem ele.

Por fim, agradeço à Indicium pela oportunidade de realizar este desafio.
