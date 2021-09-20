from data.data_access_object import DataAccessObject


class PatientDAO(DataAccessObject):
    def __init__(self, datasource, instance):
        super().__init__(datasource, instance)

    def edit_current_patient(self, key, patient):
        *previous_admittions, _ = self.get(key)
        self.add(key, previous_admittions + [patient], force_insert=True)

