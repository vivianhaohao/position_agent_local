
from datetime import datetime
from pathlib import Path

log_dir=Path('***')
log_dir.mkdir(exist_ok=True)

def add_user_logs(wallet:str,event_type:str,detail:str):
    log_file=log_dir/f'{wallet.lower()}.log'
    timestamp=datetime.utcnow().strftime('%Y--%m--%d--%H--%M--%S')
    log_line=f'[time:{timestamp}][📡event type:{event_type}]📙details:{detail}]\n'

    with open(log_file,'a',encoding='utf-8') as f:
        f.write(log_line)
