import os
from .Dataset import Dataset


class Group(Dataset):
    """Classe responsável pelo download de grupos de datasets.

    Atributos
    ---------
    url_group: str
        a url para a consulta de grupos de conjuntos de dados da API da UFRN.
    available_groups: list
        lista de grupos de conjuntos de dados que estão disponíveis
        para download.
    """

    def __init__(self):
        super().__init__()

        self.url_group = self.url_base + 'api/rest/group/'
        self.available_groups = []
        self.load_groups()

    def load_groups(self):
        """Atualiza lista de grupos de datasets disponíveis."""
        self.available_groups = self._load_list('group_list')

    def list_groups(self):
        """Lista os grupos de dados."""
        self._print_list("grupos de dados", self.available_groups)

    def download_group(
        self, name: str, path: str = os.getcwd(), dictionary: bool = True
    ):
        """Exibe grupo de dados de acordo com seu nome
        e baixa-os em pastas com o nome do respectivo
        grupo de dados.

        > Exemplo: download_group('pessoas')

        Parâmetros
        ----------
        name: str
            nome do grupo
        path: str
            o caminho da pasta onde serão adicionados os arquivos
            (por padrão, a pasta atual)
        dictionary: bool
            flag para baixar o dicionário dos dados (por padrão, True)
        """

        # Checa se o grupo está disponível
        if not (name in self.available_groups):
            print("O grupo de dados \"{}\" não foi encontrado.".format(name))
            return

        groups = self._request_get(self.url_group + name)
        path = self._make_dir('{}/{}'.format(path, name))

        try:
            for package in groups['packages']:
                self.download_dataset(package, path, dictionary)

        except Exception as ex:
            self._print_exception(ex)

    def download_groups(self, groups: list,
                        path: str = os.getcwd(), dictionary: bool = True):
        """Exibe os grupos de dados de acordo com seu nome
        e baixa-os em pastas com o nome do respectivo
        grupo de dados.

        > Exemplo: download_groups(['biblioteca', 'ensino'])

        Parâmetros
        ----------
        groups: list
            lista com os nomes dos grupos desejados
        path: str
            o caminho da pasta onde serão adicionados os arquivos
            (por padrão, a pasta atual)
        dictionary: bool
            flag para baixar o dicionário dos dados (por padrão, True)
        """

        for group in groups:
            self.download_group(group, path, dictionary)

    def search_related_groups(self, keyword: str) -> list:
        """Procura os grupos de conjuntos de dados que possuam nomes
        semelhantes à palavra recebida.

        > Exemplo: search_related_groups('pesquisa')

        Parâmetros
        ----------
        keyword: str
            palavra-chave com a qual será feita a busca
        """
        # Busca nomes de grupos semelhantes à palavra passada
        related = self.search_related(keyword, self.available_groups)

        # Imprime exceção se não houver grupos similares
        if not len(related):
            print(
                "Não há nenhum grupo de conjunto de dados"
                "semelhante a \"{}\".".format(keyword)
            )

        return related
