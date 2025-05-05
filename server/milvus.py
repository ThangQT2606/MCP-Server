from loguru import logger
from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Optional, Union, Any
import os


def get_milvus_instance(collection_name: Optional[Union[str, Any]] = None) -> Optional[Milvus]:
    """
    Initialize a Milvus instance for a given collection name.

    Args:
        collection_name (str): The name of the collection to connect to.

    Returns:
        Milvus: A Milvus instance for the given collection name.
    """
    logger.info(f"Initializing Milvus connection for collection: {collection_name}")
    try:
        milvus_db = Milvus(
            collection_name=collection_name,
            embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
            connection_args={
                "host": os.getenv("MILVUS_HOST"),
                "port": os.getenv("MILVUS_PORT"),
            },
            # drop_old=True
        )
        logger.info(f"Successfully connected to Milvus collection: {collection_name}")
        return milvus_db
    except Exception as e:
        logger.error(f"Error initializing Milvus connection: {e}")
        return None

def get_retriever(collection_name: Optional[Union[str, Any]]) -> None:
    """
    Get a retriever for a given collection name.

    Args:
        collection_name (str): The name of the collection to get a retriever for.

    Returns:
        Retriever: A retriever for the given collection name.
    """
    milvus_instance = get_milvus_instance(collection_name)
    if milvus_instance:
        return milvus_instance.as_retriever(search_type='mmr', search_kwargs={"k": 15}, lambda_mult=1)
    return None
