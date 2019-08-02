from import_export import resources, fields, widgets
from import_export.results import RowResult

from .models import Employe
from Gestion_Attestations.models import Salaire


class EmployeResource(resources.ModelResource):

    date_naissance = fields.Field(column_name='Date de naissance', attribute='date_naissance',widget=widgets.DateWidget(format('%d-%m-%Y')))
    date_entree = fields.Field(column_name='Date d entré', attribute='date_entree', widget=widgets.DateWidget(format('%d-%m-%Y')))
    date_anciennete = fields.Field(column_name='Date d ancienneté', attribute='date_anciennete', widget=widgets.DateWidget(format('%d-%m-%Y')))
    date_sortie = fields.Field(column_name='Date sortie', attribute='date_sortie', widget=widgets.DateWidget(format('%d-%m-%Y')))
    matricule_paie = fields.Field(column_name='Matricule paie', attribute='matricule_paie', widget=widgets.CharWidget())
    full_name = fields.Field(column_name='Nom Prénom', attribute='full_name', widget=widgets.CharWidget())
    fonction = fields.Field(column_name='Fonction', attribute='fonction', widget=widgets.CharWidget())
    sexe =  fields.Field(column_name='Sexe', attribute='sexe', widget=widgets.CharWidget())
    adresse = fields.Field(column_name='Adresse', attribute='adresse', widget=widgets.CharWidget())
    ville = fields.Field(column_name='Ville', attribute='ville', widget=widgets.CharWidget())
    n_cin = fields.Field(column_name='N° cin', attribute='n_cin', widget=widgets.CharWidget())
    nationalite_paie = fields.Field(column_name='Nationalité paie',attribute='nationalite_paie', widget=widgets.CharWidget())
    situation_famille = fields.Field(column_name='Situation de famille', attribute='situation_famille', widget=widgets.CharWidget())
    n_compte = fields.Field(column_name='N° compte', attribute='n_compte', widget=widgets.CharWidget())
    n_cnss = fields.Field(column_name='N° CNSS', attribute='n_cnss', widget=widgets.CharWidget())
    superieur_hierarchique = fields.Field(column_name='Supérieur hierarchiq', attribute='superieur_hierarchique', widget=widgets.ForeignKeyWidget(Employe))
    type_contrat = fields.Field(column_name='Type de contrat', attribute='type_contrat', widget=widgets.CharWidget())
    date_fin_contrat = fields.Field(column_name='Date fin contrat', attribute='date_fin_contrat', widget=widgets.CharWidget())
    email = fields.Field(column_name='email', attribute='email', widget=widgets.CharWidget())


    class Meta:
        model = Employe
        import_id_fields = ('matricule_paie',)
        fields = ('matricule_paie', 'full_name',
                        'fonction', 'date_naissance', 'sexe', 'adresse', 'ville',
                        'n_cin', 'nationalite_paie', 'situation_famille', 'date_entree',
                        'date_anciennete', 'n_cnss', 'date_sortie', 'superieur_hierarchique',
                        'type_contrat', 'date_fin_contrat', 'email', 'n_compte')
        #exclude = ('active', 'staff', 'admin', 'last_login')

        #import_order = ('matricule_paie', 'last_name', 'first_name', 'fonction', 'email')


class SalaireResource(resources.ModelResource):

    matricule_paie = fields.Field(
        column_name='Matricule',
        attribute='matricule_paie',
        widget=widgets.ForeignKeyWidget(Employe)
    )

    valeur_brute = fields.Field(
        column_name='299 Brut',
        attribute='valeur_brute',
        widget=widgets.IntegerWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(SalaireResource, self).import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            # Add a column with the error message
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result

    class Meta:
        model = Salaire
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('matricule_paie',)
        fields = ('matricule_paie', 'valeur_brute')

