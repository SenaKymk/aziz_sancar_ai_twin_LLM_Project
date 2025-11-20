import mlflow
import time
import random

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("jenkins_demo")

with mlflow.start_run():
    for epoch in range(1, 6):
        acc = 0.8 + random.random() * 0.1
        loss = 1.0 / epoch + random.random() * 0.01
        mlflow.log_metric("accuracy", acc, step=epoch)
        mlflow.log_metric("loss", loss, step=epoch)
        print(f"[Epoch {epoch}] acc={acc:.3f}, loss={loss:.3f}")
        time.sleep(0.5)

print("✅ Demo training complete — metrics logged to MLflow!")
