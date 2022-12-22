import pandas as pd

file = pd.read_excel("Вычисление параметров маятника от 2022.09.23.xlsx", usecols=["Время, сек",
                                                                                   "Rz_L, Н",
                                                                                   "Rz_R, Н",
                                                                                   "Rx, Н"])
file.to_csv("import_file.csv", encoding="UTF-8")