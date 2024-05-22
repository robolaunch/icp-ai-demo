# <img src="https://raw.githubusercontent.com/robolaunch/trademark/main/logos/svg/rocket.svg" width="40" height="40" align="top"> robolaunch ICP Inference Pipeline Demo


This project aims to demonstrate building an inference pipeline on robolaunch ICP.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)

## Overview

Repository contains four charts:
- DeepStream Inference
- Recording Agent
- DeepStream Recording
- PLC Client

![robolaunch ICP - Inference Pipeline Demo](https://github.com/robolaunch/icp-ai-demo/assets/46759747/c713213f-1f1e-4990-814a-b6ccfdaf9bd7)


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
helm install recording-agent ./artifacts/packages/recording-agent-0.1.0.tgz -n recording-agent
```

```bash
helm install ds-recording ./artifacts/packages/deepstream-recording-0.1.0.tgz -n deepstream-recording-test
```

```bash
helm install plc-client ./artifacts/packages/plc-client-0.1.0.tgz -n plc
```
