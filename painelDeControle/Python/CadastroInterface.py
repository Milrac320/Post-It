import json
import os
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

class CadastroInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cadastro')
        self.setGeometry(0,0, 400, 200)
        self.center_on_screen()              

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label_email = QLabel('E-mail:', self)
        self.edit_email = QLineEdit(self)

        self.label_cpf = QLabel('CPF:', self)
        self.edit_cpf = QLineEdit(self)

        self.label_senha = QLabel('Senha:', self)
        self.edit_senha = QLineEdit(self)
        self.edit_senha.setEchoMode(QLineEdit.Password)

        self.btn_cadastrar = QPushButton('Cadastrar', self)
        self.btn_cadastrar.clicked.connect(self.cadastrar)

        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.edit_email)
        self.layout.addWidget(self.label_cpf)
        self.layout.addWidget(self.edit_cpf)
        self.layout.addWidget(self.label_senha)
        self.layout.addWidget(self.edit_senha)
        self.layout.addWidget(self.btn_cadastrar)

        self.central_widget.setLayout(self.layout)

    def cadastrar(self):
        email = self.edit_email.text()
        cpf = self.edit_cpf.text()
        senha = self.edit_senha.text()

        if email and cpf and senha:
            # Validar CPF (pode adicionar uma verificação mais robusta)
            if len(cpf) != 11 or not cpf.isdigit():
                QMessageBox.warning(self, 'Erro no CPF', 'Por favor, insira um CPF válido (11 dígitos numéricos).')
                return

            # Hash da senha antes de armazenar
            hashed_senha = hashlib.sha256(senha.encode()).hexdigest()

            novo_usuario = {
                "Email": email,
                "CPF": cpf,
                "Senha": hashed_senha
            }

            caminho_arquivo = 'painelDeControle/Json/usuarios.json'

            if not self.arquivo_existe(caminho_arquivo):
                # Se o arquivo não existe, cria um novo arquivo com os dados fornecidos
                with open(caminho_arquivo, 'w') as arquivo_json:
                    json.dump([novo_usuario], arquivo_json, indent=2)
            else:
                # Se o arquivo existe, carrega os dados existentes
                with open(caminho_arquivo, 'r') as arquivo_json:
                    dados_existentes = json.load(arquivo_json)
                
                # Verifica se os dados existentes são uma lista
                if not isinstance(dados_existentes, list):
                    dados_existentes = []
                
                # Adiciona o novo usuário aos dados existentes
                dados_existentes.append(novo_usuario)

                # Escreve os dados atualizados de volta no arquivo
                with open(caminho_arquivo, 'w') as arquivo_json:
                    json.dump(dados_existentes, arquivo_json, indent=2)
            
            QMessageBox.information(self, 'Cadastrado', 'Usuário cadastrado com sucesso!')
            self.close()  # Fecha a janela de cadastro após o sucesso
        else:
            QMessageBox.warning(self, 'Aviso', 'Por favor, preencha todos os campos.')

    def arquivo_existe(self, caminho):
        return os.path.exists(caminho)

    def center_on_screen(self):
        # Obtém a geometria da tela
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calcula as coordenadas x e y para centralizar a janela
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Move a janela para as coordenadas calculadas
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication([])
    cadastro_interface = CadastroInterface()
    cadastro_interface.show()
    app.exec_()
