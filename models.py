from datetime import datetime
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError

# Formulário de login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo de email com validação de presença e formato de email
    senha = PasswordField('Senha', validators=[DataRequired()])  # Campo de senha com validação de presença
    entra = SubmitField('Entrar')  # Botão de submissão para login

# Formulário de cadastro
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])  # Campo de nome com validação de presença
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo de email com validação de presença e formato de email
    senha = PasswordField('Senha', validators=[DataRequired()])  # Campo de senha com validação de presença
    cadastrar = SubmitField('Cadastrar')  # Botão de submissão para cadastro

# Formulário para adicionar valores
class AddValueForm(FlaskForm):
    valor = StringField('Valor', validators=[DataRequired()])  # Campo de valor com validação de presença
    adicionar = SubmitField('Adicionar')  # Botão de submissão para adicionar valor
    confirmar = SubmitField('Confirmar')  # Botão de submissão para confirmar adição
    limpar = SubmitField('Limpar')  # Botão de submissão para limpar campos
    voltar_menu = SubmitField('Voltar menu')  # Botão de submissão para voltar ao menu

# Formulário para operações de caixa
class CaixaForm(FlaskForm):
    id_refeicao = StringField('ID Refeição', validators=[DataRequired()])  # Campo de ID da refeição com validação de presença
    buscar_id = SubmitField('Buscar ID')  # Botão de submissão para buscar ID da refeição
    voltar_menu = SubmitField('Voltar menu')  # Botão de submissão para voltar ao menu
    realizar_pagamento = SubmitField('Realizar Pagamento')  # Botão de submissão para realizar pagamento
    forma_pagamento = SelectField('Forma de Pagamento', choices=[('Cartão'), ('Dinheiro'), ('Pix')],
                                  validators=[DataRequired()])  # Campo de seleção para forma de pagamento

# Formulário para geração de relatórios
class RelatorioForm(FlaskForm):
    data_inicial = DateTimeField('Data Inicial', validators=[DataRequired()], format='%Y-%m-%dT%H:%M', default=datetime.now)  # Campo de data inicial com validação de presença e formato específico
    data_final = DateTimeField('Data Final', validators=[DataRequired()], format='%Y-%m-%dT%H:%M', default=datetime.now)  # Campo de data final com validação de presença e formato específico
    gerar_relatorio = SubmitField('Gerar Relatório')  # Botão de submissão para gerar relatório
    voltar_menu = SubmitField('Voltar Menu')  # Botão de submissão para voltar ao menu

    # Validação personalizada para garantir que a data final não seja menor que a data inicial
    def validate_data_final(form, field):
        if field.data < form.data_inicial.data:
            raise ValidationError('A data final não pode ser menor que a data inicial.')

# Modelo para usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Chave primária autoincrementada
    nome = db.Column(db.String(100), nullable=False)  # Campo de nome, não pode ser nulo
    email = db.Column(db.String(100), unique=True, nullable=False)  # Campo de email, deve ser único e não pode ser nulo
    senha = db.Column(db.String(100), nullable=False)  # Campo de senha, não pode ser nulo

    # Método para representação em string do objeto
    def __repr__(self):
        return f'<Usuario {self.nome}>'

# Modelo para registros da balança
class Balanca(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Chave primária autoincrementada
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira referenciando o ID do usuário
    usuario = db.relationship('Usuario', backref=db.backref('registros_balancas', lazy=True))  # Relacionamento com o modelo Usuario
    numero_refeicoes = db.Column(db.Integer, nullable=False)  # Campo para o número de refeições, não pode ser nulo
    total_refeicoes = db.Column(db.Float, nullable=False)  # Campo para o total de refeições, não pode ser nulo
    forma_pagamento = db.Column(db.String(50), nullable=True)  # Campo para a forma de pagamento, pode ser nulo
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)  # Campo para a data, não pode ser nulo, valor padrão é a data e hora atual

    # Método para representação em string do objeto
    def __repr__(self):
        return f'<Balanca {self.id}>'
