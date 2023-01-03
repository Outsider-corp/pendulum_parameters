import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

# Создание списка для сохранения промежуточных расчётов
calculations = []


# Функция для записи значения, единицы измерения и описания
# в список calculation
def write_calcs(value, unit, description):
    calculations.append([f'{value} {unit}', description])
    return


# Создание словаря с постоянными переменными
const = {"g": 9.81, "p": 998, "V": 0.4, "m_c": 3050,
         "h_c": 0.5, "L": 2, "V_liq_st": 1.044,
         "h_liq_st": 0.18, "V_liq_move": 0.261,
         "fi_0": 0, "fi": np.radians(10)}
const['m_liq_st'] = const['p'] * const["V_liq_st"]
write_calcs(const['m_liq_st'], "кг", "Масса неподвижной жидкости")
const['m_liq_move'] = const['p'] * const["V_liq_move"]
write_calcs(const['m_liq_move'], "кг", "Масса подвижной жидкости")


# Создание класса, который хранит данные измерений
class Data():
    def __init__(self, file):
        self.data = pd.read_csv(file)
        # Переименование столбцов для более удобной работы
        self.data = self.data.rename(columns={"Время, сек": "time",
                                              "Rz_L, Н": "Rz_L",
                                              "Rz_R, Н": "Rz_R",
                                              "Rx, Н": "Rx"})

    # Метод для фильтрации данных с нужной частотой
    def filter(self, cutoff):
        T = self.data.time.max()
        fs = self.data.time.count() / T
        nyq = fs / 2
        order = 2
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        self.data.Rz_R = pd.Series(filtfilt(b, a, self.data.Rz_R))
        self.data.Rz_L = pd.Series(filtfilt(b, a, self.data.Rz_L))
        self.data.Rx = pd.Series(filtfilt(b, a, self.data.Rx))
        return

    # Метод для нахождения частоты колебаний
    def find_fs(self):
        # Нахождение разницы между реакциями в левой и правой опорах
        self.data['Rz_diff'] = self.data.Rz_L - self.data.Rz_R
        balance_state = []
        # Поиск строк, когда реакция одной опоры начинает превышать
        # реакцию другой
        for i in range(self.data.Rz_diff.count() - 1):
            if self.data.Rz_diff[i] * self.data.Rz_diff[i + 1] < 0:
                balance_state.append(i)
        # Вычисление частоты колебаний для последнего колебания
        fs = 1 / (self.data.time[balance_state[-1]] \
                  - self.data.time[balance_state[-3]])
        fs = round(fs, 2)
        return fs


def main():
    data = Data("import_file.csv")
    data.filter(10)  # Фильтр данных в диапазоне от 0 до 10 Гц
    fs = data.find_fs()  # Нахождение частоты колебаний маятника
    write_calcs(fs, "Гц", "Частота колебаний свободной"
                          " поверхности жидкости")
    w1 = 2 * np.pi * fs  # Вычисление циклической частоты маятника
    w1 = round(w1, 2)
    write_calcs(w1, "рад/сек", "Циклическая частота колебаний "
                               "свободной поверхности жидкости")
    l_pend = const["g"] / pow(w1, 2)  # Вычисление длины подвеса
    l_pend = round(l_pend, 2)
    write_calcs(l_pend, "м", "Длина подвеса математического маятника")

    Rz_L = 20466.50
    Rz_R = 21997.10
    Rx = 650
    # Вычисление веса маятника
    G = Rx / (pow(const["V"], 2) / const["g"] / l_pend \
              + 3 * np.cos(const['fi']) - 2 * np.cos(const['fi_0'])) \
        / np.sin(const['fi'])
    G = round(G, 2)
    write_calcs(G, "Н", "Вес маятника")
    m_pend = G / const['g']  # Вычисление массы маятника
    m_pend = round(m_pend, 2)
    write_calcs(m_pend, "кг", "Масса маятника")
    # Вычисление момента, образуемого из-за смещения жидкости
    M_liq = np.abs(Rz_R - Rz_L) * const['L'] - const['m_liq_st'] \
            * const['h_liq_st'] - const['m_c'] * const['h_c']
    M_liq = round(M_liq, 2)
    write_calcs(M_liq, "Н*м", "Момент, образуемый из-за смещения жидкости")
    # Вычисление высоты подвеса маятника
    H_pend = M_liq / Rx
    H_pend = round(H_pend, 2)
    write_calcs(H_pend, "м", "Высота подвеса математического маятника")
    # Запись параметров маятника в DataFrame
    result = pd.DataFrame(data={"Масса маятника": [m_pend],
                                "Длина подвеса маятника": [l_pend],
                                "Высота подвеса": [H_pend]})
    # Запись параметров маятника в файл формата .csv
    result.to_csv('result_file.csv', encoding="UTF-8", index=False)
    # Запись промежуточных вычислений в DataFrame
    calcs = pd.DataFrame(data=calculations,
                         columns=['Значение, размерность', 'Описание'])
    # Запись промежуточных вычислений в файл формата .csv
    calcs.to_csv('calculations.csv', encoding="UTF-8", index=False)


if __name__ == '__main__':
    main()
