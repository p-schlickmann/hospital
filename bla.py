from datetime import datetime, timedelta
from random import randint

line = []


class Patient:
    def __init__(self, nome, arrived_at):
        self.nome = nome
        self.arrived_at = arrived_at

    def __str__(self):
        return self.nome
        

def add_patient_to_line(line, patient, illness_severity):
    """
    Adds patient to patient line based on illness severity, that can vary from 0 to 5.
    Patient arrival time is used as a tie breaker
    :param patient: Patient instance
    :param illness_severity: random integer between 0 to 5
    :return: None
    """
    passed_line = line
    patient_to_be_appended = {'patient': patient, 'severity': illness_severity, 'nome':patient.__str__()}
    if not passed_line:
        passed_line.append(patient_to_be_appended)
    else:
        first_patient = passed_line[0]
        if first_patient['severity'] < illness_severity:
            passed_line = [patient_to_be_appended] + passed_line
        else:
            indexes_of_patients_with_the_same_severity = [
                index for index, patient in enumerate(passed_line) if patient['severity'] == illness_severity
            ]
            if not indexes_of_patients_with_the_same_severity:
                # find the first patient in passed_line that has a lower severity then passed patient
                try:
                    index_of_the_first_patient_with_less_severity = [
                        index for index, patient in enumerate(passed_line) if patient['severity'] < illness_severity
                    ][0]
                    cutting_point = index_of_the_first_patient_with_less_severity - 1
                    passed_line = passed_line[0:cutting_point] + [patient_to_be_appended] + passed_line[cutting_point:]
                except IndexError:
                    # no patient with less severity then this one
                    passed_line.append(patient_to_be_appended)
            else:
                # tie break based on arrival time
                for patient_index in indexes_of_patients_with_the_same_severity:
                    found_patient = passed_line[patient_index]
                    if found_patient['patient'].arrived_at < patient.arrived_at:
                        # if found patient arrived earlier then we did,
                        # check if the next patient with the same severity arrived after we did
                        # if both are true, append the patient between them
                        try:
                            next_patient_in_passed_line = passed_line[patient_index + 1]
                            if next_patient_in_passed_line['severity'] != illness_severity:
                                raise IndexError
                        except IndexError:
                            # there was no patient with the same severity further down the passed_line,
                            # so we can append this new patient right after this last one
                            cutting_point = patient_index + 1
                            passed_line = passed_line[0:cutting_point] + [patient_to_be_appended] + passed_line[
                                                                                                 cutting_point:]
                            break
                        else:
                            # there was a next patient in passed_line with the same severity
                            # now if this patient arrived after this one, we should append this one before him.
                            if next_patient_in_passed_line['patient'].arrived_at > patient.arrived_at:
                                cutting_point = patient_index + 1
                                passed_line = passed_line[0:cutting_point] + [patient_to_be_appended] + passed_line[cutting_point:]
                                break
    return passed_line


while True:
    delay = input('delay em minutos: ')
    sev = input('sev: ')
    nome = str(input('nome:' ))
    p = Patient(nome, datetime.now() - timedelta(minutes=int(delay)))
    line = add_patient_to_line(line, p, int(sev))
    print(line)
