from django.db import models
from enum import Enum
from django.utils import timezone


class UnidadeArm(models.Model):
    nome = models.CharField(max_length=50, unique=True, null=True)
    responsavel = models.CharField(max_length=50, unique=True, null=True)
    is_ativo = models.BooleanField(null=True, verbose_name='Está ativa?')
    data_ativacao = models.DateTimeField(auto_now_add=False, null=True,
                                         verbose_name='Data de ativação da Unidade de Armazenamento')
    data_encerramento = models.DateTimeField(auto_now_add=False, null=True, blank=True,
                                             verbose_name='Data de encerramento da Unidade de Armazenamento')

    class Meta:
        verbose_name = 'Unidade de Armazenamento'
        verbose_name_plural = 'Unidades de Armazenamento'

    def __str__(self):
        return f'{self.nome}'

    def save(self, *args, **kwargs):
        if self.data_encerramento and timezone.now() > self.data_encerramento:
            self.is_ativo = False
        super().save(*args, **kwargs)


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


class Material(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(
        max_length=50,
        choices=[(cat.name, cat.value) for cat in CategoriaEnum],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Cadastro de Material'
        verbose_name_plural = 'Cadastro de Materiais'

    def __str__(self):
        return self.nome


class QuantidadeMaterialPorUnidade(models.Model):
    unidade = models.ForeignKey(UnidadeArm, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade_em_estoque = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoque'

    def __str__(self):
        return f'{self.quantidade_em_estoque}'


class Pacote(models.Model):
    nome = models.CharField(max_length=100)
    materiais = models.ManyToManyField(Material, through='ItensPacote')

    def __str__(self):
        return self.nome


class ItensPacote(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE, verbose_name="Pacote")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return 'Item:'


class EntradaMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_entrada = models.DateTimeField(auto_now_add=True)
    remetente = models.CharField(max_length=100, null=True)
    destino = models.ForeignKey(UnidadeArm, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Externo - Entrada de Material'
        verbose_name_plural = 'Externo - Entradas de Materiais'

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
    unidade_debito = models.ForeignKey(UnidadeArm, on_delete=models.CASCADE, null=True)
    destino = models.CharField(max_length=100, null=True)  # Mudar para Farm
    servico = models.CharField(max_length=100, choices=TipoServicoEnum.choices())

    class Meta:
        verbose_name = 'Externo - Saída de Material'
        verbose_name_plural = 'Externo - Saídas de Materiais'

    def __str__(self):
        return f"Saida de Material do Pacote: {self.pacote} Com destino para: {self.destino} - " \
               f"Debitado da unidade: {self.unidade_debito} "


class TransferenciaInterna(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    data_saida = models.DateTimeField(auto_now_add=True, verbose_name='Data de saida da unidade remetente')
    unidade_debito = models.ForeignKey(UnidadeArm, on_delete=models.CASCADE, null=True,related_name="transferencia_debito")
    unidade_credito = models.ForeignKey(UnidadeArm, on_delete=models.CASCADE, null=True,related_name="transferencia_credito")
    data_entrada = models.DateTimeField(auto_now_add=False,blank=True, null=True, verbose_name='Data de entrada na unidade de destino')
    entregue = models.BooleanField(null=True, verbose_name='Foi entregue a unidade de destino?')

    class Meta:
        verbose_name = 'Transferência interna de Material'
        verbose_name_plural = 'Transferências internas de Materiais'

    def __str__(self):
        return f"Transferência interna do Pacote: {self.pacote} Com destino para: {self.unidade_credito} - " \
               f"Debitado da unidade: {self.unidade_debito} "

    def save(self, *args, **kwargs):
        if self.data_entrada:
            self.entregue = True
        else:
            self.entregue = False
        super().save(*args, **kwargs)