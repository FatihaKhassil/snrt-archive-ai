from prometheus_client import Counter, Gauge, Histogram


# ============================================================
# DOCUMENTS
# ============================================================

documents_received_total = Counter(
    "documents_received_total",
    "Total number of documents received"
)

documents_processed_total = Counter(
    "documents_processed_total",
    "Total number of documents processed"
)

documents_success_total = Counter(
    "documents_success_total",
    "Total number of successfully processed documents"
)

documents_failed_total = Counter(
    "documents_failed_total",
    "Total number of failed documents"
)


# ============================================================
# DOCUMENT PROCESSING
# ============================================================

documents_processing = Gauge(
    "documents_processing",
    "Number of documents currently being processed"
)


document_processing_seconds = Histogram(
    "document_processing_seconds",
    "Document processing duration in seconds",
    ["stage"]
)


# ============================================================
# ERRORS / TIMEOUTS
# ============================================================

worker_errors_total = Counter(
    "worker_errors_total",
    "Total number of worker errors",
    ["worker"]
)


worker_timeouts_total = Counter(
    "worker_timeouts_total",
    "Total number of worker timeouts",
    ["worker"]
)


# ============================================================
# SEARCH
# ============================================================

searches_total = Counter(
    "searches_total",
    "Total number of searches",
    ["type"]
)


solr_search_latency = Histogram(
    "solr_search_latency",
    "Solr search latency in seconds"
)


chroma_search_latency = Histogram(
    "chroma_search_latency",
    "ChromaDB search latency in seconds"
)


rag_response_latency = Histogram(
    "rag_response_latency",
    "RAG response latency in seconds"
)