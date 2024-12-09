import subprocess

def run_cli(args, input_data=None):
    process = subprocess.run(
        ["python3", "util.py"] + args,
        input=input_data,
        text=True,
        capture_output=True
    )
    return process.stdout, process.stderr

def test_first_option():
    stdout, _ = run_cli(["--first", "3", "logs/sample.log"])
    assert len(stdout.splitlines()) == 3

def test_ipv4_option():
    stdout, _ = run_cli(["--ipv4", "logs/sample.log"])
    assert "192.168.1.1" in stdout

def test_timestamps_option():
    stdout, _ = run_cli(["--timestamps", "logs/sample.log"])
    assert "12:34:56" in stdout

def test_last_option():
    stdout, _ = run_cli(["--last", "2", "logs/sample.log"])
    assert len(stdout.splitlines()) == 2
