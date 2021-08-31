from flask import Flask, Blueprint, render_template, request, redirect, url_for, current_app
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail',methods=['GET','POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_email(name,email,message)
        return render_template('portfolio/sent_mail.html')
    
    return redirect(url_for('portfolio.index'))

def send_email(name,email,message):
    miCorreo = 'ficettiesteban@gmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_API_KEY'])
    
    from_email = Email(miCorreo)
    to_email = To(miCorreo, substitutions={
        '-name-': name,
        '-email-': email,
        '-message-': message,
    })
    html_Content = ''' 
        <p>Hola Esteban!, tienes un nuevo contacto desde tu web!</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>message: -message-</p>

    '''

    mail = Mail(miCorreo, to_email, 'Nuevo contacto desde la web', html_content=html_Content)
    response = sg.client.mail.send.post(request_body=mail.get())