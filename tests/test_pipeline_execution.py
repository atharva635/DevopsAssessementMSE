import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from aiops_pipeline import run_pipeline


def test_run_pipeline_processes_and_consumes_anomalies(tmp_path):
    records = [
        {
            "timestamp": "2026-09-20T10:00:00",
            "service": "payment-service",
            "response_time_ms": 100,
            "cpu_percent": 40,
            "memory_percent": 50,
            "log_level": "INFO",
        },
        {
            "timestamp": "2026-09-20T10:01:00",
            "service": "payment-service",
            "response_time_ms": 700,
            "cpu_percent": 90,
            "memory_percent": 90,
            "log_level": "WARNING",
        },
    ]
    data_file = tmp_path / "service_data.json"
    data_file.write_text(json.dumps(records), encoding="utf-8")

    result = run_pipeline(str(data_file))

    assert result["records_processed"] == 2
    assert len(result["anomalies_detected"]) == 1
    assert result["events_consumed"] == []
    assert result["anomalies_detected"][0]["reasons"] == [
        "High response time",
        "High CPU utilization",
        "High memory utilization",
        "Error log detected",
    ]
