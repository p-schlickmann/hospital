from .base_view import BaseView


class DoctorView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        print("-------- Hospital Mendes ---------")
        print("------------ Médicos -------------")
        print("1 - Cadastrar médico")
        print("2 - Alterar médico")
        print("3 - Buscar médico")
        print("4 - Excluir médico")
        print("5 - Listar médicos de plantão")
        print("6 - Chamar médico")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4, 5, 6})

    def display_register_doctor(self, cpf):
        info = self.ask_for_main_info()
        info['cpf'] = cpf
        info['salary'] = self.read_whole_number(input('Salário anual (apenas números): '))

    def display_edit_doctor(self, doctor):
        pass

    @staticmethod
    def list_on_call_doctors(doctors):
        print("-------- Hospital Mendes ---------")
        print("------- Médicos de plantão -------")
        for doctor in doctors:
            print(doctor)

    def list_available_doctors_to_call(self, on_call_doctors, doctors):
        """
        Lists available doctors to call and lets the user choose one
        :param on_call_doctors: List of on call doctors
        :param doctors: List of available doctors, but not on call
        :return: chosen doctor
        """
        print("-------- Hospital Mendes ---------")
        print("------- Médicos disponíveis ------")
        joined_doctors = set(on_call_doctors + doctors)
        for i, doctor in enumerate(joined_doctors):
            print(f'[{i}] {doctor}', ' - PLANTÃO' if doctor in on_call_doctors else '')
        chosen_doctor = input('Digite o número do lado do nome do médico que você deseja ligar: ')
        possible_doctors_indexes = set([_ + 1 for _ in range(len(joined_doctors))])
        chosen_doctor_index = self.read_whole_number(chosen_doctor, possible_doctors_indexes) + 1
        return list(joined_doctors)[chosen_doctor_index]
