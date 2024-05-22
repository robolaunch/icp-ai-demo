# <img src="https://raw.githubusercontent.com/robolaunch/trademark/main/logos/svg/rocket.svg" width="40" height="40" align="top"> robolaunch ICP Inference Pipeline Demo


This project aims to demonstrate building an inference pipeline on robolaunch ICP.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)

## Overview

Repository contains three charts:
- DeepStream Inference
- DeepStream Recording
- PLC Client

![robolaunch ICP - ML Inference Pipeline Demo Schema](https://github.com/robolaunch/icp-ai-demo/assets/46759747/5f2eb7dd-77b1-45af-80f1-4c0da61a6262)

## Quick Start

Clone repository.

```bash
git clone https://github.com/robolaunch/icp-ai-demo
cd icp-ai-demo
git checkout 1ae436dc60d5951c12713c4f5031a5c3b7778d99
```

Generate Helm charts.

```bash
make generate-chart-packages
```

Install charts. Remember manipulating chart values.

## DeepStream Inference

```bash
helm install ds-inference ./artifacts/packages/deepstream-inference-0.1.0.tgz -n deepstream-test
```

```yaml
# default values
deepstream:
  deepstream:
    image:
      repository: robolaunchio/deepstream-inference
      tag: 6.4-gc-triton-devel-v0.1.1
    imagePullPolicy: IfNotPresent
    resources:
      limits:
        nvidia.com/gpu: "1"
  ports:
  - name: rtsp-out
    port: 8554
    protocol: TCP
    targetPort: 8554
  replicas: 1
  type: NodePort
kubernetesClusterDomain: cluster.local
rtspSourceURL: rtsp://172.16.44.172:8554/mystream
boundingBoxes:
  enabled: true
  borderWidth: 5
  borderColor: "0;0;0.7;1"
  textSize: 15
  textColor: "1;1;1;1;"
  textBackgroundColor: "0.3;0.3;0.3;1"
  font: "Arial"
videoSink:
  width: 1280
  height: 720
  rtsp:
    enabled: true
    port: 8554
  kafka:
    enabled: true
    ip: "172.16.44.101"
    port: 32438
    topic: my-topic
inference:
  model:
    url: https://github.com/robolaunch/deepstream-test5-playground/releases/download/test/best.pt
    filename: best.pt
    framework: "YOLOV8" # or YOLOV8
    format: "pt"
```

## DeepStream Recording

```bash
helm install ds-recording ./artifacts/packages/deepstream-recording-0.1.0.tgz -n deepstream-recording-test
```

```yaml
# default values
deepstream:
  deepstream:
    image:
      repository: robolaunchio/deepstream-recording
      tag: 6.4-gc-triton-devel-v0.1.0
    imagePullPolicy: IfNotPresent
    resources:
      limits:
        nvidia.com/gpu: "1"
  ports:
  - name: rtsp-out
    port: 8554
    protocol: TCP
    targetPort: 8554
  replicas: 1
  type: NodePort
kubernetesClusterDomain: cluster.local
rtspSourceURL: rtsp://172.16.44.101:30725/ds-test
videoSink:
  width: 1280
  height: 720
  rtsp:
    enabled: true
    port: 8554
recording:
  enabled: true
  duration: 3
  interval: 3
  cache: 10
  agent:
    config:
      consumedKafka:
        ip: 172.16.44.101
        port: 32438
        topic: my-topic
      producedKafka:
        ip: 172.16.44.101
        port: 32438
        topic: record
      action:
        deltaSeconds: 3
        startMessage: delik
    kubernetesClusterDomain: cluster.local
    recordingAgent:
      recordingAgent:
        image:
          repository: robolaunchio/recording-agent
          tag: 0.1.2
        imagePullPolicy: IfNotPresent
      replicas: 1
```

## PLC Client

```bash
helm install plc-client ./artifacts/packages/plc-client-0.1.0.tgz -n plc
```

```yaml
# default values
kubernetesClusterDomain: cluster.local
plc:
  plcClient:
    image:
      repository: robolaunchio/plc-client
      tag: 0.1.2
    imagePullPolicy: IfNotPresent
  replicas: 1
config:
  kafka:
    ip: "172.16.44.101"
    port: 32438
    topic: my-topic
  plc:
    action:
      circuitKeyID: 0
      datablockID: 0
      startMessage: "devam"
      stopMessage: "delik"
    ip: "172.16.44.130"
    rack: 0
    slot: 1
```
