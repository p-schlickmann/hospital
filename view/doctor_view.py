from .base_view import BaseView


class DoctorView(BaseView):
    def __init__(self):
        super().__init__()

    def display_options(self):
        """
        Displays system options
        :return: chosen option
        """
        self.display_header('Médicos')
        print("1 - Cadastrar médico")
        print("2 - Alterar médico")
        print("3 - Buscar médico")
        print("4 - Excluir médico")
        print("5 - Listar médicos de plantão")
        print("6 - Chamar médico")
        print("0 - Voltar ao menu principal")
        chosen_option = input("Digite o número da opção desejada: ")
        return self.read_whole_number(chosen_option, {0, 1, 2, 3, 4, 5, 6})

    def open(self):
        pass

    def close(self):
        pass

    def display_register_doctor(self):
        name, phone, birth = self.ask_for_main_info()
        salary = self.read_whole_number(input('Salário anual (apenas números): '))
        return name, phone, birth, salary

    def display_edit_doctor(self, doctor):
        print('[+] Pressione `Enter` para pular.')
        name = input(f'Nome [{doctor.name}]: ')
        cpf = input(f'CPF [{doctor.cpf}]: ')
        phone = input(f'Celular [{doctor.phone_number}]: ')
        birth = input(f'Data de nascimento [{doctor.date_of_birth}]: ')
        salary = input(f'Salário [{doctor.salary}]: ')
        available = input(f'Disponível [{"sim" if doctor.available else "nao"}](s/N): ')
        on_call = input(f'De plantão [{"sim" if doctor.on_call else "nao"}](s/N): ')
        return cpf, name, phone, birth, salary, available, on_call

    def list_on_call_doctors(self, doctors):
        if not doctors:
            self.display_msg('[!] Nenhum médico está de plantão!')
        for doctor in doctors:
            print(doctor)

    def list_available_doctors_to_call(self, on_call_doctors, doctors):
        """
        Lists available doctors to call and lets the user choose one
        :param on_call_doctors: List of on call doctors
        :param doctors: List of available doctors, but not on call
        :return: chosen doctor
        """
        joined_doctors = list(set(on_call_doctors + doctors))
        for i, doctor in enumerate(joined_doctors):
            print(f'[{i + 1}] {doctor.name}', ' - PLANTÃO' if doctor in on_call_doctors else '')
        chosen_doctor = input('Digite o número do lado do nome do médico que você deseja chamar: ')
        possible_doctors_indexes = {idx + 1 for idx, doc in enumerate(joined_doctors)}
        chosen_doctor_index = self.read_whole_number(chosen_doctor, possible_doctors_indexes)
        if chosen_doctor_index:
            return joined_doctors[chosen_doctor_index - 1]

