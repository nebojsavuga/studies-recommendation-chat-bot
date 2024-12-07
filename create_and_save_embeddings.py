from sparql_query_helpers import create_embeddings, save_embeddings, embedding_file
import numpy as np

query_embeddings = np.array(create_embeddings(), dtype=np.float32)
save_embeddings(query_embeddings, embedding_file)
