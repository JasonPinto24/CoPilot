import os
import requests
import time

# ── Output folder ─────────────────────────────────────────────────────────────
OPTION_A_DIR = "data/raw/option_a"

# ── Documents to download ─────────────────────────────────────────────────────
DOCS = [
    # Kafka
    (
        "kafka-introduction.md",
        "https://raw.githubusercontent.com/confluentinc/kafka-tutorials/master/README.md",
    ),
    (
        "kafka-consumers.md",
        "https://raw.githubusercontent.com/confluentinc/confluent-kafka-python/master/README.md",
    ),
    # Kubernetes
    (
        "kubernetes-pods.md",
        "https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/workloads/pods/pod-lifecycle.md",
    ),
    (
        "kubernetes-deployments.md",
        "https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/concepts/workloads/controllers/deployment.md",
    ),
    (
        "kubernetes-debugging.md",
        "https://raw.githubusercontent.com/kubernetes/website/main/content/en/docs/tasks/debug/debug-application/debug-pods.md",
    ),
    # Docker
    (
        "docker-overview.md",
        "https://raw.githubusercontent.com/moby/moby/master/README.md",
    ),
    (
        "docker-compose.md",
        "https://raw.githubusercontent.com/docker/compose/main/README.md",
    ),
    # FastAPI
    (
        "fastapi-tutorial.md",
        "https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/tutorial/first-steps.md",
    ),
    (
        "fastapi-requestbody.md",
        "https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/tutorial/body.md",
    ),
    # Python
    (
        "python-logging.md",
        "https://raw.githubusercontent.com/python/cpython/main/Doc/howto/logging.rst",
    ),
    (
        "python-exceptions.md",
        "https://raw.githubusercontent.com/python/cpython/main/Doc/tutorial/errors.rst",
    ),
]


# ── Download one file ─────────────────────────────────────────────────────────
def download_doc(filename, url):
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filepath = f"{OPTION_A_DIR}/{filename}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"  Saved: {filepath} ({len(response.text)} chars)")
            return True
        else:
            print(f"  Failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  Error: {e}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== Downloading Option A Public IT Docs ===")
    print()

    os.makedirs(OPTION_A_DIR, exist_ok=True)

    success = 0
    failed = 0

    for filename, url in DOCS:
        result = download_doc(filename, url)
        if result:
            success += 1
        else:
            failed += 1
        time.sleep(1)

    print()
    print("=== Download complete ===")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Files saved to: {OPTION_A_DIR}/")


if __name__ == "__main__":
    main()