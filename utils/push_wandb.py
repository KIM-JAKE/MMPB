import wandb
import pandas as pd

# wandb.init(project="MMPB_v1")

df = pd.read_excel("/workspace/VLMEvalKit/outputs/outputs0306.xlsx")

loaded_experiment_df = df

PROJECT_NAME = "MMPB0306"

EXPERIMENT_NAME_COL = "model"
METRIC_COLS = [col for col in loaded_experiment_df.columns if col != "model"]


for i, row in loaded_experiment_df.iterrows():
    run_name = row[EXPERIMENT_NAME_COL]

    metrics = {col: row[col] for col in METRIC_COLS}

    run = wandb.init(
        project=PROJECT_NAME,
        name=run_name,
        reinit=True 
    )

    for key, val in metrics.items():

        if isinstance(val, list):
            for _val in val:
                run.log({key: _val})
        else:
            run.log({key: val})

    run.finish()