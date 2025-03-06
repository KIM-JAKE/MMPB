import wandb
import pandas as pd
import weave

# 엑셀 파일을 DataFrame으로 로드합니다.
df = pd.read_excel("/workspace/VLMEvalKit/outputs/outputs0306.xlsx")

PROJECT_NAME = "MMPB0306"

# DataFrame의 각 행을 딕셔너리로 변환하여 레코드 리스트로 만듭니다.
records = df.to_dict(orient='records')

# WandB Run을 초기화합니다.
run = weave.init('MMPB0306_test')

# WandB Weave Dataset 생성: records를 rows로 넣습니다.
dset = weave.Dataset(name="experiment_results", rows=records)

# Weave에 데이터셋을 게시합니다.
weave.publish(dset)

run.finish()