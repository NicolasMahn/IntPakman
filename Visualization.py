import matplotlib.pyplot as plt


def data_details(data):
    data.info()
    data.weight_in_g.describe()
    data.length_cm.describe()
    data.height_cm.describe()
    data.width_cm.describe()
    data.volume.describe()


def plot_data_overview(data, column):
    fig = plt.figure()
    plt.scatter(data["Sendungsnummer"], data[column])
    plt.title('Overview of ' + str(column))
    fig.show()
