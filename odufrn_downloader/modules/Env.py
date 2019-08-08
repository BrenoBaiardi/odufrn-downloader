from abc import ABC
import requests
import os
import pprint


class Env(ABC):
    """Classe com os atributos e métodos responsáveis pelo
    funcionamento correto do pacote.

    Atributos
    ---------
    url_base: str
        a url para a API de dados abertos da UFRN.
    url_action: str
        a url para a página de ações da API.
    """

    def __init__(self):
        self.url_base = 'http://dados.ufrn.br/'
        self.url_action = self.url_base + 'api/action/'

    def _print_exception(self, ex: Exception):
        """Imprime mensagem padrão para exceções."""
        print('\033[91m{}\033[0m'.format(ex))
        print(
            "Ocorreu algum erro durante o download do pacote. "
            "Verifique sua conexão, o nome do conjunto de dados "
            "e tente novamente."
        )

    def _print_list(self, name: str, variable: list):
        """Mostra na tela a lista desejada."""
        print("Os {} disponíveis são:".format(name))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(variable)

    def _load_list(self, option: str) -> list:
        """Atualiza a lista desejada através de uma consulta.

        Parâmetros
        ----------
        option: str
            indica o que se deseja consultar pelo request."""
        try:
            packages = requests.get(self.url_action + option).json()
            return packages['result']
        except Exception as ex:
            self._print_exception(ex)

    def _make_dir(self, path: str) -> str:
        """Cria o diretório, caso ele não exista.

        Parâmetros
        ----------
        path: str
            o caminho da pasta onde serão adicionados os arquivos."""
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def _request_get(self, url: str) -> requests.Response:
        """Realiza a requisição desejada e retorna os dados
        e o caminho formado para download.

        Parâmetros
        ----------
        url: str
            a url que se deseja realizar a requisição.

        Retorno
        ----------
        requests.Response
            a resposta da requisição em json (dicionário)."""
        request_get = requests.get(url)

        return request_get.json()

    def _year_find(self, years: list, package_name: str) -> bool:
        """Verifica se o pacote pertence a uma ano específico da lista years.

        Parâmetros
        ----------
        years: list
            anos que serão filtrados na pesquisa.
        package_name: str
            nome do pacote a ser filtrado.
        Retorno
        ----------
        bool
            True se o ano foi encontrado no nome do pacote se não false."""
        year_find = False
        if years:
            for _, year in enumerate(years):
                if str(year) in package_name:
                    year_find = True
        return year_find
