import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolBar, QAction, QStackedWidget, QMessageBox
from PyQt5.QtGui import QIcon
from NovoProcesso import CadastroProcessoApp

class PainelInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Visualizar Dados')
        self.setGeometry(0,0, 800, 400)
        self.center_on_screen()              

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)

        # Adiciona ação para recarregar os dados
        carregar = QAction(self)
        carregar.setText('Carregar')        
        carregar.setIcon(QIcon('painelDeControle/Png/recarregar.png'))
        carregar.triggered.connect(self.reload_data)
        self.toolbar.addAction(carregar)

        excluir = QAction(self)
        excluir.setText('Excluir')        
        excluir.setIcon(QIcon('painelDeControle/Png/excluir.png'))
        excluir.triggered.connect(self.excluir_selecionado)
        self.toolbar.addAction(excluir)

        # Adiciona um QStackedWidget para alternar entre painéis
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Adiciona um painel com a tabela
        self.tabela_dados = QTableWidget(self)
        self.stacked_widget.addWidget(self.tabela_dados)

        # Adiciona o CadastroProcessoApp como um widget no QStackedWidget
        self.cadastro_widget = CadastroProcessoApp()
        self.stacked_widget.addWidget(self.cadastro_widget)

        cadastro = QAction(self)
        cadastro.setText('Cadastrar')
        cadastro.setIcon(QIcon('painelDeControle/Png/adicionar.png'))
        cadastro.triggered.connect(self.show_cadastro_painel)
        self.toolbar.addAction(cadastro)

        # Adiciona botões na toolbar para alternar entre os painéis

        tabela=QAction(self)
        tabela.setText('Processos')
        tabela.setIcon(QIcon('painelDeControle/Png/tabela.png'))
        tabela.triggered.connect(self.show_tabela_panel)        
        self.toolbar.addAction(tabela)

        self.central_widget.setLayout(self.layout)

        # Conecta o sinal de seleção da tabela para habilitar/desabilitar o botão Excluir Selecionado
        self.tabela_dados.itemSelectionChanged.connect(self.atualizar_botao_excluir)

        self.stacked_widget.currentChanged.connect(self.atualizar_titulo_janela)

        # Carrega os dados ao iniciar o aplicativo
        self.carregar_dados('painelDeControle/Json/BancoDeDados.json')

    def carregar_dados(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo_json:
            dados = json.load(arquivo_json)

        if dados:
            # Defina o número de linhas e colunas com base nos dados
            self.tabela_dados.setRowCount(len(dados))
            self.tabela_dados.setColumnCount(len(dados[0]))

            # Defina os cabeçalhos da tabela
            headers = [key for key in dados[0]]
            self.tabela_dados.setHorizontalHeaderLabels(headers)

            # Preencha a tabela com os dados
            for i, linha in enumerate(dados):
                for j, item in enumerate(linha):
                    self.tabela_dados.setItem(i, j, QTableWidgetItem(str(linha[item])))
        else:
            self.tabela_dados.setRowCount(0)
            self.tabela_dados.setColumnCount(0)

    def reload_data(self):
        # Recarrega os dados quando o botão na toolbar é clicado
        self.carregar_dados('painelDeControle/Json/BancoDeDados.json')

    def show_tabela_panel(self):
        # Mostra o painel da tabela
        self.stacked_widget.setCurrentIndex(0)

    def show_cadastro_painel(self):
        # Mostra o painel de cadastro
        self.stacked_widget.setCurrentIndex(1)

    def atualizar_botao_excluir(self):
        # Habilita ou desabilita o botão Excluir Selecionado com base na seleção na tabela
        has_selection = bool(self.tabela_dados.selectedItems())
        self.toolbar.actions()[2].setEnabled(has_selection)

    def atualizar_titulo_janela(self, index):
        # Atualiza o título da janela com base no índice no QStackedWidget
        if index == 0:
            self.setWindowTitle('Visualizar Processos - Tabela')
        elif index == 1:
            self.setWindowTitle('Adicionar Processos - Cadastro')

    def excluir_selecionado(self):
        # Exclui a linha selecionada na tabela e atualiza o arquivo JSON
        selected_row = self.tabela_dados.currentRow()

        if selected_row >= 0:
            reply = QMessageBox.question(
                self, 'Confirmar Exclusão', 'Tem certeza que deseja excluir a linha selecionada?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Carrega os dados existentes do arquivo JSON
                caminho_arquivo = 'painelDeControle/Json/BancoDeDados.json'
                with open(caminho_arquivo, 'r') as arquivo_json:
                    dados_existentes = json.load(arquivo_json)

                # Remove a linha selecionada
                dados_existentes.pop(selected_row)

                # Escreve os dados atualizados de volta no arquivo
                with open(caminho_arquivo, 'w') as arquivo_json:
                    json.dump(dados_existentes, arquivo_json, indent=2)

                # Recarrega os dados na tabela
                self.carregar_dados(caminho_arquivo)

                QMessageBox.information(self, 'Sucesso', 'Linha excluída com sucesso!')
        else:
            QMessageBox.warning(self, 'Aviso', 'Por favor, selecione uma linha para excluir.')

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
    visualizar_app = PainelInterface()
    visualizar_app.show()
    app.exec_()
