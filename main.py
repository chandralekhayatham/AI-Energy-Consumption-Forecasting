import argparse, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument("action",choices=["train","predict","web"],nargs="?",default="train"); a=p.parse_args()
if a.action=="train": subprocess.run([sys.executable,str(ROOT/"src/train.py")],check=True,cwd=ROOT)
elif a.action=="predict": subprocess.run([sys.executable,str(ROOT/"src/predict.py")],check=True,cwd=ROOT)
else: subprocess.run([sys.executable,str(ROOT/"app.py")],check=True,cwd=ROOT)
