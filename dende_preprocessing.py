from dende_statistics import Statistics
from typing import Dict, List, Set, Any

class MissingValueProcessor:
    """
    Processa valores ausentes (representados como None) no dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        """Retorna as colunas a serem processadas. Se 'columns' for vazio, retorna todas as colunas."""
        #vocês deveriam garantir se as colunas passadas realmente existem no dataset, para evitar erros de chave.
        # if columns:
        #     for col in columns:
        #         if col not in self.dataset:
        #             raise ValueError(f"Coluna '{col}' não encontrada no dataset.")
        return list(columns) if columns else list(self.dataset.keys())

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que possuem
        pelo menos um valor nulo (None, vazio ou N/A) em uma das colunas especificadas.

        """
        # Garante que o dataset recebido tem dados e mira nos espaços vazios
        #se a verificação das colunas tivesse sido feita na função _get_target_columns, 
        # aqui vocês poderiam simplesmente usar o resultado sem se preocupar das colunas passadas existirem
        alvos = self._get_target_columns(columns)
        if not alvos:
            return {}

        #seria melhor criar uma função para criar um novo dataset vazio, para evitar repetição de código
        # def create_empty_dataset(self):
        #     return {col: [] for col in self.dataset.keys()}
        # já que o código para criar um novo dataset vazio é repetido tanto no isna quanto no notna, 
        # seria interessante criar uma função para isso, evitando a repetição de código e 
        # melhorando a manutenção do código.

        num_linhas = len(self.dataset[alvos[0]])
        novo_dataset = {col: [] for col in self.dataset.keys()}

        #vocês poderia ter simplificado esse código usando a função filter e lambda:        

        for i in range(num_linhas):
            # Verifica se existe algum valor nulo na linha atual para as colunas alvo
            # poderia ter simplificado 
            # if any(self.dataset[col][i] in [None, "", "N/A"] for col in alvos): 
            
            tem_nulo = any(self.dataset[col][i] in [None, "", "N/A"] for col in alvos)
            if tem_nulo:
                for col in self.dataset.keys():
                    novo_dataset[col].append(self.dataset[col][i])

        return novo_dataset


    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Retorna um novo dataset contendo apenas as linhas que não possuem
        valores nulos (None) em nenhuma das colunas especificadas.
        """
        #mesmo problema de validação das colunas aqui, se a validação tivesse sido feita na função _get_target_columns, 
        # aqui vocês poderiam simplesmente usar o resultado sem se preocupar das colunas passadas existirem
        alvos = self._get_target_columns(columns)
        if not alvos:
            return {}

        #mesma questão de reutilização de código para criar um novo dataset vazio,
        # seria interessante criar uma função para isso, evitando a repetição de código e melhorando 
        # a manutenção do código.
        # def create_empty_dataset(self)
        num_linhas = len(self.dataset[alvos[0]])
        novo_dataset = {col: [] for col in self.dataset.keys()}

        for i in range(num_linhas):
            #mesma questão que poderia ter simplificado 
            # if not any(self.dataset[col][i] in [None, "", "N/A"] for col in alvos):
            tem_nulo = any(self.dataset[col][i] in [None, "", "N/A"] for col in alvos)
            if not tem_nulo:
                for col in self.dataset.keys():
                    novo_dataset[col].append(self.dataset[col][i])


        # aqui um bônus: 
            # vocês poderiam ter criado uma função que faz exatamente tudo isso, mas recebendo um parâmetro que indica se deve 
            # filtrar os nulos ou os não nulos, evitando a repetição de código e melhorando a manutenção do código.

        return novo_dataset


    def fillna(self, columns: Set[str] = None, value: Any = 0) -> Dict[str, List[Any]]:
        """
        Preenche valores nulos (None) nas colunas especificadas com um valor fixo (Any = 0).
        Modifica o dataset da classe.
        """
        #mesmo problema de validação das colunas aqui, se a validação tivesse sido feita na função _get_target_columns,
        # aqui vocês poderiam simplesmente usar o resultado sem se preocupar das colunas passadas existirem
        alvos = self._get_target_columns(columns)

        for col in alvos:
            dados = self.dataset[col] # pode acabar buscando uma chave que não existe
            for i in range(len(dados)):
                if dados[i] in [None, "", "N/A"]:
                    dados[i] = value

        return self.dataset


    def dropna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Remove as linhas que contêm valores nulos (None) nas colunas especificadas.
        Modifica o dataset da classe.
        """
        # Substitui o dataset original apenas pelas linhas sem nulos (filtrado no notna)
        # muito bom, hein? eu ia descontar a pontuação das validações das colunas aqui
        # mas como vocês usaram a função notna, gostei muito, vou deixar a pontuação completa aqui, parabéns!
        self.dataset = self.notna(columns)
        return self.dataset


class Scaler:
    """
    Aplica transformações de escala em colunas numéricas do dataset.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        # cadê a statistics aqui? 
        # precisamos da statistics para calcular a média e o desvio padrão para o standard scaler, 
        # então seria interessante ter uma instância da statistics aqui, evitando a necessidade de criar uma nova instância 
        # toda vez que for usar o standard scaler, melhorando a eficiência do código.    

    def _get_target_columns(self, columns: Set[str]) -> List[str]:
        #mesmo problema de validação das colunas aqui
        #vocês deveriam garantir se as colunas passadas realmente existem no dataset, para evitar erros de chave.
        # if columns:
        #     for col in columns:
        #         if col not in self.dataset:
        #             raise ValueError(f"Coluna '{col}' não encontrada no dataset.")
        # uma sugestão era criar essa função como uma utilitaria, assim todas as classes poderiam usar, 
        # evitando a repetição de código e melhorando a manutenção do código.

        return list(columns) if columns else list(self.dataset.keys())

    def minMax_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Aplica a normalização Min-Max ($X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}$)
        nas colunas especificadas. Modifica o dataset.
        """
        #mesmo problema de validação das colunas aqui, se a validação tivesse sido feita na função _get_target_columns,
        # aqui vocês poderiam simplesmente usar o resultado sem se preocupar das colunas passadas existirem
        alvos = self._get_target_columns(columns)

        for col in alvos:
            dados = self.dataset[col] # pode acabar buscando uma chave que não existe
            val_min = min(dados)
            val_max = max(dados)
            amplitude = val_max - val_min

            #boa a validação para evitar divisão por zero, gostei muito, parabéns!
            if amplitude == 0:
                self.dataset[col] = [0.0 for _ in dados]
                continue  # Pula para a próxima coluna

            # poderia ser simplificado:
            # self.dataset[col] = [(x - val_min) / amplitude for x in dados]

            dados_escalados = []
            for x in dados:
                x_normalizado = (x - val_min) / amplitude
                dados_escalados.append(x_normalizado)

            self.dataset[col] = dados_escalados

        return self.dataset


    def standard_scaler(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Aplica a padronização Z-score ($X_{std} = \frac{X - \mu}{\sigma}$)
        nas colunas especificadas. Modifica o dataset.

        Args:
            columns (Set[str]): Colunas para aplicar o scaler. Se vazio, tenta aplicar a todas.
        """
        #mesmo problema de validação das colunas aqui, se a validação tivesse sido feita na função _get_target_columns,
        # aqui vocês poderiam simplesmente usar o resultado sem se preocupar das colunas passadas existirem
        alvos = self._get_target_columns(columns)

        #deveria usar uma instância da statistics aqui, evitando a necessidade de criar uma nova instância 
        # toda vez que for usar o standard scaler, melhorando a eficiência do código.
        stats = Statistics(self.dataset)  # Instancia (usa a statistics) aqui para calcular média e desvio

        for col in alvos:
            dados = self.dataset[col] # pode acabar buscando uma chave que não existe
            media = stats.mean(col)
            desvio = stats.stdev(col)

            #boa a validação para evitar divisão por zero, gostei muito, parabéns!
            if desvio == 0:
                self.dataset[col] = [0.0 for _ in dados]
                continue

            # poderia ser simplificado:
            # self.dataset[col] = [(x - media) / desvio for x in dados ]
            dados_padronizados = []
            for x in dados:
                zScore = (x - media) / desvio
                dados_padronizados.append(zScore)

            self.dataset[col] = dados_padronizados

        return self.dataset


class Encoder:
    """
    Aplica codificação em colunas categóricas.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset

    def label_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:
        """
        Converte cada categoria em uma coluna em um número inteiro.
        Modifica o dataset.
        """
        #não verificam se as colunas passadas realmente existem no dataset, para evitar erros de chave.

        for col in columns:
            dados = self.dataset[col] # pode acabar buscando uma chave que não existe

            # poderia ser simplificado usando a função set e sorted:
            # categoriasUnicas = sorted(set(dados))
            categoriasUnicas = list(set(dados))
            categoriasUnicas.sort()

            # poderia ser simplificado usando um dicionário de compreensão:
            # mapaCategorias = {categoria: i for i, categoria in enumerate(categoriasUnicas)}
            mapaCategorias = {}
            for i, categoria in enumerate(categoriasUnicas):
                mapaCategorias[categoria] = i

            # poderia ser simplificado usando uma lista de compreensão:
            # dadosCodificados = [mapaCategorias[valor] for valor in dados]

            # poderia ser simplificado usando a função map:
            # dadosCodificados = [mapaCategorias[valor] for valor in dados]
            dadosCodificados = []
            for valor in dados:
                dadosCodificados.append(mapaCategorias[valor])

            #o código ficaria assim: 
            # categoriasUnicas = sorted(set(dados))
            # mapaCategorias = {categoria: i for i, categoria in enumerate(categoriasUnicas)}
            # self.dataset[col] = [mapaCategorias[valor] for valor in dados]

            self.dataset[col] = dadosCodificados

        return self.dataset


    def oneHot_encode(self, columns: Set[str]) -> Dict[str, List[Any]]:
        """
        Cria novas colunas binárias para cada categoria nas colunas especificadas (One-Hot Encoding).
        Modifica o dataset adicionando e removendo colunas.
        """
        # não verificaram se as colunas passadas realmente existem no dataset, para evitar erros de chave.

        # Converte para lista para evitar erro ao apagar colunas durante o loop
        for col in list(columns):
            dados = self.dataset[col] # pode acabar buscando uma chave que não existe
            # poderia ser simplificado usando a função set e sorted:
            # categoriasUnicas = sorted(set(dados))
            categoriasUnicas = list(set(dados))
            categoriasUnicas.sort()

            num_linhas = len(dados)

            # Cria as novas colunas preenchidas com zeros
            # poderia ser simplificado usando um dicionário de compreensão:
            # for categoria in categoriasUnicas:
            #     novaColuna = f"{col}_{categoria}"
            #     self.dataset[novaColuna] = [0 if value != categoria else 1 for value in dados]
            for categoria in categoriasUnicas:
                novaColuna = f"{col}_{categoria}"
                self.dataset[novaColuna] = [0 for _ in range(num_linhas)]

            # não precisava desse loop, já que as colunas já foram criadas preenchidas com zeros e uns
            # Coloca os '1' nas devidas colunas
            for i, valor in enumerate(dados):
                colunaAlvo = f"{col}_{valor}"
                self.dataset[colunaAlvo][i] = 1

            # Apaga a coluna original de texto
            # não precisava remover a coluna original, já que as novas colunas foram criadas com o nome da coluna original + o valor da categoria, 
            # então não teria risco de confusão entre as colunas, e manter a coluna original poderia ser útil para futuras operações de pré-processamento ou análise,
            # então seria melhor manter a coluna original
            # mas isso não é um erro, então vou deixar a pontuação com os outros cuidados aqui, parabéns!

            del self.dataset[col]

        return self.dataset


class Preprocessing:
    """
    Classe principal que orquestra as operações de pré-processamento de dados.
    Nota: Todos os métodos retornam o dicionário de dados (dataset), 
    o que encerra a possibilidade de encadeamento de métodos da classe.
    """
    def __init__(self, dataset: Dict[str, List[Any]]):
        self.dataset = dataset
        self._validate_dataset_shape()
        
        self.statistics = Statistics(self.dataset)
        self.missing_values = MissingValueProcessor(self.dataset)
        self.scaler = Scaler(self.dataset)
        self.encoder = Encoder(self.dataset)

    def _validate_dataset_shape(self):
        """
        Valida se todas as listas (colunas) no dicionário do dataset
        têm o mesmo comprimento.
        """
        if not self.dataset:
            return

        tamanhos = [len(coluna) for coluna in self.dataset.values()]
        # Transforma a lista de tamanhos num 'set', aí só pode restar 1 valor
        # Se restar mais de 1, significa que temos colunas de tamanhos diferentes
        if len(set(tamanhos)) > 1:
            raise ValueError("Erro: As colunas do dataset possuem tamanhos diferentes (linhas faltando).")

    def isna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.isna(). 
        Retorna um dicionário contendo apenas as linhas com valores nulos.
        """

        return self.missing_values.isna(columns)

    def notna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.notna(). 
        Retorna um dicionário contendo apenas as linhas sem valores nulos.
        """
        return self.missing_values.notna(columns)

    def fillna(self, columns: Set[str] = None, value: Any = 0) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.fillna(). 
        Modifica e retorna o dicionário de dados com valores preenchidos.
        """
        return self.missing_values.fillna(columns, value)

    def dropna(self, columns: Set[str] = None) -> Dict[str, List[Any]]:
        """
        Atalho para missing_values.dropna(). 
        Modifica e retorna o dicionário de dados sem as linhas nulas.
        """
        return self.missing_values.dropna(columns)

    def scale(self, columns: Set[str] = None, method: str = 'minMax') -> Dict[str, List[Any]]:
        """
        Aplica escalonamento e retorna o dicionário de dados modificado.

        Args:
            columns (Set[str]): Colunas para aplicar o escalonamento.
            method (str): O método a ser usado: 'minMax' ou 'standard'.

        Returns:
            Dict[str, List[Any]]: O dataset com as colunas escalonadas.
        """
        if method == 'minMax':
            return self.scaler.minMax_scaler(columns)
        elif method == 'standard':
            return self.scaler.standard_scaler(columns)
        else:
            raise ValueError(f"Método de escalonamento '{method}' não suportado.")

    def encode(self, columns: Set[str], method: str = 'label') -> Dict[str, List[Any]]:
        """
        Aplica codificação e retorna o dicionário de dados modificado.

        Args:
            columns (Set[str]): Colunas para aplicar a codificação.
            method (str): O método a ser usado: 'label' ou 'oneHot'.
        
        Returns:
            Dict[str, List[Any]]: O dataset com as colunas codificadas.
        """
        if method == 'label':
            return self.encoder.label_encode(columns)
        elif method == 'oneHot':
            return self.encoder.oneHot_encode(columns)
        else:
            raise ValueError(f"Método de codificação '{method}' não suportado.")