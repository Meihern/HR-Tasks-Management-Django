from import_export import resources, fields, widgets
from import_export.results import RowResult

from Authentification.models import Employe
from Gestion_Conge.models import SoldeConge


class SoldeCongeResource(resources.ModelResource):
    solde = fields.Field(
        column_name='solde',
        attribute='solde',
        widget=widgets.ForeignKeyWidget(Employe)
    )

    matricule_paie = fields.Field(
        column_name='Matricule',
        attribute='matricule_paie',
        widget=widgets.ForeignKeyWidget(Employe)
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(SoldeCongeResource, self).import_row(row, instance_loader, **kwargs)
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
        model = SoldeConge
        skip_unchanged = True
        report_skipped = False
        raise_errors = False
        import_id_fields = ('matricule_paie',)
        fields = ('matricule_paie', 'solde')
