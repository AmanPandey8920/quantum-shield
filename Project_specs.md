# QuantumShield --- Project Specifications

**Project type:** IoT cybersecurity prototype\
**Core themes:** IoT security, AI-assisted anomaly detection,
post-quantum cryptography\
**Project owner:** Anurudh Singh\
**Status:** Prototype / active development

## 1. Executive Summary

QuantumShield is an educational IoT cybersecurity platform designed to
explore how device authentication, request-rate controls, AI-assisted
anomaly detection, security-event monitoring, and post-quantum
cryptography demonstrations can work together.

An ESP32-based sensor node can send telemetry to a FastAPI backend. The
backend validates incoming requests, can store sensor readings, and can
analyse selected features for unusual patterns. A React dashboard is
intended to present readings and security alerts. A separate
cryptography demonstration uses ML-KEM for shared-secret establishment
and AES-GCM for authenticated encryption.

QuantumShield is a prototype, not a certified security product. Features
must be verified in the integrated code before they are described as
operational.

## 2. Problem Statement

Connected IoT devices can be exposed to risks such as:

-   Weak or poorly managed device credentials.
-   Excessive requests and resource exhaustion.
-   Unusual or manipulated sensor readings.
-   Limited visibility into security-relevant events.
-   Long-term planning challenges as organisations prepare to adopt
    post-quantum cryptography.

QuantumShield explores a modular approach to device controls, anomaly
signals, event visibility, and cryptographic readiness.

## 3. Objectives

1.  Receive sensor telemetry from an IoT device.
2.  Validate device identity and request data.
3.  Apply rate limits to reduce excessive requests.
4.  Use an anomaly-detection model to flag unusual telemetry or traffic
    features.
5.  Record security-relevant events for investigation.
6.  Provide a dashboard for sensor readings and security alerts.
7.  Demonstrate ML-KEM shared-secret establishment and AES-GCM
    authenticated encryption in a separate test program.
8.  Evaluate the prototype with controlled tests and measured results.

## 4. Scope

### In scope

-   ESP32 and DHT22 sensor demonstration.
-   FastAPI backend.
-   SQLite persistence for device, reading, and event records where
    integrated.
-   Device authentication and request-rate limiting prototypes.
-   Isolation Forest anomaly-detection demonstration.
-   React/Vite dashboard.
-   ML-KEM and AES-GCM cryptography demonstration.
-   Educational Qiskit Grover circuit and a classical
    Shor/period-finding concept demonstration.
-   Controlled tests for authentication, rate limiting, unusual input,
    and event logging.

### Out of scope for the current prototype

-   Certified or production-ready end-to-end quantum-safe security.
-   A custom cryptographic protocol.
-   Guaranteed attack detection or zero false positives.
-   Automatic containment of real attacks without operator review.
-   Safety-critical healthcare or industrial deployment.
-   Claims of actual quantum advantage from small educational
    simulations.

## 5. Proposed Architecture

``` text
ESP32 + DHT22
     |
     | Sensor telemetry over local network
     v
FastAPI Backend
     |
     +--> Device authentication
     |
     +--> Request rate limiting
     |
     +--> Input validation
     |
     +--> AI anomaly detector
     |
     +--> SQLite persistence
              |
              v
       Security event records
              |
              v
       React monitoring dashboard


Separate cryptography demonstration:
ML-KEM shared-secret establishment
              |
              v
       AES-GCM authenticated encryption
              |
              v
      Decryption / tamper-rejection test
```

The cryptography demonstration is separate from the live
ESP32-to-backend pipeline unless and until it is deliberately integrated
and tested.

## 6. Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Purpose
  ----------------------- ----------------------- -----------------------
  IoT hardware            ESP32, DHT22            Sensor telemetry
                                                  prototype

  Firmware                Arduino IDE, C++        Read sensor and send
                                                  HTTP requests

  Backend                 Python, FastAPI,        API and request
                          Uvicorn                 processing

  Database                SQLite, SQLAlchemy      Device, reading, and
                                                  event persistence

  AI/ML                   scikit-learn, Isolation Flag unusual feature
                          Forest                  patterns

  Frontend                React, Vite             Monitoring interface

  Visualisation           Recharts                Sensor charts

  Post-quantum demo       Python `cryptography`   Shared-secret
                          with ML-KEM support     establishment
                                                  demonstration

  Symmetric encryption    AES-GCM                 Confidentiality and
                                                  authenticated integrity

  Quantum learning demo   Qiskit                  Small quantum-circuit
                                                  simulation
  -----------------------------------------------------------------------

Package APIs and supported algorithm names must be verified against the
installed library version.

## 7. Functional Requirements

### FR-01: Sensor ingestion

The backend should accept a validated payload containing a device ID and
sensor values.

Example payload:

``` json
{
  "device_id": "ESP32-001",
  "temperature": 25.0,
  "humidity": 50.0
}
```

### FR-02: Device authentication

Protected ingestion endpoints should reject missing or invalid
credentials. Device-specific credentials are preferred over a single
shared token.

### FR-03: Request rate limiting

The service should reject requests that exceed the configured limit and
return HTTP `429 Too Many Requests`.

### FR-04: Anomaly analysis

The AI component should analyse configured features, such as
temperature, humidity, and requests per minute, and return a result that
indicates whether the sample is unusual.

An anomaly result is a review signal, not proof of malicious activity.

### FR-05: Persistence

When integrated, the backend should persist device records, sensor
readings, and security events.

### FR-06: Dashboard

The frontend should display sensor readings, recent events, anomaly
results, and device status where supported by the backend API.

### FR-07: Cryptography demonstration

The demo should establish a shared secret using ML-KEM, derive or use an
appropriate symmetric key, encrypt a sample payload with AES-GCM,
decrypt it successfully, and reject modified ciphertext.

### FR-08: Auditability

Security events should include an event type, device identifier where
available, timestamp, and safe diagnostic details. Secrets must never be
written to logs.

## 8. Proposed API Surface

These are target endpoints, not a guarantee that every route is
currently implemented.

  ----------------------------------------------------------------------------
  Method                  Endpoint                     Purpose
  ----------------------- ---------------------------- -----------------------
  `GET`                   `/`                          Basic service
                                                       information

  `GET`                   `/health`                    Health check

  `GET`                   `/devices`                   List registered devices

  `POST`                  `/devices/register`          Register a device,
                                                       subject to secure
                                                       provisioning

  `POST`                  `/sensor-data`               Submit a sensor reading

  `GET`                   `/sensor-data/{device_id}`   Read stored telemetry

  `POST`                  `/ai/analyze`                Analyse a sample with
                                                       the AI detector

  `POST`                  `/monitoring/ingest`         Target integrated
                                                       ingestion workflow

  `GET`                   `/monitoring/events`         Retrieve recent
                                                       security events

  `GET`                   `/monitoring/live`           Target live-alert
                                                       stream, if implemented
  ----------------------------------------------------------------------------

The final API contract must be reconciled with the actual `app/main.py`
and database models.

## 9. Non-Functional Requirements

-   **Security:** Use authenticated communication, secure credential
    handling, input validation, and least privilege.
-   **Reliability:** Return clear error codes and avoid losing persisted
    events.
-   **Maintainability:** Keep API, database, AI, and security logic
    modular.
-   **Observability:** Record useful security events without logging
    secrets.
-   **Performance:** Measure latency and request handling under
    controlled loads.
-   **Usability:** Keep the dashboard understandable to operators and
    judges.
-   **Portability:** Support local development on a typical Python and
    Node.js environment.

## 10. Security Design Notes

1.  Do not expose the development server directly to the public
    internet.
2.  Use TLS for deployed client-server communication.
3.  Use unique per-device credentials with secure provisioning and
    revocation.
4.  Do not store raw long-lived secrets in source code or logs.
5.  An in-memory rate limiter is only a development demonstration;
    multi-worker deployments need shared state or a central limiter.
6.  Replay protection requires authenticated messages, freshness checks,
    and server-side duplicate detection; a timestamp or nonce alone is
    insufficient.
7.  ML-KEM establishes a shared secret; it does not authenticate the
    sender by itself.
8.  AES-GCM requires correct nonce handling and key management.
9.  Do not build a custom production cryptographic handshake. Use
    maintained, standards-based protocols and libraries.
10. Keep quantum-algorithm simulations clearly separate from deployed
    security controls.

## 11. AI Model and Evaluation

The current educational design uses an Isolation Forest trained on
synthetic or demonstration data.

### Candidate features

-   Temperature.
-   Humidity.
-   Requests per minute.

### Evaluation plan

-   Precision.
-   Recall.
-   False-positive rate.
-   False-negative rate.
-   Detection latency.
-   Performance on labelled, representative test data.

No accuracy percentage should be claimed until measured on a documented
test set. Sensor values outside expected ranges may indicate sensor
faults, environmental changes, or attacks; context matters.

## 12. Test Plan

  ---------------------------------------------------------------------------
  Test                    Method                  Expected outcome
  ----------------------- ----------------------- ---------------------------
  Normal telemetry        Submit a valid          Valid request is processed
                          registered-device       
                          reading                 

  Missing/invalid         Submit without valid    Request rejected, normally
  credential              credentials             HTTP 401

  Unregistered device     Submit an unknown       Rejected according to the
                          device ID               API policy

  Rate limit              Exceed the configured   HTTP 429
                          request window          

  Unusual sensor pattern  Submit controlled       Model returns an anomaly
                          unusual feature values  score/flag where expected

  Persistence             Submit a reading and    Reading is retrievable if
                          query history           persistence is integrated

  Event logging           Trigger a controlled    Event appears in stored
                          security event          event history if
                                                  implemented

  AES-GCM tamper test     Modify ciphertext or    Decryption/authentication
                          authentication tag      fails

  Device revocation       Revoke a test device    Protected request is
                          and retry               rejected

  Stream reconnect        Disconnect and          Stream resumes according to
                          reconnect dashboard     implemented design
  ---------------------------------------------------------------------------

Tests should be run only against systems and devices the project team
owns or is authorised to test.

## 13. Demo Plan for Judges

Recommended short demo:

1.  Show a normal sensor reading.
2.  Send an unusual reading and show the AI flag.
3.  Send a request with an invalid token and show rejection.
4.  Show the corresponding security event if event persistence is
    working.
5.  Run the ML-KEM + AES-GCM demonstration and show successful
    decryption followed by tamper rejection.
6.  Clearly identify which components are live-integrated and which run
    as separate demonstrations.

Keep a recorded demo and screenshots as a backup.

## 14. Roadmap

### Milestone 1 --- Stable backend

Confirm database models, API routes, validation, and error handling.

### Milestone 2 --- Device security

Implement per-device credentials, revocation, and secure provisioning.

### Milestone 3 --- Persistent monitoring

Store readings and security events; verify dashboard integration.

### Milestone 4 --- AI evaluation

Use representative data, define baselines, and report measured metrics.

### Milestone 5 --- Cryptography integration research

Evaluate a supported standards-based protocol and library for
post-quantum key establishment; avoid custom protocol design.

### Milestone 6 --- Controlled pilot

Run security tests, performance tests, and documented limitations
review.

## 15. Known Limitations

-   Some features may exist only as separate code examples and may not
    yet be integrated end to end.
-   The AI demonstration may rely on synthetic data.
-   The initial rate limiter may be in-memory and not shared across
    server workers.
-   The ML-KEM + AES-GCM example is not automatically connected to ESP32
    telemetry.
-   The quantum algorithm demonstrations are educational simulations.
-   No production security certification or real-world detection
    performance is implied.

## 16. Short Project Description

**QuantumShield** is an IoT cybersecurity prototype that explores device
authentication, request-rate controls, AI-assisted anomaly detection,
security-event monitoring, and post-quantum cryptography demonstrations.
It uses an ESP32 sensor node, a Python/FastAPI backend, SQLite
persistence, a React dashboard, and separate ML-KEM/AES-GCM experiments.
Its goal is to provide a testable foundation for smarter IoT security
while clearly measuring limitations and planning for future integration.

------------------------------------------------------------------------

**Before submission:** Replace proposed or planned features with the
verified implementation status, add the team name and repository/demo
links, and include only measured test results.
