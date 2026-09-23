"""Bounded production-path test for the E4 duration implementation."""
from types import SimpleNamespace
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.fedscale_trace import _profile_duration

def test_production_duration_path():
    args=SimpleNamespace(fedscale_default_duration=1.0,fedscale_upload_size_mb=1.0,fedscale_download_size_mb=2.0,fedscale_batch_size=8,fedscale_local_steps=10)
    assert abs(_profile_duration({'computation':12.5,'communication':25.0},args)-3.12)<1e-12

if __name__=='__main__':
    test_production_duration_path(); print('PASS production DirBridge duration path')
