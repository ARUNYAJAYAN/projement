import pandas as pd


def export_project_data(data):
    df = pd.DataFrame(data)
    df.to_excel('project.xls', index=False)
    file = pd.read_excel('project.xls')
    return file