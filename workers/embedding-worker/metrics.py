from prometheus_client import Counter, Gauge, Histogram


documents_received = Counter(
    "documents_received_total",
    "Total number of documents received by embedding worker"
)

documents_processed = Counter(
    "documents_processed_total",
    "Total number of documents processed by embedding worker"
)

documents_success = Counter(
    "documents_success_total",
    "Total number of successfully embedded documents"
)

documents_failed = Counter(
    "documents_failed_total",
    "Total number of failed embedding documents"
)

documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being embedded"
)

embedding_duration = Histogram(
    "embedding_duration_seconds",
    "Embedding and ChromaDB storage duration in seconds"
)

worker_errors = Counter(
    "worker_errors_total",
    "Total number of worker errors"
)