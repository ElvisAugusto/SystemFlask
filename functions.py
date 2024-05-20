from flask import Flask
from flask_weasyprint import HTML, render_pdf  # Importando para gerar PDF
import pytz
from fpdf import FPDF
import qrcode
import locale
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

# Defina a localidade para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class FomularioCadastro(FlaskForm):
    # Definindo um formulário de cadastro usando Flask-WTF
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=100)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha = StringField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    salvar = SubmitField('Cadastrar')

def generate_pdf(id, refeicoes, total_refeicoes, qr_code_data, file_name):
    # Função para gerar um PDF usando a biblioteca FPDF
    pdf = FPDF()

    # Adicione uma página ao PDF
    pdf.add_page()

    # Defina a fonte para o título (Arial, negrito, 16)
    pdf.set_font("Arial", "B", 16)

    # Escreva o título da comanda
    pdf.cell(200, 10, "Comanda", ln=True, align="C")

    # Adicione uma quebra de linha
    pdf.ln(10)

    # Adicione os detalhes do registro (ID e lista de refeições)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"ID: {id}", ln=True)
    pdf.cell(200, 10, "Refeições:", ln=True)

    # Adicione a lista enumerada de refeições, formatada como moeda brasileira
    for i, refeicao in enumerate(refeicoes, start=1):
        pdf.cell(200, 10, f"{i}. {locale.currency(refeicao, grouping=True)}", ln=True)

    # Adicione o total de refeições, formatado como moeda brasileira
    pdf.cell(200, 10, f"Total a pagar: {locale.currency(total_refeicoes, grouping=True)}", ln=True)

    # Adicione o QR Code de pagamento
    pdf.cell(200, 10, "QR Code de Pagamento:", ln=True)
    pdf.ln(5)
    # Insere a imagem do QR Code no PDF
    pdf.image(qr_code_data, x=20, y=pdf.get_y(), w=50, h=50)

    # Salve o PDF no arquivo especificado por file_name
    pdf.output(file_name)

def generate_qr_code(data, file_name):
    # Função para gerar um QR Code usando a biblioteca qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)  # Adicione os dados ao QR Code
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)  # Salve a imagem do QR Code no arquivo especificado por file_name
