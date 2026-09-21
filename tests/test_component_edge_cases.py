import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from anomaly_detector import AnomalyDetector
from src.event_consumer import EventConsumer
from src.event_producer import EventProducer
from src.event_topic import EventTopic


def test_detector_reports_each_anomaly_reason():
    record = {
        "timestamp": "2026-09-20T10:06:00",
        "service": "payment-service",
        "response_time_ms": 501,
        "cpu_percent": 81,
        "memory_percent": 81,
        "log_level": "WARNING",
    }

    event = AnomalyDetector().detect(record)

    assert event["reasons"] == [
        "High response time",
        "High CPU utilization",
        "High memory utilization",
        "Error log detected",
    ]
    assert event["source"] == record


def test_producer_rejects_empty_event():
    topic = EventTopic("anomaly-events")

    assert EventProducer(topic).publish(None) is False
    assert topic.get_messages() == []


def test_topic_clear_removes_messages():
    topic = EventTopic("anomaly-events")
    topic.publish({"type": "ANOMALY"})

    topic.clear()

    assert topic.get_messages() == []


def test_consumer_returns_empty_topic_messages():
    assert EventConsumer(EventTopic("anomaly-events")).consume() == []
