from sql_alchemy import banco
from flask import request
from flask import url_for
from requests import post

MAILGUN_DOMAIN = 'sandbox246d58bbbc4643b099e7e79b285aa733.mailgun.org'
MAILGUN_API_KEY = '57345997d2b7a38ad51c6d613018b680-a9919d1f-ce4076a5'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@restapihoteis.com'


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }
    
    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
            auth=("api", MAILGUN_API_KEY),
            data={"from": "{} <{}>".format(FROM_TITLE, FROM_EMAIL),
                "to": self.email,
                "subject": "Confirmação de cadastro",
                "text": "Confirme seu cadastro clicando no link a seguir: {}".format(link),
                "html": "<html><p>\
                    Confirme seu cadastro clicando no link a seguir: <a href='{}'>CONFIRMAR EMAIL<a>\
                    </p></html>".format(link)
                    }
                    )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None