import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox

class CadastroProcessoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cadastro de Processo')
        self.setGeometry(0,0, 500, 300)
        self.center_on_screen()      

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label_id = QLabel('ID:', self)
        self.edit_id = QLineEdit(self)

        self.label_processo = QLabel('Processo:', self)
        self.edit_processo = QLineEdit(self)

        self.label_reclamante = QLabel('Reclamante:', self)
        self.edit_reclamante = QLineEdit(self)

        self.label_reclamada = QLabel('Reclamada:', self)
        self.edit_reclamada = QLineEdit(self)

        self.label_intimacao = QLabel('Data de Intimação:', self)
        self.edit_intimacao = QLineEdit(self)

        self.label_entrega = QLabel('Data de Entrega:', self)
        self.edit_entrega = QLineEdit(self)

        self.label_implementacao = QLabel('Data de Implementação:', self)
        self.edit_implementacao = QLineEdit(self)

        self.btn_cadastrar = QPushButton('Cadastrar', self)
        self.btn_cadastrar.clicked.connect(self.cadastrar_processo)

        self.layout.addWidget(self.label_id)
        self.layout.addWidget(self.edit_id)
        self.layout.addWidget(self.label_processo)
        self.layout.addWidget(self.edit_processo)
        self.layout.addWidget(self.label_reclamante)
        self.layout.addWidget(self.edit_reclamante)
        self.layout.addWidget(self.label_reclamada)
        self.layout.addWidget(self.edit_reclamada)
        self.layout.addWidget(self.label_intimacao)
        self.layout.addWidget(self.edit_intimacao)
        self.layout.addWidget(self.label_entrega)
        self.layout.addWidget(self.edit_entrega)
        self.layout.addWidget(self.label_implementacao)
        self.layout.addWidget(self.edit_implementacao)
        self.layout.addWidget(self.btn_cadastrar)

        self.central_widget.setLayout(self.layout)

    def cadastrar_processo(self):
        id_processo = self.edit_id.text()
        processo = self.edit_processo.text()
        reclamante = self.edit_reclamante.text()
        reclamada = self.edit_reclamada.text()
        intimacao = self.edit_intimacao.text()
        entrega = self.edit_entrega.text()
        implementacao = self.edit_implementacao.text()

        if id_processo and processo and reclamante and reclamada and intimacao and entrega and implementacao:
        
            id_processo = self.obter_proximo_id()

            novo_processo = {
                "ID": id_processo,
                "Processo": processo,
                "Reclamante": reclamante,
                "Reclamada": reclamada,
                "Data de Intimação": intimacao,
                "Data de Entrega": entrega,
                "Data de Implementação": implementacao
            }

            caminho_arquivo = 'painelDeControle/Json/BancoDeDados.json'

            if not self.arquivo_existe(caminho_arquivo):
                # Se o arquivo não existe, cria um novo arquivo com os dados fornecidos
                with open(caminho_arquivo, 'w') as arquivo_json:
                    json.dump([novo_processo], arquivo_json, indent=2)
            else:
                # Se o arquivo existe, carrega os dados existentes
                with open(caminho_arquivo, 'r') as arquivo_json:
                    dados_existentes = json.load(arquivo_json)
                
                # Verifica se os dados existentes são uma lista
                if not isinstance(dados_existentes, list):
                    dados_existentes = []
                
                # Adiciona o novo processo aos dados existentes
                dados_existentes.append(novo_processo)

                # Escreve os dados atualizados de volta no arquivo
                with open(caminho_arquivo, 'w') as arquivo_json:
                    json.dump(dados_existentes, arquivo_json, indent=2)
            
            QMessageBox.information(self, 'Sucesso', 'Processo cadastrado com sucesso!')
            self.limpar_campos()
        else:
            QMessageBox.warning(self, 'Aviso', 'Por favor, preencha todos os campos.')

    def obter_proximo_id(self):
        # Obtém o último ID cadastrado ou retorna 1 se não houver nenhum ID ainda
        caminho_arquivo = 'painelDeControle/Json/BancoDeDados.json'
        if self.arquivo_existe(caminho_arquivo):
            with open(caminho_arquivo, 'r') as arquivo_json:
                dados_existentes = json.load(arquivo_json)

            if dados_existentes:
                # Obtém o último ID cadastrado
                ultimo_id = int(dados_existentes[-1].get("ID"))
                # Incrementa 1 para o próximo ID
                proximo_id = ultimo_id + 1
                return str(proximo_id)
        
        # Se não houver nenhum ID cadastrado ainda, retorna 1
        return "1"            

    def arquivo_existe(self, caminho):
        return os.path.exists(caminho)

    def limpar_campos(self):
        self.edit_id.clear()
        self.edit_processo.clear()
        self.edit_reclamante.clear()
        self.edit_reclamada.clear()
        self.edit_intimacao.clear()
        self.edit_entrega.clear()
        self.edit_implementacao.clear()

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
    cadastro_app = CadastroProcessoApp()
    cadastro_app.show()
    sys.exit(app.exec_())
