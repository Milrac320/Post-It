import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QFile, QTextStream, Qt
from CadastroInterface import CadastroInterface
from PainelInterface import PainelInterface
import json
import hashlib

class MenuInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menu Interface')
        self.setGeometry(0, 0, 400, 200)
        self.center_on_screen()        

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Layout horizontal para os campos de e-mail
        email_layout = QHBoxLayout()
        self.label_email = QLabel('E-mail:', self)
        self.edit_email = QLineEdit(self)
        email_layout.addWidget(self.label_email)
        email_layout.addWidget(self.edit_email)

        # Layout horizontal para os campos de senha
        senha_layout = QHBoxLayout()
        self.label_senha = QLabel('Senha:', self)
        self.edit_senha = QLineEdit(self)
        self.edit_senha.setEchoMode(QLineEdit.Password)
        senha_layout.addWidget(self.label_senha)
        senha_layout.addWidget(self.edit_senha)

        # Adiciona os layouts horizontais ao layout vertical principal
        self.layout.addLayout(email_layout)
        self.layout.addLayout(senha_layout)

        self.btn_login = QPushButton('Login', self)
        self.btn_login.clicked.connect(self.login)

        self.btn_cadastrar = QPushButton('Cadastrar', self)
        self.btn_cadastrar.clicked.connect(self.abrir_cadastro)

        self.layout.addWidget(self.btn_login)
        self.layout.addWidget(self.btn_cadastrar)

        self.central_widget.setLayout(self.layout)

    def abrir_cadastro(self):
        self.cadastro_interface = CadastroInterface()
        self.cadastro_interface.show()
        
    def abrir_painel(self):
        self.painel_interface = PainelInterface()
        self.painel_interface.show()

    def login(self):
        email = self.edit_email.text()
        senha = self.edit_senha.text()

        if email and senha:
            hashed_senha_input = hashlib.sha256(senha.encode()).hexdigest()
            caminho_arquivo = 'painelDeControle/Json/usuarios.json'

            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r') as arquivo_json:
                    dados_usuarios = json.load(arquivo_json)

                for usuario in dados_usuarios:
                    if usuario.get("Email") == email and usuario.get("Senha") == hashed_senha_input:
                        # Lógica de login bem-sucedida
                        QMessageBox.information(self, 'Login', 'Login realizado com sucesso!')
                        
                        # Abre a interface Painel
                        self.abrir_painel()

                        # Fecha a interface Menu
                        self.close()

                        return

            QMessageBox.warning(self, 'Erro de Login', 'E-mail ou senha incorretos.')
        else:
            QMessageBox.warning(self, 'Aviso', 'Por favor, preencha e-mail e senha.')
    
    def center_on_screen(self):
        # Obtém a geometria da tela
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calcula as coordenadas x e y para centralizar a janela
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Move a janela para as coordenadas calculadas
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Carregar o arquivo CSS
    stylesheet = QFile("Css/stylesMenu.css")
    stylesheet.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(stylesheet)
    app.setStyleSheet(stream.readAll())

    menu_interface = MenuInterface()
    menu_interface.show()
    sys.exit(app.exec_())
