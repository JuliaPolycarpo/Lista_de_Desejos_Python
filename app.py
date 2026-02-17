from flask import Flask, redirect, render_template, request, url_for
from models.database import init_db
from models.desejos import Desejo
import os
from werkzeug.utils import secure_filename #importação necessária para salvar as imagens com um nome seguro, o secure_filename remove caracteres perigosos do nome do arquivo enviado pelo usuário, impedindo ataques como path traversal (ex: "../../../arquivo.py") e evitando que arquivos do sistema sejam sobrescritos.

app = Flask(__name__) 
init_db()

# faço isso para habilitar o salvamento de imagens na pasta static/images
UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html', titulo='Must Watch List')


@app.route('/lista', methods=['GET', 'POST'])
def lista():
    if request.method == 'POST':
        titulo_desejo = request.form['titulo_desejo']
        tipo_desejo = request.form['tipo_desejo']
        indicado_por = request.form.get('indicado_por', '')  # usar .get() para evitar KeyError
        imagem = request.files.get('imagem') # pegar o arquivo de imagem, se ele existir 

        nome_imagem = None
        if imagem and imagem.filename != "": # verifica se o arquivo existe e se tem um nome válido
            nome_imagem = secure_filename(imagem.filename) # gera um nome seguro para o arquivo
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_imagem) # cria o caminho completo para salvar a imagem. O "os.path.join" é usado para garantir que o caminho seja construído corretamente, independentemente do sistema operacional.
            imagem.save(caminho) # salva a imagem no servidor

        novo_desejo = Desejo(titulo_desejo, tipo_desejo, indicado_por, nome_imagem)
        novo_desejo.salvar_desejo()

    desejos = Desejo.obter_desejos()
    return render_template('lista.html', titulo='Lista de Desejos', desejos=desejos)

@app.route('/delete/<int:idDesejo>')
def delete(idDesejo):
    desejo = Desejo.id(idDesejo)

    if desejo and desejo.imagem: # verifica se o desejo existe e se tem uma imagem associada
       caminho = os.path.join(app.config["UPLOAD_FOLDER"], desejo.imagem) # cria o caminho completo para a imagem usando o nome da imagem armazenado no banco de dados
       if os.path.exists(caminho): # verifica se o arquivo de imagem existe antes de tentar removê-lo para evitar erros
            os.remove(caminho) # remove a imagem do servidor

    desejo.excluir_desejo()
    return redirect(url_for('lista'))

  
@app.route('/update/<int:idDesejo>', methods=['GET', 'POST'])
def update(idDesejo):
    if request.method == 'POST':
        titulo_desejo = request.form['titulo_desejo']
        tipo_desejo = request.form['tipo_desejo']
        indicado_por = request.form.get('indicado_por', '') 
        imagem = request.files.get('imagem') # pegar o arquivo de imagem, se ele existir 
        nome_imagem = None

        if imagem and imagem.filename != "": # verifica se o arquivo existe e se tem um nome válido
            nome_imagem = secure_filename(imagem.filename) # gera um nome seguro para o arquivo
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_imagem) # cria o caminho completo para salvar a imagem. O "os.path.join" é usado para garantir que o caminho seja construído corretamente, independentemente do sistema operacional.
            imagem.save(caminho) # salva a imagem no servidor
        else:
            # Mantém a imagem antiga caso nenhuma nova imagem seja enviada
            desejo_atual = Desejo.id(idDesejo)
            nome_imagem = desejo_atual.imagem    

        desejo = Desejo( titulo_desejo, tipo_desejo, indicado_por, nome_imagem, id_desejo=idDesejo)
        desejo.atualizar_desejo()
        return redirect(url_for('lista'))

    desejos = Desejo.obter_desejos()
    desejo_selecionado = Desejo.id(idDesejo)
    return render_template('lista.html', titulo=f'Editando o desejo ID: {idDesejo}', desejos=desejos, desejo_selecionado=desejo_selecionado)
