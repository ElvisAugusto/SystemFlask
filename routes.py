from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, time
from functions import *
from app import app, db
from models import Usuario, Balanca, CadastroForm, LoginForm, AddValueForm, CaixaForm, RelatorioForm
from flask_bcrypt import check_password_hash, generate_password_hash

# Lista global para armazenar os valores da refeição
refeicao = []

# Função para verificar a autenticação do usuário
def verificar_autenticacao():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

@app.route('/')
def index():
    # Chama a função de logout para garantir que não haja sessão ativa
    logout()
    form = LoginForm()  # Instancia o formulário de login
    return render_template('login.html', form=form)
@app.route('/logout')
def logout():
    session.clear()  # Limpa todos os dados da sessão
    return redirect(url_for('index'))  # Redireciona para a página de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instancia o formulário de login
    if form.validate_on_submit():  # Verifica se o formulário foi submetido e validado
        email = form.email.data
        usuario = Usuario.query.filter_by(email=email).first()  # Busca o usuário pelo e-mail
        if usuario and check_password_hash(usuario.senha,
                                           form.senha.data):  # Verifica se o usuário existe e se a senha está correta
            session['usuario_logado'] = usuario.id  # Armazena o ID do usuário na sessão
            return redirect(url_for('menu'))  # Redireciona para a página menu em caso de sucesso
        else:
            flash('Falha no login! Verifique suas credenciais.', 'error')
            return redirect(url_for('login'))  # Redireciona de volta para a página de login em caso de falha
    return render_template('login.html', form=form)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = CadastroForm()  # Instancia o formulário de cadastro
    if form.validate_on_submit():  # Verifica se o formulário foi submetido e validado
        nome = form.nome.data
        email = form.email.data
        senha = generate_password_hash(form.senha.data).decode('utf-8')  # Gera o hash da senha
        usuario_existente = Usuario.query.filter_by(email=email).first()  # Verifica se o email já está em uso
        if usuario_existente:
            flash('Este email já está em uso.', 'error')
            return redirect(url_for('cadastrar'))
        else:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)  # Adiciona o novo usuário ao banco de dados
            db.session.commit()  # Confirma a transação
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/menu')
def menu():
    if verificar_autenticacao():
        return verificar_autenticacao()  # Redireciona para a página de login se não estiver autenticado
    return render_template('menu.html')

@app.route('/balanca', methods=['GET', 'POST'])
def balanca():
    global refeicao
    if verificar_autenticacao():
        return verificar_autenticacao()  # Redireciona para a página de login se não estiver autenticado

    form = AddValueForm()  # Instancia o formulário de adição de valor
    total = locale.currency(sum(refeicao), grouping=True)  # Calcula o total dos valores da refeição
    refeicao_valor = [locale.currency(valor, grouping=True) for valor in refeicao]  # Formata os valores da refeição

    return render_template('balanca.html', form=form, valor=total, refeicao=refeicao_valor)

@app.route('/add_value', methods=['POST'])
def add_value():
    global refeicao
    if verificar_autenticacao():
        return verificar_autenticacao()  # Redireciona para a página de login se não estiver autenticado

    form = AddValueForm()  # Instancia o formulário de adição de valor

    if form.validate_on_submit():
        if 'adicionar' in request.form:  # Se o botão "Adicionar" foi pressionado
            valor = form.valor.data  # Obtém o valor do formulário
            valor = float(valor.replace(',', '.'))  # Converte o valor para float
            if valor != 0.00:
                refeicao.append(valor)  # Adiciona o valor à lista de refeição
                flash('Valor adicionado!')
                return redirect(url_for('balanca'))
            else:
                flash('Insira um valor!')
                return redirect(url_for('balanca'))
        elif 'confirmar' in request.form:  # Se o botão "Confirmar" foi pressionado
            if refeicao:  # Verifica se há valores na lista de refeição
                total = sum(refeicao)  # Calcula o total dos valores da refeição
                numero_refeicoes = len(refeicao)  # Obtém o número de refeições
                usuario_id = session['usuario_logado']  # Obtém o ID do usuário logado
                balanca = Balanca(usuario_id=usuario_id, numero_refeicoes=numero_refeicoes,
                                  total_refeicoes=total)  # Cria uma instância da classe Balanca
                db.session.add(balanca)  # Adiciona a instância ao banco de dados
                db.session.commit()  # Confirma a transação
                # Gera o QR Code
                qr_code_data = '00020126470014BR.GOV.BCB.PIX0125elvisaugusto520@gmail.com5204000053039865802BR5921Elvis Augusto Pedroso6009SAO PAULO62140510BFHrmk7ZKD6304B9FA'
                generate_qr_code(qr_code_data, "qr_code.png")
                # Gera o PDF com os detalhes do registro de balança
                generate_pdf(balanca.id, refeicao, balanca.total_refeicoes, "qr_code.png", "detalhes_balanca.pdf")
                refeicao = []  # Limpa a lista de refeição
                flash('Valor confirmado e salvo!')
                return redirect(url_for('balanca'))
            else:
                flash('Adicione um valor antes de confirmar!')
                return redirect(url_for('balanca'))
        elif 'limpar' in request.form:  # Se o botão "Limpar" foi pressionado
            refeicao = []  # Limpa a lista de refeição
            flash('Lista de refeição limpa!')
            return redirect(url_for('balanca'))
        elif 'voltar_menu' in request.form:  # Se o botão "Voltar menu" foi pressionado
            refeicao = []  # Limpa a lista de refeição
            return redirect(url_for('menu'))

    # Se o formulário não for válido ou não tiver sido submetido ainda, renderiza a página balanca.html com o formulário
    return render_template('balanca.html', form=form)

@app.route('/caixa', methods=['GET', 'POST'])
def caixa():
    if verificar_autenticacao():
        return verificar_autenticacao()  # Redireciona para a página de login se não estiver autenticado

    form = CaixaForm()  # Instancia o formulário de caixa

    if form.validate_on_submit():
        if 'buscar_id' in request.form:  # Se o botão "Buscar ID" foi pressionado
            id_refeicao = form.id_refeicao.data
            session['id_refeicao'] = id_refeicao  # Armazena o ID na sessão
            registro_balanca = Balanca.query.filter_by(id=id_refeicao).first()  # Busca o registro pelo ID
            if registro_balanca:
                total_pagamento = locale.currency(registro_balanca.total_refeicoes,
                                                  grouping=True)  # Formata o valor total
                flash(f'ID {id_refeicao} - Total a pagar: {total_pagamento}')
                return redirect(url_for('caixa'))
            else:
                flash('ID não encontrado!')
                return redirect(url_for('caixa'))
        elif 'voltar_menu' in request.form:  # Se o botão "Voltar menu" foi pressionado
            return redirect(url_for('menu'))
        elif 'realizar_pagamento' in request.form:  # Se o botão "Realizar Pagamento" foi pressionado
            id_refeicao = session.get('id_refeicao')  # Obtém o ID da sessão
            forma_pagamento = form.forma_pagamento.data  # Obtém a forma de pagamento
            registro_balanca = Balanca.query.filter_by(id=id_refeicao).first()  # Busca o registro pelo ID
            if registro_balanca:
                registro_balanca.forma_pagamento = forma_pagamento  # Atualiza a forma de pagamento
                db.session.commit()  # Confirma a transação
                session.pop('id_refeicao')  # Remove o ID da sessão após o pagamento
                flash('Pagamento realizado com sucesso!')
                return render_template('caixa.html', form=form)
            else:
                flash('Primeiro insira um ID Valido, depois a forma de pagamento.')
                return redirect(url_for('caixa'))
        elif 'cancelar' in request.form:  # Se o botão "Cancelar" foi pressionado
            if 'id_refeicao' in session:
                session.pop('id_refeicao')  # Remove o ID da sessão após o cancelamento
            return redirect(url_for('caixa'))

    return render_template('caixa.html', form=form)

@app.route('/relatorio', methods=['POST', 'GET'])
def relatorio():
    if verificar_autenticacao():
        return verificar_autenticacao()  # Redireciona para a página de login se não estiver autenticado

    form = RelatorioForm()  # Instancia o formulário de relatório

    if form.validate_on_submit():
        if 'gerar_relatorio' in request.form:  # Se o botão "Gerar Relatório" foi pressionado
            try:
                data_inicial = form.data_inicial.data  # Obtém a data inicial do formulário
                data_final = form.data_final.data  # Obtém a data final do formulário

                # Realiza a consulta no banco de dados entre as datas fornecidas
                consulta_banco = Balanca.query.filter(Balanca.data.between(data_inicial, data_final)).all()

                # Inicializa as variáveis para armazenar os totais
                total_refeicoes = 0
                total_valor_refeicoes = 0
                total_campos_preenchidos = 0
                total_campos_naopreenchidos = 0
                ids_nao_pagos = []

                # Soma os valores das colunas numero_refeicoes e total_refeicoes
                for registro in consulta_banco:
                    total_refeicoes += registro.numero_refeicoes
                    total_valor_refeicoes += registro.total_refeicoes

                    # Verifica se o campo de forma de pagamento está preenchido
                    if registro.forma_pagamento:
                        total_campos_preenchidos += 1
                    else:
                        total_campos_naopreenchidos += 1
                        ids_nao_pagos.append(registro.id)

                # Formata os valores monetários
                total_valor_refeicoes = locale.currency(total_valor_refeicoes, grouping=True)

                # Flash dos resultados individualmente
                flash('Total de refeições vendidas: {}'.format(total_refeicoes))
                flash('Valor total arrecadado: {}'.format(total_valor_refeicoes))
                flash('Quantidade de pagadores: {}'.format(total_campos_preenchidos))
                flash('Quantidade de não pagadores: {}'.format(total_campos_naopreenchidos))
                flash('IDs que não pagaram: {}'.format(ids_nao_pagos))

                return redirect(url_for('relatorio'))

            except ValueError:
                flash('Por favor, preencha as datas e horários do formulário.')
                return redirect(url_for('relatorio'))

        elif 'voltar_menu' in request.form:  # Se o botão "Voltar menu" foi pressionado
            return redirect(url_for('menu'))

    return render_template('relatorio.html', form=form)
