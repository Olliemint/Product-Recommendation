# 🛍️ Product Recommendation API

This is a Django REST API for retrieving product information and generating personalized product recommendations using a content-based recommendation approach.

---



## 🚀 Setup Instructions

### 1. **Clone the Repository**

```bash
git clone https://github.com/Olliemint/Product-Recommendation.git
cd Product-Recommendation

```


### 2. **Install Dependencies**
Create and activate a virtual environment:

### Prerequisites
- Python 3.8+
- SQLite

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install required packages:
```bash
pip install -r requirements.txt
```

### Apply Migrations:
```bash
python manage.py migrate
```
### Run the Development Server
```bash
python manage.py runserver
```

    
## 📦 API Endpoints


#### Get all products

```http
  GET /products/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `category` | `string` | List all products (optionally filter by category) |

#### Get product

```http
  GET /products/<id>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Retrieve a single product by ID |

#### Get recommendations

```http
  POST /recommendations/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `viewed_product_ids`      | `number[]` | Get product recommendations based on viewed products |


## 🤖 Recommendation Logic

The recommendation system uses a content-based filtering approach:

- Text Representation : Each product is represented as a string combining its category, tags, and name.

- Vectorization : These product texts are converted into vectors using TF-IDF (Term Frequency–Inverse Document Frequency).

- Similarity Scoring: For the provided list of viewed product IDs, an average TF-IDF vector is computed.
- Cosine similarity is used to measure similarity between this average vector and all other products.

- Ranking: Products not in the viewed list are sorted by similarity score. The top 3 most similar products are returned.

- Fallback :If no viewed products are provided, 3 random products are returned.


## ✅ Assumptions

- Each product has meaningful values for category, tags, or name.

- Up to 3 recommendations are returned per request.

- The system does not use collaborative filtering or user-specific preferences beyond the viewed product IDs.

- Product data is already present in the database and accessible via Django ORM.




## 📩 Example Recommendation Request

### Request
```http
POST /recommendations/
Content-Type: application/json

{
  "viewed_product_ids": [1, 2, 3]
}
```

### Response
```json
{
  "message": "Since you viewed Electronics, Books you might like these",
  "recommendations": [
    {
      "id": 5,
      "name": "Wireless Mouse",
      "category": "Electronics",
      ...
    },
    ...
  ]
}
```


## Tech Stack

- Python 3

- Django & Django REST Framework

- scikit-learn (TF-IDF + Cosine Similarity)

- SQLite



