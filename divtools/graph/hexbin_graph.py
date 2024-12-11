import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

from typing import List


def draw_hexbin(x_name: str, y_name: str, data: List) -> None:
    df_data = pd.DataFrame(data, columns=[x_name, y_name])

    # Hexbin图

    sns.jointplot(x=x_name, y=y_name, data=df_data, kind='hex')
    df_data.plot.hexbin(x=x_name, y=y_name, gridsize=25)
    plt.show()
