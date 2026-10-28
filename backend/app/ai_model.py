from __future__ import annotations

from dataclasses import dataclass

from sklearn.ensemble import IsolationForest


@dataclass
class AnomalyResult:
    is_anomaly: bool
    score: float
    threshold: float


class AnomalyDetector:
    def __init__(self) -> None:
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.fit_data = [
            [20.0, 45.0, 5.0],
            [22.0, 50.0, 6.0],
            [21.0, 48.0, 5.5],
            [30.0, 60.0, 15.0],
            [31.0, 62.0, 17.0],
            [18.0, 40.0, 4.0],
            [19.0, 42.0, 5.0],
            [25.0, 52.0, 8.0],
            [24.0, 51.0, 7.0],
            [80.0, 10.0, 90.0],
        ]
        self.model.fit(self.fit_data)

    def analyze(self, temperature: float, humidity: float, requests_per_minute: float) -> AnomalyResult:
        sample = [[temperature, humidity, requests_per_minute]]
        decision = self.model.decision_function(sample)[0]
        score = -decision
        threshold = -self.model.offset_
        is_anomaly = bool(self.model.predict(sample)[0] == -1)
        return AnomalyResult(is_anomaly=is_anomaly, score=float(score), threshold=float(threshold))
