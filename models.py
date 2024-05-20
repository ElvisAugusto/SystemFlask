from datetime import datetime
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired, ValidationError
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    entra = SubmitField('Entrar')
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    cadastrar = SubmitField('Cadastrar')
class AddValueForm(FlaskForm):
    valor = StringField('Valor', validators=[DataRequired()])
    adicionar = SubmitField('Adicionar')
    confirmar = SubmitField('Confirmar')
    limpar = SubmitField('Limpar')
    voltar_menu = SubmitField('Voltar menu')
class CaixaForm(FlaskForm):
    id_refeicao = StringField('ID Refeição', validators=[DataRequired()])
    buscar_id = SubmitField('Buscar ID')
    voltar_menu = SubmitField('Voltar menu')
    realizar_pagamento = SubmitField('Realizar Pagamento')
    forma_pagamento = SelectField('Forma de Pagamento', choices=[('Cartão'), ('Dinheiro'), ('Pix')],
                                  validators=[DataRequired()])
class RelatorioForm(FlaskForm):
    data_inicial = DateTimeField('Data Inicial', validators=[DataRequired()], format='%Y-%m-%dT%H:%M', default=datetime.now)
    data_final = DateTimeField('Data Final', validators=[DataRequired()], format='%Y-%m-%dT%H:%M', default=datetime.now)
    gerar_relatorio = SubmitField('Gerar Relatório')
    voltar_menu = SubmitField('Voltar Menu')

    def validate_data_final(form, field):
        if field.data < form.data_inicial.data:
            raise ValidationError('A data final não pode ser menor que a data inicial.')
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'
class Balanca(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('registros_balancas', lazy=True))
    numero_refeicoes = db.Column(db.Integer, nullable=False)
    total_refeicoes = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<Balanca {self.id}>'
