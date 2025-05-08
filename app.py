from flask import Flask, render_template, request, redirect, url_for  # Importa as funções principais do Flask
import mysql.connector  # Importa a biblioteca para conexão com MySQL

app = Flask(__name__)  # Cria a aplicação Flask
app.app_context().push()  # Garante que o contexto da aplicação esteja ativo

# Conexão com o banco de dados MySQL
mydb = mysql.connector.connect(
	host = "localhost",
	port = "3306",
	user = "root",
	password = "alunos",
	database = "bdprod"
)

mycursor = mydb.cursor(buffered=True)  # Cria um cursor com buffer para executar comandos SQL

#Toda hora eu esqueço o que é cursor buffer então vou deixar explicado aqui 😗:
#Quando você usa mysql.connector em Python para trabalhar com banco de dados, o cursor é o objeto
#que executa os comandos SQL (SELECT, INSERT, etc). O buffered=True significa que os resultados
#das consultas são armazenados na memória imediatamente depois que você faz a consulta.

# Rota principal (página inicial)
@app.route('/')
def principal():
	return render_template("index_mysql.html")  # Renderiza o template da página inicial

# Rota para cadastro de produtos
@app.route('/categorias', methods = ["POST", "GET"])
def categorias_func():
	if request.method == "POST":  # Se o método for POST, o formulário foi enviado
		print("PASSOU NO POST")  # Mensagem no terminal para mostrar se está passando porque cometi 3 mil erros tentando executar

		# Verifica se todos os campos do formulário foram preenchidos
		if request.form.get("id") and request.form.get("nome") and request.form.get("descricao") and request.form.get("preco") and request.form.get("marca"):
			id_var = request.form.get("id")  # Pega o ID do formulário
			nome_var = request.form.get("nome")  # Nome do produto
			descricao_var = request.form.get("descricao")  # Descrição do produto
			preco_var = request.form.get("preco")  # Preço do produto
			marca_var = request.form.get("marca")  # Marca do produto

			# Comando SQL para inserir os dados na tabela "produtos"
			sql = "INSERT INTO produtos (ID, NOME, DESCRICAO, PRECO, MARCA) VALUES (%s, %s, %s, %s, %s)"
			val = (id_var, nome_var, descricao_var, preco_var, marca_var)
			mycursor.execute(sql, val)  # Executa o comando
			mydb.commit()  # Salva as alterações no banco

			# Se pelo menos uma linha foi inserida com sucesso, redireciona para a listagem
			if mycursor.rowcount >= 1:
				return redirect(url_for('listar_func'))
			else:  # Caso contrário, também redireciona por algum motivo mas há a notificação de erro embaixo
				print("Erro")
				return redirect(url_for('listar_func'))

	return render_template("categorias.html")  # Se for GET, exibe o formulário de cadastro

# Rota para a página de sucesso
@app.route('/sucesso')
def sucesso_func():
	return render_template("sucesso.html")

# Rota para listar todos os produtos cadastrados
@app.route('/listar')
def listar_func():
	mycursor = mydb.cursor()  # Cria um cursor novo
	mycursor.execute("SELECT * FROM produtos")  # Executa a consulta para pegar todos os produtos
	myresult = mycursor.fetchall()  # Pega todos os resultados retornados
	return render_template("lista_categorias.html", categorias = myresult)  # Envia os dados para o template

# Rota para remover um produto pelo ID
@app.route('/<int:id>/remove_categoria')
def remove_categoria(id):
	sql = "DELETE FROM produtos WHERE id=%s"  # Comando SQL para deletar o produto com ID correspondente
	val = (id, )
	mycursor.execute(sql, val)  # Executa o comando
	mydb.commit()  # Salva a alteração no banco
	return redirect(url_for("listar_func"))  # Redireciona de volta para a listagem

# Rota para atualizar os dados de um produto
@app.route('/<int:id>/atualiza_categoria', methods = ["POST", "GET"])
def atualiza_categoria(id):
	mycursor = mydb.cursor(buffered=True)  # Cria um cursor com buffer

	# Consulta o produto pelo ID para pegar os dados atuais
	sql = "SELECT * FROM produtos where id=%s"
	val = (id,)
	mycursor.execute(sql, val)
	myresult = mycursor.fetchone()  # Retorna apenas um produto

	# Se o formulário foi enviado (método POST)
	if request.method == "POST":
		# Verifica se os campos do formulário foram preenchidos
		if request.form.get("id") and request.form.get("nome") and request.form.get("descricao") and request.form.get("preco") and request.form.get("marca"):
			id_var = request.form.get("id")  # Pega o ID
			nome_var = request.form.get("nome")
			descricao_var = request.form.get("descricao")
			preco_var = request.form.get("preco")
			marca_var = request.form.get("marca")

			# Comando SQL para atualizar os dados do produto
			sql = "UPDATE produtos set nome=%s, descricao=%s, preco=%s, marca=%s WHERE id=%s"
			val = (nome_var, descricao_var, preco_var, marca_var, id_var)
			mycursor.execute(sql, val)  # Executa a atualização
			mydb.commit()  # Salva no banco

			# Se a atualização deu certo, redireciona para a listagem, todas as rotas voltam para a listagem
			if mycursor.rowcount >= 1:
				return redirect(url_for('listar_func'))
			else:
				print("Erro")
				return redirect(url_for('listar_func'))

	# Exibe o formulário de atualização com os dados atuais preenchidos
	return render_template("update.html", id=myresult[0], nome=myresult[1], descricao=myresult[2], preco=myresult[3], marca=myresult[4])

# Inicia o servidor Flask em modo debug pra passar raiva testando até funcionar
if __name__ == "__main__":
	app.run(debug = True)

# Cansei, queria estar jogando roblox e comendo bolacha