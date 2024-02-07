from django.contrib import admin
from django import forms
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from .models import Material, Pacote, ItensPacote, SaidaMaterial, EntradaMaterial, UnidadeArm, \
    QuantidadeMaterialPorUnidade


class QuantidadeMaterialPorUnidadeAdmin(admin.ModelAdmin):
    list_display = ['unidade', 'material', 'quantidade_em_estoque']
    list_filter = ['unidade', 'material']
    ordering = ['material']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QtnUndInLine(admin.TabularInline):
    model = QuantidadeMaterialPorUnidade
    extra = 0
    readonly_fields = ['unidade', 'material', 'quantidade_em_estoque']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UnidadeArmAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel', 'is_ativo', 'data_ativacao', 'data_encerramento']
    # inlines = [QtnUndInLine]


class ItensPacoteInline(admin.TabularInline):
    model = ItensPacote


class PacoteAdmin(admin.ModelAdmin):
    inlines = [ItensPacoteInline]


class MateriaisAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria']
    ordering = ['nome']
    list_filter = ['categoria']


class EntradaMaterialAdminForm(forms.ModelForm):
    class Meta:
        model = EntradaMaterial
        fields = '__all__'


class EntradaMaterialAdmin(admin.ModelAdmin):
    list_display = ['material', 'quantidade', 'data_entrada', 'remetente', 'destino']
    form = EntradaMaterialAdminForm
    list_filter = ['material__categoria', 'data_entrada', 'remetente']

    def save_model(self, request, obj, form, change):
        material = obj.material
        quantidade_entrada = obj.quantidade
        unidade_destino = obj.destino

        if unidade_destino:
            # Adicione a quantidade de entrada ao estoque do material para a unidade de destino
            qnt_unidade, created = QuantidadeMaterialPorUnidade.objects.get_or_create(unidade=unidade_destino,
                                                                                      material=material)

            if not qnt_unidade.quantidade_em_estoque:
                qnt_unidade.quantidade_em_estoque = 0

            qnt_unidade.quantidade_em_estoque += quantidade_entrada
            qnt_unidade.save()

        super().save_model(request, obj, form, change)


class SaidaMaterialAdminForm(forms.ModelForm):
    class Meta:
        model = SaidaMaterial
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        pacote = cleaned_data.get('pacote')
        unidade_debito = cleaned_data.get('unidade_debito')  # Corrigindo aqui

        for item in pacote.itenspacote_set.all():
            material = item.material
            quantidade_saida = item.quantidade

            try:
                qnt_unidade = QuantidadeMaterialPorUnidade.objects.get(unidade=unidade_debito, material=material)
            except QuantidadeMaterialPorUnidade.DoesNotExist:
                msg = f"Material {material.nome} não existe na unidade de débito {unidade_debito.nome}."
                self.add_error(None, msg)
                break

            if qnt_unidade and qnt_unidade.quantidade_em_estoque < quantidade_saida:
                msg = f"Quantidade insuficiente em estoque para {material.nome} na unidade de débito."
                self.add_error(None, msg)


class SaidaMaterialAdmin(admin.ModelAdmin):
    list_display = ['pacote', 'data_saida', 'destino', 'servico', 'unidade_debito']
    form = SaidaMaterialAdminForm

    def save_model(self, request, obj, form, change):
        pacote = obj.pacote
        unidade_debito = obj.unidade_debito
        transacao_bem_sucedida = True

        for item in pacote.itenspacote_set.all():
            material = item.material
            quantidade_saida = item.quantidade

            try:
                qnt_unidade = QuantidadeMaterialPorUnidade.objects.get(unidade=unidade_debito, material=material)
            except QuantidadeMaterialPorUnidade.DoesNotExist:
                # Lidar com a exceção aqui, por exemplo, criando um novo objeto ou exibindo uma mensagem de erro.
                msg = f"Material {material.nome} não existe na unidade de débito {unidade_debito.nome}."
                form.add_error(None, msg)
                transacao_bem_sucedida = False
                break

            if qnt_unidade and qnt_unidade.quantidade_em_estoque >= quantidade_saida:
                qnt_unidade.quantidade_em_estoque -= quantidade_saida
                qnt_unidade.save()
            elif qnt_unidade:
                msg = f"Quantidade insuficiente em estoque para {material.nome} na unidade de débito."
                form.add_error(None, msg)
                transacao_bem_sucedida = False
                break
            else:
                # Lidar com o caso onde qnt_unidade é None (exceção ocorreu)
                msg = f"Erro ao obter quantidade para {material.nome} na unidade de débito {unidade_debito.nome}."
                form.add_error(None, msg)
                transacao_bem_sucedida = False
                break

        if transacao_bem_sucedida:
            super().save_model(request, obj, form, change)
        else:
            form.add_error(None, "A transação de saída não foi concluída com sucesso.")


admin.site.register(QuantidadeMaterialPorUnidade, QuantidadeMaterialPorUnidadeAdmin)
admin.site.register(Material, MateriaisAdmin)
admin.site.register(Pacote, PacoteAdmin)
admin.site.register(EntradaMaterial, EntradaMaterialAdmin)
admin.site.register(SaidaMaterial, SaidaMaterialAdmin)
admin.site.register(UnidadeArm, UnidadeArmAdmin)
