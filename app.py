from flask import Flask, redirect, render_template, request, url_for
from models.database import init_db
from models.desejos import Desejo

app = Flask(__name__)
init_db()


@app.route('/')
def home():
    return render_template('home.html', titulo='Must Watch List')


@app.route('/lista', methods=['GET', 'POST'])
def lista():
    if request.method == 'POST':
        titulo_desejo = request.form['titulo_desejo']
        tipo_desejo = request.form['tipo_desejo']
        indicado_por = request.form.get('indicado_por', '')  # Usar .get() para evitar KeyError
        novo_desejo = Desejo(titulo_desejo, tipo_desejo, indicado_por)
        novo_desejo.salvar_desejo()

    desejos = Desejo.obter_desejos()
    return render_template('lista.html', titulo='Lista de Desejos', desejos=desejos)

@app.route('/delete/<int:idDesejo>')
def delete(idDesejo):
    desejo = Desejo.id(idDesejo)
    desejo.excluir_desejo()
    return redirect(url_for('lista'))

  
@app.route('/update/<int:idDesejo>', methods=['GET', 'POST'])
def update(idDesejo):
    if request.method == 'POST':
        titulo_desejo = request.form['titulo_desejo']
        tipo_desejo = request.form['tipo_desejo']
        indicado_por = request.form.get('indicado_por', '')  # Usar .get() para evitar KeyError
        desejo = Desejo(titulo_desejo, tipo_desejo, indicado_por, idDesejo)
        desejo.atualizar_desejo()
        return redirect(url_for('lista'))

    desejos = Desejo.obter_desejos()
    desejo_selecionado = Desejo.id(idDesejo)
    return render_template('lista.html', titulo=f'Editando o desejo ID: {idDesejo}', desejos=desejos, desejo_selecionado=desejo_selecionado)

