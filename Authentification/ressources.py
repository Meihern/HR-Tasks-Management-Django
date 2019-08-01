from import_export import resources, fields, widgets
from import_export.results import RowResult

from .models import Employe, Salaire


class EmployeResource(resources.ModelResource):

    date_naissance = fields.Field(
        column_name='date_naissance',
        attribute='date_naissance',
        widget=widgets.DateWidget(format('%d-%m-%Y'))
    )
    date_entree = fields.Field(
        column_name='date_entree',
        attribute='date_entree',
        widget=widgets.DateWidget(format('%d-%m-%Y'))
    )
    date_anciennete = fields.Field(
        column_name='date_anciennete',
        attribute='date_anciennete',
        widget=widgets.DateWidget(format('%d-%m-%Y'))
    )
    date_sortie = fields.Field(
        column_name='date_sortie',
        attribute='date_sortie',
        widget=widgets.DateWidget(format('%d-%m-%Y'))
    )


    class Meta:
        model = Employe
        import_id_fields = ('matricule_paie',)
        fields = ('password', 'matricule_paie', 'last_name', 'first_name',
                        'fonction', 'date_naissance', 'sexe', 'adresse', 'ville',
                        'n_cin', 'nationalite_paie', 'situation_famille', 'date_entree',
                        'date_anciennete', 'n_cnss', 'date_sortie', 'superieur_hierarchique',
                        'type_contrat', 'date_fin_contrat', 'email', 'n_compte')
        #exclude = ('active', 'staff', 'admin', 'last_login')
        '''
        import_order = ('password', 'matricule_paie', 'last_name', 'first_name',
                        'fonction', 'date_naissance', 'sexe', 'adresse', 'ville',
                        'n_cin', 'nationalite_paie', 'situation_famille', 'date_entree',
                        'date_anciennete', 'n_cnss', 'date_sortie', 'superieur_hierarchique',
                        'type_contrat', 'date_fin_contrat', 'email', 'n_compte')
        '''

        #import_order = ('matricule_paie', 'last_name', 'first_name', 'fonction', 'email')


class SalaireResource(resources.ModelResource):

    matricule_paie = fields.Field(
        column_name='matricule_paie',
        attribute='matricule_paie',
        widget=widgets.ForeignKeyWidget(Employe)
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

