from prometheus_client import Counter, Gauge, Histogram


documents_received_total = Counter(
    "documents_received_total",
    "Total number of documents received by document worker"
)


documents_processed_total = Counter(
    "documents_processed_total",
    "Total number of documents processed by document worker"
)


documents_success_total = Counter(
    "documents_success_total",
    "Total number of successfully processed documents"
)


documents_failed_total = Counter(
    "documents_failed_total",
    "Total number of failed documents"
)


documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being processed"
)


extraction_duration = Histogram(
    "extraction_duration_seconds",
    "Document text extraction duration in seconds"
)


worker_errors_total = Counter(
    "worker_errors_total",
    "Total number of worker errors",
    ["worker"]
)