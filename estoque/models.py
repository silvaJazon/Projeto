from django.db import models
from enum import Enum


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Categoria do material'
        verbose_name_plural = 'Categoria dos materiais'

    def __str__(self):
        return self.nome


class Materiais(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    quantidade_em_estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)

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
        return [(key.value, key.value) for key in cls]


class SaidaMaterial(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    data_saida = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=100, null=True)
    servico = models.CharField(max_length=100, choices=TipoServicoEnum.choices())

    class Meta:
        verbose_name = 'Registro de saída de Material'
        verbose_name_plural = 'Registros de saídas de Materiais'

    def __str__(self):
        return f"Saida de Material do Pacote: {self.pacote} - Com destino para: {self.destino}"
