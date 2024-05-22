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
```

Generate Helm charts.

```bash
make generate-chart-packages
```

Install charts. Remember manipulating chart values.

```bash
helm install ds-inference ./artifacts/packages/deepstream-inference-0.1.0.tgz -n deepstream-test
```

```bash
helm install ds-recording ./artifacts/packages/deepstream-recording-0.1.0.tgz -n deepstream-recording-test
```

```bash
helm install plc-client ./artifacts/packages/plc-client-0.1.0.tgz -n plc
```
