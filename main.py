import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

const = {"g": 9.81, "p": 998, "V": 0.4,
         "m_c": 3050, "h_c": 0.5, "L": 2,
         "m_liq": 1302, "V_liq_st": 1.044,
         "h_liq_st": 0.18, "V_liq_move": 0.261}
const['m_liq_st'] = const['p'] * const["V_liq_st"]
const['m_liq_move'] = const['p'] * const["V_liq_move"]
check_data = {}
check_data['m_syst'] = const['m_c']+const['m_liq_move']+const['m_liq_st']
check_data['R_st'] = check_data['m_syst']+const['g']/2

class Data():
    def __init__(self, file):
        self.data = pd.read_csv(file)
        self.data = self.data.rename(columns={"Время, сек": "time",
                                              "Rz_L, Н": "Rz_L",
                                              "Rz_R, Н": "Rz_R",
                                              "Rx, Н": "Rx"})


def frequency(data: pd.DataFrame):
    dim = True
    change_point = []
    for i in range(len(data) - 1):
        if (data["Rz_L"].loc[i] < data["Rz_L"].loc[i + 1] and dim) \
                or (data["Rz_L"].loc[i] > data["Rz_L"].loc[i + 1] and dim == False):
            change_point.append(data["time"][i])
            dim = not dim
    return change_point


def main():
    data = Data("import_file.csv")
    data.data.hist
    data.data.loc[2:].plot(x="time", y=["Rz_L", "Rz_R"])
    # print(len(frequency(data.data)))
    # plt.show()
    # print(data.data.groupby(["Rz_R", "Rz_L"]).agg("count").loc[data.data.groupby(["Rz_R", "Rz_L"]).agg("count").time>1])
    print(data.data.Rz_L/data.data.Rz_L.max())

if __name__ == '__main__':
    main()
