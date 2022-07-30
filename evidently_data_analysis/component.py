import lightning as L
import pandas as pd
from evidently.dashboard import Dashboard
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab, NumTargetDriftTab


class EvidentlyDataAnalysis(L.LightningWork):
    def __init__(self, train_dataframe_path=None, test_dataframe_path=None, target_column_name=None, task_type='classification') -> None:
        super().__init__()
        self.train_dataframe_path = train_dataframe_path
        self.test_dataframe_path = test_dataframe_path
        self.target_column = target_column_name
        self.task_type = task_type
        self.report_path = None

        self.supported_task_types = ['classification', 'regression']

        if self.task_type not in self.supported_task_types:
            raise Exception(f'task_type must be {",".join(self.supported_task_types)}')



    def run(self):
        col_map = ColumnMapping()
        col_map.target = self.target_column
        train_df = pd.read_csv(self.train_dataframe_path)
        test_df = pd.read_csv(self.test_dataframe_path)
        train_df.reset_index(drop=True, inplace=True)
        train_df.reset_index(drop=True, inplace=True)
        test_df.reset_index(drop=True, inplace=True)

        
        tabs = [DataDriftTab(verbose_level=0)]
        if self.task_type == 'classification':
            tabs.append(CatTargetDriftTab(verbose_level=0))
        else:
            tabs.append(NumTargetDriftTab(verbose_level=0))
        data_and_target_drift_dashboard = Dashboard(tabs=tabs)
        data_and_target_drift_dashboard.calculate(train_df, test_df, column_mapping=col_map)
        data_and_target_drift_dashboard.save('./data_and_target_drift.html')
        self.report_path = './data_and_target_drift.html'