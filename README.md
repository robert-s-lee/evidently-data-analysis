# evidently_data_analysis component - WIP

This ⚡ [Lightning component](lightning.ai) ⚡ was generated automatically with:

```bash
lightning init component evidently_data_analysis
```

## Note
It takes some time for the output to be generated and visible in the browser. Try and refresh a couple of times in the browser to see the output.

## What problem is this component solving?
After doing a train-test split of our dataset which is to be used for modelling or to compare the data distributions of training data vs incoming data in production(test data), this component helps analyse the data trends and any drifts detected in the train and test sets. In simple words, it gives us a visual analysis to verify if our train and test sets have somewhat similar distributions or not and if they vary then by what degree.

This component uses Evidently AI to facilitate this data drift detection which is one of the crucial steps in the whole ML development lifecycle.

This is made primarily for tabular dataset analysis and currently supported tasks are classification or regression.

This must be done before jumping into modeling and the app can be extended to include the training along with the model prediction analysis too (Evidently AI helps for model prediction analysis as well)

Stop looking at bland numbers which make limited sense, give the visualization a shot.

## To run evidently_data_analysis

First, install evidently_data_analysis (warning: this component has not been officially approved on the lightning gallery):

```bash
lightning install component https://github.com/Nachimak28/evidently-data-analysis
```

If the above does not work, manually setup the environment:

```bash
git clone https://github.com/Nachimak28/evidently-data-analysis
cd evidently-data-analysis
conda create --yes --name evidently python=3.8
conda activate evidently
python -m pip install -r requirements.txt
python -m pip install lightning
python -m lightning run app app.py
python -m lightning run app app.py --cloud
```

Once the app is installed, use it in an app:

Example #1 - Passing data during initialization

```python

import pandas as pd
from evidently_data_analysis import EvidentlyDataAnalysis
from lightning.app.frontend.web import StaticWebFrontend
import lightning as L

class LitApp(L.LightningFlow):
    def __init__(self, train_dataframe_path, test_dataframe_path, target_column_name, task_type) -> None:
        super().__init__()
        self.train_dataframe_path = train_dataframe_path
        self.test_dataframe_path = test_dataframe_path
        self.target_column_name = target_column_name
        self.task_type = task_type
        self.evidently_data_analysis = EvidentlyDataAnalysis(
                                                        train_dataframe_path=self.train_dataframe_path,
                                                        test_dataframe_path=self.test_dataframe_path,
                                                        target_column_name=self.target_column_name,
                                                        task_type=self.task_type
                                                        )

    def run(self):
        self.evidently_data_analysis.run()

    def configure_layout(self):
        tab_1 = {'name': 'Data report', 'content': self.evidently_data_analysis}
        return tab_1

if __name__ == "__main__":
    # classification use case
    app = L.LightningApp(LitApp(
            train_dataframe_path='resources/ba_cancer_train.csv',
            test_dataframe_path='resources/ba_cancer_test.csv',
            target_column_name='target',
            task_type='classification'
        ))

```

Example #2
```python
# Note: This is not a complete example but is a demo of providing data to the component during the execution of the run method of some other component instead of providing data during the initialization

# provide payload arguments of the train and test dataframes transferred from another component

# some other component's run method:

class LitApp(L.LightningFlow):
    def __init__(self):
        self.other_component = OtherComponent()
        self.evidently_data_anaylysis = EvidentlyDataAnalysis() #default initialization

    def run(self):
        self.other_component.run()
        self.evidently_data_analysis.task_type = 'classification'
        self.evidently_data_analysis.target_column_name = 'target'
        # other_component has two attributes which are of type lightning.app.storage.payload.Payload
        self.evidently_data_analysis.run(
                                            train_df=self.other_component.train_df, 
                                            test_df=self.other_component.test_df
                                        )
        # some other work components running
    
    def configure_layout(self):
        tabs = []
        tab_1 = {'name': 'Data report', 'content': self.evidently_data_analysis}
        # tab_2 = ...  some other frontend
        # tab_3 = ...  some other frontend
        tabs.append(tab_1)

        return tabs
        

if __name__ == "__main__":
    app = L.LightningApp(LitApp())

```

## Sample Output of the App

![data_drift](https://user-images.githubusercontent.com/23210132/181892630-7a6afe2f-9ed1-43f3-9425-84c45fb8f665.PNG)

## TODO

- [x] Write relevant tests
- [x] Integrate more use cases supported by EvidentlyAI (only 2 use cases - classification and regression supported and they're covered in this component)
- [x] Test in lightning cloud
