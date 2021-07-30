#!/usr/bin/env python
# coding: utf-8

# # Connecting Neo4j with Python

# In[1]:


# the following library will run codes on python which directly 
# operates onto neo4j
# this is a good method to store your code as 
# neo4j does not store/track its cypher language  
from neo4j import GraphDatabase

# Database Credentials

uri             = "bolt://localhost:11005"

userName        = "neo4j"

password        = "1234"

# Connect to the neo4j database server

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))


# In[2]:


#Create unique director nodes
#First set up the unique constraint
# create director nodes
ql1="""
CREATE CONSTRAINT directorConstraint ON (director:Director) ASSERT director.id IS UNIQUE
"""


# In[5]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(ql1)


# In[4]:


# create a constraint for unique company number- this prevent duplicating node
constraint="""
CREATE CONSTRAINT companyConstraint ON (company:Company) ASSERT company.id IS UNIQUE
"""


# In[7]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(constraint)


# In[6]:


# load csv
node="""LOAD CSV WITH HEADERS FROM "file:///directornumber.csv" AS csvLine
CREATE (d:Director {id:csvLine.DirectorNumber, name: csvLine.Fullname})
"""


# In[7]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(node)


# In[ ]:


# the following creates the edges for directors whilst using weights as an property
overlap = """
WITH "file:///overlap_clear.csv" AS uri
LOAD CSV WITH HEADERS FROM uri AS row
MATCH (d:Director {id:row.DirectorNumber}), (d2:Director {id:row.DirectorNumber_y})
CREATE (d)-[r:KNOWS {weight:toInteger(row.weight)}]->(d2) """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(overlap)


# # Centrality Analysis

# In[ ]:


#Create a graph variable on neo4j
graph = """
CALL gds.graph.create('myGraph', '*', 'KNOWS')"""


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(graph)


# In[ ]:


#Closeness centrality 
closeness = """
 CALL gds.alpha.closeness.stream({
   nodeProjection: '*',
   relationshipProjection: 'KNOWS'
 })
 YIELD nodeId, centrality
 RETURN gds.util.asNode(nodeId).name AS user, centrality
 ORDER BY centrality DESC """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(closeness)


# In[ ]:


#betweenness centrality 
betweenness = """
CALL gds.betweenness.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(betweenness)


# In[ ]:


#eigenvector centrality
eigenvector = """
 CALL gds.alpha.eigenvector.stream('myGraph')
 YIELD nodeId, score
 RETURN gds.util.asNode(nodeId).name AS name, score
 ORDER BY score DESC """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(eigenvector)


# In[ ]:


# degree centrality 
degree = """
CALL gds.alpha.degree.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS followers
ORDER BY followers DESC, name DESC """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(degree)


# In[ ]:


# harmonic
harmonic = """
CALL gds.alpha.closeness.harmonic.stream({
  nodeProjection: '*',
  relationshipProjection: 'KNOWS'
})
YIELD nodeId, centrality
RETURN gds.util.asNode(nodeId).name AS user, centrality
ORDER BY centrality DESC """


# In[ ]:


# run this everytime you run a query and it connect with neo4j
with graphDB_Driver.session() as graphDB_Session:

    # Create nodes

    graphDB_Session.run(harmonic)


# In[2]:


# erased all relationship
clear1 = """match (a) -[r] -> () delete a, r"""


# In[3]:


# erased all node
clear2 = """match (a) delete a"""


# In[6]:


with graphDB_Driver.session() as graphDB_Session:

    # Create nodes
    graphDB_Session.run(clear1)
    graphDB_Session.run(clear2)


# In[10]:


with graphDB_Driver.session() as graphDB_Session:

    # Create nodes
    graphDB_Session.run(clear1)


# # Codes not used

# In[32]:


# unique company number
#ql4="""
#LOAD CSV WITH HEADERS FROM "file:///companynumber.csv" AS csvLine
#CREATE (c:Company {id:csvLine.CompanyNumber})
#"""


# In[34]:


# # Create the relationship 
# ql5="""LOAD CSV WITH HEADERS FROM "file:///leedshealthtech.csv" AS csvLine
# MATCH (d:Director), (d2:Director {id:csvLine.DirectorNumber})
# WHERE d <> d2 
# CREATE (d)-[:KNOWS {Companynumber: csvLine.CompanyNumber}]->(d2)

# """

