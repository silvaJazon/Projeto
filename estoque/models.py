from django.db import models
from enum import Enum


class Responsavel(models.Model):
    nome = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_ativo = models.BooleanField( null=True, blank=True, verbose_name='Está ativo?')
    data_ativacao = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Data de ativação do '
                                                                                                 'usuário')
    data_encerramento = models.DateTimeField(auto_now_add=False, blank=True, null=True,
                                                 verbose_name='Data de encerramento do '
                                                              'usuário')

    def __str__(self):
        return self.nome


class CategoriaEnum(Enum):
    FERRAMENTAS = 'Ferramentas'
    MASTROS = 'Mastros'
    BATERIAS = 'Baterias'
    ACESSORIOS = 'Acessórios'
    CABOS = 'Cabos'
    ANTENAS = 'Antenas'
    PORCAS_E_PARAFUSOS = 'Porcas e Parafusos'
    CONECTORES_PINOS_BARRAMENTOS = 'Conectores, Pinos e Barramentos'
    SENSORES = 'Sensores'
    PLACAS_E_ELETRONICOS = 'Placas e Eletrônicos'
    SUPORTE = 'Suportes'
    OUTROS = 'Outros'


class Materiais(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    quantidade_em_estoque = models.PositiveIntegerField()
    categoria = models.CharField(
        max_length=50,
        choices=[(cat.name, cat.value) for cat in CategoriaEnum],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Material em estoque'
        verbose_name_plural = 'Materiais em estoque'

    def __str__(self):
        return self.nome


class Pacote(models.Model):
    nome = models.CharField(max_length=100)
    materiais = models.ManyToManyField(Materiais, through='ItensPacote')

    def __str__(self):
        return self.nome


class ItensPacote(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE, verbose_name="Pacote")
    material = models.ForeignKey(Materiais, on_delete=models.CASCADE, verbose_name='Material')
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return 'Item:'


class EntradaMaterial(models.Model):
    material = models.ForeignKey(Materiais, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)
    remetente = models.CharField(max_length=100, null=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Registro de entrada de Material'
        verbose_name_plural = 'Registros de entradas de Materiais'

    def __str__(self):
        return f"Entrada de Material - {self.material}"


class TipoServicoEnum(Enum):
    INSTALACAO = 'Instalação'
    MANUTENCAO_PREVENTIVA = 'Manutenção Preventiva'
    MANUTENCAO_CORRETIVA = 'Manutenção Corretiva'

    @classmethod
    def choices(cls):
        return [(tipo.value, tipo.value) for tipo in cls]


class SaidaMaterial(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    data_saida = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=100, null=True)
    servico = models.CharField(max_length=100, choices=TipoServicoEnum.choices())
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Registro de saída de Material'
        verbose_name_plural = 'Registros de saídas de Materiais'

    def __str__(self):
        return f"Saida de Material do Pacote: {self.pacote} - Com destino para: {self.destino}"
