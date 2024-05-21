KAFKA_MANIFESTS_PATH = artifacts/manifests/kafka
KAFKA_CHART_PATH = artifacts/charts/kafka
DS_INFERENCE_MANIFESTS_PATH = artifacts/manifests/deepstream-inference
DS_INFERENCE_CHART_PATH = artifacts/charts/deepstream-inference
DS_RECORDING_CHART_PATH = artifacts/charts/deepstream-recording
CHART_PACKAGES_PATH = artifacts/packages

# Get the currently used golang install path (in GOPATH/bin, unless GOBIN is set)
ifeq (,$(shell go env GOBIN))
GOBIN=$(shell go env GOPATH)/bin
else
GOBIN=$(shell go env GOBIN)
endif

# Setting SHELL to bash allows bash commands to be executed by recipes.
# Options are set to exit when a recipe line exits non-zero or a piped command fails.
SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec

.PHONY: all
all: generate-charts

## Location to install dependencies to
LOCALBIN ?= $(shell pwd)/bin
$(LOCALBIN):
	mkdir -p $(LOCALBIN)

## Tool Binaries
HELMIFY ?= $(LOCALBIN)/helmify
HELM ?= helm

.PHONY: helmify
helmify: $(HELMIFY) ## Download helmify locally if necessary.
$(HELMIFY): $(LOCALBIN)
	test -s $(LOCALBIN)/helmify || GOBIN=$(LOCALBIN) go install github.com/arttor/helmify/cmd/helmify@latest

generate-charts: helmify
	$(HELMIFY) -f ${KAFKA_MANIFESTS_PATH} -r ${KAFKA_CHART_PATH}
#	$(HELMIFY) -f ${DS_INFERENCE_MANIFESTS_PATH} -r ${DS_INFERENCE_CHART_PATH}

generate-chart-packages:
	rm -rf ${CHART_PACKAGES_PATH}
	$(HELM) package ${KAFKA_CHART_PATH} -d ${CHART_PACKAGES_PATH}
	$(HELM) package ${DS_INFERENCE_CHART_PATH} -d ${CHART_PACKAGES_PATH}
	$(HELM) package ${DS_RECORDING_CHART_PATH} -d ${CHART_PACKAGES_PATH}

