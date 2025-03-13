## Introduction

LLMs (Large Language Models) are increasingly used to power chatbots or other knowledge assistants. KServe is a standard Model Inference Platform on Kubernetes, built for highly scalable use cases. Kserve comes with multiple Model Serving Runtimes. One of the runtimes is the Hugging Face serving runtime. This runtime implements two backends namely Hugging Face and vLLM that can serve Hugging Face models out of the box.

The Hugging Face runtime supports the following ML tasks:

- Text Generation
- Text2Text Generation
- Fill Mask
- Token Classification
- Sequence Classification (Text Classification)

This example Helm chart can be used to create a Kserve `InferenceService` to deploy a vLLM model.

## Prerequisites

- A Huggingface account
- (optional) Access to the model to deploy
- A Huggingface access toke with `write` access
- A SealedSecret with the Hugging Face token (`HF_TOKEN`)
- Kserve installed by a platform-admin
- An LKE cluster with at least 3 RTX4000 Ada x1 Medium GPU plan