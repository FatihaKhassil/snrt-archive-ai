from prometheus_client import Counter, Gauge, Histogram


documents_received_total = Counter(
    "documents_received_total",
    "Total number of documents received by audio worker"
)


documents_processed_total = Counter(
    "documents_processed_total",
    "Total number of documents processed by audio worker"
)


documents_success_total = Counter(
    "documents_success_total",
    "Total number of successfully processed audio documents"
)


documents_failed_total = Counter(
    "documents_failed_total",
    "Total number of failed audio documents"
)


documents_processing = Gauge(
    "documents_processing",
    "Number of audio documents currently being processed"
)


transcription_duration = Histogram(
    "transcription_duration_seconds",
    "Audio transcription duration in seconds"
)


worker_errors_total = Counter(
    "worker_errors_total",
    "Total number of worker errors",
    ["worker"]
)