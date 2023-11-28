# Coletor de Dados de E-mails do Gmane
Programa que coleta dados de e-mails do Gmane (na realidade coleta do [servidor de dr-chuck](https://mbox.dr-chuck.net) para que não sobrecarregue o Gmane), salva-os em um banco de dados e criar uma variedade de modelos de visualização de dados.

### Funcionalidade

O programa é subdividido em três subprocessos principais: Spider (Aranha), Model (Modelo) e Data Visualization (Visualização de Dados).

1. O `Spider` coleta dados de e-mails do [servidor de dr-chuck](https://mbox.dr-chuck.net) e os salva em um banco de dados bruto chamado ***"spider.sqlite"***, os dados são:
    - Sender e-mail (E-mail do remetente);
    - Date (Data);
    - Subject (Assunto);
    - E-mail header (Cabeçalho do e-mail);
    - E-mail body (Corpo do e-mail).

2. O `Model` toma os dados do banco de dados bruto e cria um novo e aprimorado banco de dados relacional chamado ***"model_db.sqlite"***. O modelo de dados pode ser visto em ***email_datamodel.png***.

3. O `Data Visualization` criar arquivos javascript (.js) para serem usados como dado para os arquivos htm renderizarem em modelos de visualização em um browser de internet usando a biblioteca ***"D3 JavaScript"***. Os modelos são:
    - **Basic (Básico)**: mostra os 'n' maiores remetentes e organizações no próprio shell (onde 'n' é o número escolhido);
    - **Word (Palavra)**: pega as 'n' palavras, maiores de 3 caracteres, que mais aparecem na coluna de assuntos e as mostra em diversos tamanhos a depender de sua frequência;
    - **Line (Linha)**: um gráfico de linha que mostra quantas vezes as 'n' maiores organizações e remetentes aparecem por mês ao longo dos anos;
    - **Year (Ano)**: um gráfico de linha que mostra quantas vezes as 'n' maiores organizações e remetentes aparecem por ano.

### Módulos Necessários
- os
- signal
- subprocess
- ssl
- sqlite3
- time
- datetime
- dateutil
- string
- zlib
- urllib.request, urllib.parse, urllib.error

### Como usar

Abra o `gmane_run.py` para rodar o programa. Um interface de usuário no shell foi implementada, todas as opções são explicadas abaixo.

**Aplication Manager (Gerenciador da Aplicação)**: é a parte principal do programa, você pode escolher entre Spider, Model, Data Visualization ou Exit/Sair do programa;

1. **Spider**: será solicitado quantas mensagens o programa deverá ler e salvar no banco de dados bruto ***spider.sqlite***, para interromper o programa a qualquer momento pressione <CTRL + C> e insira <Y> quando solicitado;
2. **Model**: cria ou atualiza automaticamente o banco de dados ***mode_db.sqlite*** a partir do ***spider.sqlite***;
3. **Data Visualization**: entra no menu **Visualization Model (Modelo de Visualização)**:
   1. **Basic**: solicita quantas organizações e remententes para mostrar no shell (deve-se inserir um número inteiro);
    2. **Word**: solicita quantas palavras mostrar no navegador (inteiro), em seguida cria os dados e pergunta se quer visualiza-los;
    3. **Line**: solicita quantas organizações e remententes para mostrar no navegador (inteiro), em seguida cria os dados e pergunta se quer visualiza-los;
    4. **Year**: solicita quantas organizações e remententes para mostrar no navegador (inteiro), em seguida cria os dados e pergunta se quer visualiza-los;
    5. **All Above (Todos Acima)**: roda todos os subprocessos acima em sequência;
    9. **Visualize Data (Visualizar Dados)**: entra no menu **Visualization Manager (Gerenciador de Visualização)**, onde você pode escolher dentre todos os modelos de visualização de dados acima para ser mostrado no navegador.

Se for inserido "0" o programa vai para o menu anterior ou sai do programa.

### Observações
- Todos os arquivos se subprocesso se encontram na pasta `files`;
- Todos os arquivos criados serão armazenados na pasta `files` (incluindo bancos de dados e arquivos javascript);
- Todos os arquivos htm estão na pasta `files`, você pode abri-los manualmente depois de ter criado os arquivos javascript necessários;
- Depois de cada passo no programa ele irá perguntar se você deseja seguir para a próxima etapa lógica, se sim insira <Y>, se não insira <N> para voltar ao menu;
- Todos os creditos vão para [dr-chuck](https://dr-chuck.com/) por prover os seguintes arquivos: "d3.layout.cloud.js", "d3.v2.js", "gline_year.htm", "gline.htm" and "gword.htm".

---

# Gmane Email Data Retriever

Program that retireve e-mail data from Gmane (actually from [dr-chuck server](https://mbox.dr-chuck.net) so the Gmane server don't get overfloaded), saves in a database and creates various data visualization models.

### Functionality

The program is subdivided in three major subprocesses: Spider, Model and Data Visualization.

1. The `Spider` retrieve e-mails data from [dr-chuck server](https://mbox.dr-chuck.net) and saves in a raw database called ***"spider.sqlite"***, the data are:
    - Sender e-mail;
    - Date;
    - Subject;
    - E-mail header;
    - E-mail body.

2. The `Model` takes the raw database and creates a new cleaner relational database called ***"model_db.sqlite"***. The datamodel can be checked in ***email_datamodel.png***.

3. The `Data Visualization` creates javascript (.js) files to be used as data for the htm files to render the visualization on a browser using the ***"D3 JavaScript"*** library. The models are:
    - **Basic**: show the top 'n' senders and organizations on shell (where 'n' is a chosen number);
    - **Word**: retrieve the top 'n' words longer than 3 chars from the subjects column and show them on various sizes depending on how many times those words appear;
    - **Line**: a line graph that shows how many times the top 'n' organizations appear on every month over the years;
    - **Year**: a line graph that shows how many times the top 'n' organizations appear on every year.

### Necessary Modules
- os
- signal
- subprocess
- ssl
- sqlite3
- time
- datetime
- dateutil
- string
- zlib
- urllib.request, urllib.parse, urllib.error

### How to use

Open `gmane_run.py` to run the program. It was implemented a shell user interface, all options are explained bellow.

**Aplication Manager**: is the main part of the program, you can chose Spider, Model, Data Visualization or Exit the program;

1. **Spider**: will prompt how many messages to read and save on the raw database ***spider.sqlite***, to interupt the process just press <CTRL + C> and enter <Y> when prompted;
2. **Model**: automatically creates or update the ***mode_db.sqlite*** database from the raw database;
3. **Data Visualization**: enters in the **Visualization Model** menu:
    1. **Basic**: prompt how many organizations and senders to show on shell (must be and integer);
    2. **Word**: prompt how many words to show in the browser (integer), after creating the data asks if you want to visualize the data;
    3. **Line**: prompt how many organizations to show in the browser (integer), after creating the data asks if you want to visualize the data;
    4. **Year**: prompt how many organizations to show in the browser (integer), after creating the data asks if you want to visualize the data;
    5. **All Above**: run all the above subprocesses in sequence;
    9. **Visualize Data**: enters in the **Visualization Manager** menu, where you can chose from all the above visualization model to be shown.

If "0" is entered it will go back to the previous menu or exit the program.

### Observations
- All subprocess files are in the `files` folder;
- All the created files will be stored in the `files` folder (including database and javascript files);
- All htm files are in the `files` folder, you can manually open them after creating the necessary javascript files;
- After every step of the program it will prompt if you wish to continue to the next logical step, enter <Y> if you wish to continue or <N> to go back to the menu;
- All credits goes to [dr-chuck](https://dr-chuck.com/) for providing the following files: "d3.layout.cloud.js", "d3.v2.js", "gline_year.htm", "gline.htm" and "gword.htm".
