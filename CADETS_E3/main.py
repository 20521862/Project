import os
import subprocess

def run_command(command):
    """Runs a system command and checks for errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error:\n{e.stderr.decode()}")
        exit(1)

def prepare():
    print("Running prepare...")
    os.makedirs('./artifact/', exist_ok=True)

def create_database():
    print("Running create_database...")
    run_command("python create_data.py")

def embed_graphs():
    print("Running embed_graphs...")
    run_command("python embedding.py")

def train():
    print("Running train...")
    run_command("python train.py")

def test():
    print("Running test...")
    run_command("python test.py")

def anomalous_queue():
    print("Running anomalous_queue...")
    run_command("python anomalous_queue_construction.py")

def evaluation():
    print("Running evaluation...")
    run_command("python evaluation.py")

def attack_investigation():
    print("Running attack_investigation...")
    run_command("python attack_investigation.py")

def preprocess():
    print("Running preprocess...")
    prepare()
    #create_database()
    embed_graphs()

def deep_graph_learning():
    print("Running deep_graph_learning...")
    train()
    test()

def anomaly_detection():
    print("Running anomaly_detection...")
    anomalous_queue()
    evaluation()

def pipeline():
    print("Running full pipeline...")
    preprocess()
    deep_graph_learning()
    anomaly_detection()
    attack_investigation()

if __name__ == "__main__":
    pipeline()

