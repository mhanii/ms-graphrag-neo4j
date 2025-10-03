# MsGraphRAG-Neo4j

A Neo4j implementation of Microsoft's GraphRAG approach for knowledge graph-based retrieval augmented generation based on QFS.
Query-focused summarization (QFS) is a summarization task where the objective is to produce a concise and relevant summary of a given document or set of documents specifically tailored to answer or address a particular query or question provided by a user.

Learn more about [GraphRAG](https://graphrag.com/).

## Overview

MsGraphRAG-Neo4j is a Python library that implements Microsoft's GraphRAG methodology with Neo4j as the graph database backend. This library provides a seamless way to:

1. Extract entities and relationships from unstructured text
2. Build a knowledge graph in Neo4j
3. Generate summaries for nodes and relationships
4. Detect and summarize communities within the graph
5. Leverage this graph structure for enhanced RAG

The implementation supports multiple LLM providers (OpenAI, Azure, Gemini) for text processing and leverages Neo4j's powerful graph capabilities, including the Graph Data Science (GDS) library.

> **⚠️ IMPORTANT NOTE**: This repository is experimental and provided as-is. The current implementation lacks optimizations for larger graphs, which may lead to exceptions or performance issues when processing substantial amounts of data. Use with caution in production environments and consider implementing additional error handling and optimization for large-scale deployments.


## Features

- **Entity and Relationship Extraction**: Extract structured information from unstructured text using a configurable LLM provider.
- **Graph Construction**: Automatically build a knowledge graph in Neo4j.
- **Node and Relationship Summarization**: Generate concise summaries to improve retrieval.
- **Community Detection**: Use Neo4j GDS to identify clusters of related information.
- **Community Summarization**: Provide high-level descriptions of concept clusters.
- **Neo4j Integration**: Seamless integration with Neo4j database for persistent storage.
- **Multi-Provider Support**: Switch between OpenAI, Azure, and Gemini for LLM tasks.

## Installation

```bash
pip install -e .
```

## Requirements

- Neo4j database (5.26+)
- APOC plugin installed in Neo4j
- Graph Data Science (GDS) library installed in Neo4j
- API credentials for your chosen LLM provider (OpenAI, Azure, or Gemini)

## Quick Start

First, set the necessary environment variables for your Neo4j instance and the chosen LLM provider.

### Environment Variables

- **Neo4j**:
  ```bash
  export NEO4J_URI="bolt://localhost:7687"
  export NEO4J_USERNAME="neo4j"
  export NEO4J_PASSWORD="your-password"
  ```

- **OpenAI**:
  ```bash
  export OPENAI_API_KEY="your-openai-api-key"
  ```

- **Azure**:
  ```bash
  export AZURE_OPENAI_API_KEY="your-azure-api-key"
  export AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
  export OPENAI_API_VERSION="2024-05-01-preview" # Optional
  ```

- **Gemini**:
  ```bash
  export GOOGLE_API_KEY="your-google-api-key"
  ```

### Example Usage

The following example demonstrates how to initialize `MsGraphRAG` and use it to build and summarize a graph. You can switch between providers by changing the `llm_provider` parameter.

```python
import os
import asyncio
from ms_graphrag_neo4j import MsGraphRAG
from neo4j import GraphDatabase

# --- Configuration ---
LLM_PROVIDER = "openai"  # Choose from "openai", "azure", or "gemini"
MODEL = "gpt-4o" # Or another model compatible with your provider

# --- Connect to Neo4j ---
driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
)

# --- Initialize MsGraphRAG with the chosen provider ---
ms_graph = MsGraphRAG(driver=driver, llm_provider=LLM_PROVIDER, model=MODEL)

# --- Define example data ---
example_texts = [
    "Tomaz works for Neo4j",
    "Tomaz lives in Grosuplje",
    "Tomaz went to school in Grosuplje"
]
allowed_entities = ["Person", "Organization", "Location"]


async def main():
    # Extract entities and relationships
    result = await ms_graph.extract_nodes_and_rels(example_texts, allowed_entities)
    print(result)

    # Generate summaries for nodes and relationships
    result = await ms_graph.summarize_nodes_and_rels()
    print(result)

    # Identify and summarize communities
    result = await ms_graph.summarize_communities()
    print(result)

    # Close the connection
    ms_graph.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## How It Works

1. **Extract Nodes and Relationships**: The library uses the configured LLM provider to extract entities and relationships from your text data, creating a structured graph.

2. **Summarize Nodes and Relationships**: Each entity and relationship is summarized to capture its essence across all mentions in the source documents.

3. **Community Detection**: The Leiden algorithm is applied to identify communities of related entities.

4. **Community Summarization**: Each community is summarized to provide a high-level understanding of the concepts it contains.
