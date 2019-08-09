from import_export import resources, fields, widgets
from import_export.results import RowResult

from .models import Employe, Departement, Service, Activite, Agence, CostCenter
from Gestion_Attestations.models import Salaire


class EmployeResource(resources.ModelResource):

    matricule_paie = fields.Field(column_name='Matricule paie', attribute='matricule_paie', widget=widgets.CharWidget())
    full_name = fields.Field(column_name='Nom Prénom', attribute='full_name', widget=widgets.CharWidget())
    fonction = fields.Field(column_name='Fonction', attribute='fonction', widget=widgets.CharWidget())
    date_naissance = fields.Field(column_name='Date de naissance', attribute='date_naissance',widget=widgets.DateWidget(format('%d-%m-%Y')))
    sexe = fields.Field(column_name='Sexe', attribute='sexe', widget=widgets.CharWidget())
    adresse = fields.Field(column_name='Adresse', attribute='adresse', widget=widgets.CharWidget())
    ville = fields.Field(column_name='Ville', attribute='ville', widget=widgets.CharWidget())
    n_cin = fields.Field(column_name='N° cin', attribute='n_cin', widget=widgets.CharWidget())
    nationalite_paie = fields.Field(column_name='Nationalité paie', attribute='nationalite_paie', widget=widgets.CharWidget())
    situation_famille = fields.Field(column_name='Situation de famille', attribute='situation_famille', widget=widgets.CharWidget())
    nb_enfant = fields.Field(column_name='Nb d enfants', attribute='nb_enfant', widget=widgets.IntegerWidget())
    nb_enfant_deduction = fields.Field(column_name='Nb enf. deduction', widget=widgets.IntegerWidget())
    date_entree = fields.Field(column_name='Date d entré', attribute='date_entree', widget=widgets.DateWidget(format('%d-%m-%Y')))
    date_anciennete = fields.Field(column_name='Date d ancienneté', attribute='date_anciennete', widget=widgets.DateWidget(format('%d-%m-%Y')))
    type_base_salariale = fields.Field(column_name='Type base salariale', attribute='type_base_salariale')
    mode_reglement = fields.Field(column_name='Mode de réglement', attribute='mode_reglement', widget=widgets.CharWidget())
    type_cp = fields.Field(column_name='Type CP.', attribute='type_cp', widget=widgets.CharWidget())
    n_compte = fields.Field(column_name='N° compte', attribute='n_compte', widget=widgets.CharWidget())
    n_cnss = fields.Field(column_name='N° CNSS', attribute='n_cnss', widget=widgets.CharWidget())
    section = fields.Field(column_name='Section', attribute='section', widget=widgets.IntegerWidget())
    code_edition_comm = fields.Field(column_name='Code edition comm.', attribute='code_edition_comm',widget=widgets.IntegerWidget())
    code_agent = fields.Field(column_name='Code agent', attribute='code_agente', widget=widgets.IntegerWidget())
    date_sortie = fields.Field(column_name='Date sortie', attribute='date_sortie', widget=widgets.DateWidget(format('%d-%m-%Y')))
    superieur_hierarchique = fields.Field(column_name='Supérieur hiérarchique', attribute='superieur_hierarchique', widget=widgets.ForeignKeyWidget(Employe))
    type_contrat = fields.Field(column_name='Type de contrat', attribute='type_contrat', widget=widgets.CharWidget())
    date_fin_contrat = fields.Field(column_name='Date fin contrat', attribute='date_fin_contrat', widget=widgets.DateWidget('%d-%m-%Y'))
    commentaire = fields.Field(column_name='Commentaire', attribute='commentaire', widget=widgets.CharWidget())
    email = fields.Field(column_name='email', attribute='email', widget=widgets.CharWidget())
    agence = fields.Field(column_name='Agence', attribute='agence', widget=widgets.ForeignKeyWidget(Agence))
    service = fields.Field(column_name='Service', attribute='service', widget=widgets.ForeignKeyWidget(Service))
    department = fields.Field(column_name='Département', attribute='department', widget=widgets.ForeignKeyWidget(Departement))
    activite = fields.Field(column_name='Activité', attribute='activite', widget=widgets.ForeignKeyWidget(Activite))
    cost_center = fields.Field(column_name='Cost Center', attribute='cost_center', widget=widgets.ForeignKeyWidget(CostCenter))

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(EmployeResource, self).import_row(row, instance_loader, **kwargs)
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
        model = Employe
        import_id_fields = ('matricule_paie',)

        fields = ('matricule_paie', 'full_name',
                        'fonction', 'date_naissance', 'sexe', 'adresse', 'ville',
                        'n_cin', 'nationalite_paie', 'situation_famille', 'nb_enfant', 'nb_enfant_deduction', 'date_entree',
                        'date_anciennete', 'n_compte', 'n_cnss', 'superieur_hierarchique',
                        'type_contrat','service', 'department', 'activite', 'date_fin_contrat', 'email', 'n_compte')

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


class ServiceResource(resources.ModelResource):

    id = fields.Field(
        column_name='id',
        attribute='id',
        widget=widgets.IntegerWidget()
    )

    nom_service = fields.Field(
        column_name='nom_service',
        attribute='nom_service',
        widget=widgets.CharWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ServiceResource, self).import_row(row, instance_loader, **kwargs)
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
        model = Service
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('id',)
        fields = ('id', 'nom_service')


class CostCenterResource(resources.ModelResource):

    id = fields.Field(
        column_name='id',
        attribute='id',
        widget=widgets.IntegerWidget()
    )

    nom_cost_center = fields.Field(
        column_name='nom_cost_center',
        attribute='nom_cost_center',
        widget=widgets.CharWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(CostCenterResource, self).import_row(row, instance_loader, **kwargs)
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
        model = CostCenter
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('id',)
        fields = ('id', 'nom_cost_center')


class DepartmentResource(resources.ModelResource):

    id = fields.Field(
        column_name='id',
        attribute='id',
        widget=widgets.IntegerWidget()
    )

    nom_departement = fields.Field(
        column_name='nom_departement',
        attribute='nom_departement',
        widget=widgets.CharWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(DepartmentResource, self).import_row(row, instance_loader, **kwargs)
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
        model = Departement
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('id',)
        fields = ('id', 'nom_departement')

class AgenceResource(resources.ModelResource):

    id = fields.Field(
        column_name='id',
        attribute='id',
        widget=widgets.IntegerWidget()
    )

    nom_agence = fields.Field(
        column_name='nom_agence',
        attribute='nom_agence',
        widget=widgets.CharWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(AgenceResource, self).import_row(row, instance_loader, **kwargs)
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
        model = Agence
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('id',)
        fields = ('id', 'nom_agence')

class ActiviteResource(resources.ModelResource):

    id = fields.Field(
        column_name='id',
        attribute='id',
        widget=widgets.IntegerWidget()
    )

    nom_activite = fields.Field(
        column_name='nom_activite',
        attribute='nom_activite',
        widget=widgets.CharWidget()
    )

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ActiviteResource, self).import_row(row, instance_loader, **kwargs)
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
        model = Activite
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ('id',)
        fields = ('id', 'nom_activite')
