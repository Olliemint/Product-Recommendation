from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random


def build_product_text(product):
    """
    Combines product features into a single text string for analysis.
    This helps us compare products based on their combined attributes.
    
    Args:
        product: The product object containing category, tags, and name
    
    Returns:
        A single string combining all searchable features of the product
    """
    category = product.category or ""  # Handle empty categories gracefully
    # Combine tags if they exist
    tags = " ".join(product.tags) if product.tags else ""
    name = product.name or ""  # Ensure we always have a name
    # The "signature" we'll use to compare products
    return f"{category} {tags} {name}"


def get_recommendations(viewed_product_ids, all_products):
    """
    Generates product recommendations based on what a user has viewed.
    The magic happens in three steps:
    1. Convert products to comparable text features
    2. Find mathematical similarity between products
    3. Pick the best matches the user hasn't seen yet
    
    Args:
        viewed_product_ids: List of product IDs the user has viewed
        all_products: QuerySet of all available products
    
    Returns:
        List of 3 recommended product objects
    """

    # Convert Django QuerySet to list 
    products_list = list(all_products)

    # Step 1: Create "product fingerprints" - text representations we can compare
    product_texts = [build_product_text(p) for p in products_list]

    # Step 2: Convert text to numbers using TF-IDF (Term Frequency-Inverse Document Frequency)
    # This helps us understand which words are important for each product
    vectorizer = TfidfVectorizer()
    # Our numerical product representations
    tfidf_matrix = vectorizer.fit_transform(product_texts)

    # Create a roadmap to connect product IDs to their position in our matrix
    product_id_to_index = {p.id: idx for idx, p in enumerate(products_list)}

    # Find which of the viewed products actually exist in our database
    viewed_indices = [
        product_id_to_index[pid]
        for pid in viewed_product_ids
        if pid in product_id_to_index
    ]

    # Handle new users or empty history by showing random popular products
    if not viewed_indices:
        return random.sample(products_list, min(3, len(products_list)))

    # Step 3: Find the "average flavor" of what the user likes
    # We combine all viewed products into one average profile
    avg_vector = np.asarray(tfidf_matrix[viewed_indices].mean(axis=0))

    # Step 4: Compare this average to all products using cosine similarity
    # (Measures the angle between vectors - perfect match = 1, no similarity = 0)
    similarities = cosine_similarity(
        avg_vector.reshape(1, -1),  # Our user's taste profile
        tfidf_matrix                # All products
    ).flatten()

    # Step 5: Sort products by similarity score (best matches first)
    # [::-1] reverses for descending order
    ranked_indices = similarities.argsort()[::-1]
    recommended_products = []

    # Pick the top 3 products they haven't viewed
    for idx in ranked_indices:
        idx_int = int(idx)  # Convert numpy number to regular Python integer
        candidate = products_list[idx_int]

        # Only recommend products they haven't seen and we haven't already picked
        if (candidate.id not in viewed_product_ids and
                candidate not in recommended_products):
            recommended_products.append(candidate)

            # Stop when we have our 3 recommendations
            if len(recommended_products) == 3:
                break

    return recommended_products
