from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response
import psycopg2
import psycopg2.extras
from werkzeug.exceptions import abort

app = Flask(__name__)

def get_connection():
    conn = psycopg2.connect(database="pabd_flask",
                            user="postgres",
                            password="sql",
                            host="localhost")
    return conn


@app.route('/') #redireciona automaticamente as páginas sem necessidade de alterar a url
def red():
    return redirect('/menu')

@app.route('/abdomem/')
def abdomem():
    return render_template('abdomem.html')

@app.route('/biceps/')
def biceps():
    return render_template('biceps.html')

@app.route('/costas/')
def costas():
    return render_template('costas.html')


@app.route('/ficha/',  methods=['GET', 'POST'])
def ficha():

    dbCon = get_connection() #estabelecer a conexão com o banco

    if request.method == 'POST': #tipo de requisição 

        dados = request.form #pega os dados requisitados do form
                
        with dbCon.cursor() as cur: #abre o cursor no banco 

            for z in dados.items():                           #percorre por cada campo para checar se já existe um dado para o dia

                cur.execute('SELECT * FROM Ficha_treino WHERE dia = %s', [z[0]])

                dia_escolhido = cur.fetchall() #realiza consultas otimizadas em bancos de dados

                if len(dia_escolhido) == 0:                         # se nao existir, ele cria. Caso já exista, ele atualiza
                    cur.execute('INSERT INTO Ficha_treino VALUES (%s,%s)', z)
                else:
                    cur.execute('UPDATE Ficha_treino SET treino = %s WHERE dia = %s' , [z[1], z[0]])
    
            dbCon.commit()                                          #atualizar as alterações feitas

    dias = {'Segunda': '', 'Terça': '', 'Quarta': '', 'Quinta': '', 'Sexta': '', 'Sábado': '', 'Domingo': ''}  #guardar os dados que vão ser exibidos
    
    with dbCon.cursor() as cur:     #pega os dados no banco

        cur.execute('SELECT * FROM Ficha_treino')

        dias_adquiridos = cur.fetchall()  #realiza consultas otimizadas em bancos de dados

    for y in dias_adquiridos:       #percorrer pelos dias e inserir o treino no dicionário de dias
        dias [y[0]] = y[1]

    return render_template('ficha.html', dias = dias) #renderizar a página


@app.route('/flexao/')
def flexao():
    return render_template('flexao.html')

@app.route('/menu')
def menu():
    return render_template('index.html')

@app.route('/peito/')
def peito():
    return render_template('peito.html')

@app.route('/pernas/')
def pernas():
    return render_template('pernas.html')


@app.route('/tela-cadastro', methods=['GET', 'POST'])
def tela_cadastro():

    if request.method == 'POST':        #tipo de requisição 

        dados = request.form            #pega os dados requisitados do form

        dbCon = get_connection()        #estabelecer a conexão com o banco

        try:
            with dbCon.cursor() as cur:              #com o cursor do banco, pega os usuários que possuem o email igual ao enviado       

                cur.execute('SELECT * FROM cadastro WHERE %s = cadastro.email', [dados['Email']])

                dados_banco = cur.fetchall()           #realizar a consulta no banco

                if len(dados_banco) != 0: #checar se já existe um usuário com as informções
                    return render_template('tela-cadastro.html')

                cur.execute('INSERT INTO Cadastro VALUES (%s, %s, %s)', [dados['Nome'], dados['Email'], dados['Senha']]) #insere no banco os dados do formulário

                dbCon.commit()  #atualizar as alterações feitas

                return redirect('/tela-login')
        except:                              #tratar qualquer chance de erro no banco
            dbCon.rollback()


    return render_template('tela-cadastro.html')


@app.route('/tela-login', methods=['GET', 'POST'])
def tela_login():

    if request.method == 'POST':                #tipo de requisição

        dados = request.form                    #pega os dados requisitados do form

        dbCon = get_connection()                #estabelecer a conexão com o banco


        try:
            with dbCon.cursor() as cur: #pega do banco os usuários que possuem o nome igual ao enviado

                cur.execute('SELECT * FROM cadastro WHERE %s = cadastro.usuario', [dados['usuario']])

                dados_banco = cur.fetchall() #realiza consultas otimizadas em bancos de dados

                if len(dados_banco) == 0 or dados_banco[0][2] != dados['senha']: #checar se o usário existe e a senha cadastrada está correta
                    return render_template('tela-login.html')


                return redirect('/menu')
        except:                         #tratar qualquer chance de erro no banco
            dbCon.rollback()

    return render_template('tela-login.html')