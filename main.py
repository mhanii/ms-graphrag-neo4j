import os
from ms_graphrag_neo4j.ms_graphrag import MsGraphRAG
from neo4j import GraphDatabase


driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"], 
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
)


ms_graph = MsGraphRAG(driver=driver, model='gpt-5-mini')



# Define example texts and entity types
example_texts = [
    "Tomaz works for Neo4j",
    "Tomaz lives in Grosuplje", 
    "Tomaz went to school in Grosuplje"
]
allowed_entities = ["Person", "Organization", "Location"]

# Extract entities and relationships
result = ms_graph.extract_nodes_and_rels(example_texts, allowed_entities)
print(result)

# Generate summaries for nodes and relationships
result = ms_graph.summarize_nodes_and_rels()
print(result)

# Identify and summarize communities
result = ms_graph.summarize_communities()
print(result)

# Close the connection
ms_graph.close()