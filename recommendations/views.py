from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from recommendations.recommendation import get_recommendations
from .models import Product
from .serializers import ProductSerializer


class ProductListView(APIView):
    def get(self, request):
        # query params
        category = request.query_params.get('category', None)

        queryset = Product.objects.all()

        if category:
            queryset = queryset.filter(
                # Exact match 
                Q(category__iexact=category) |
                Q(category__icontains=category)  # Partial match
            ).distinct()

        serializer = ProductSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
            'filters': {
                'category': category
            }
        })


class RecommendationView(APIView):
    def post(self, request):
        viewed_product_ids = request.data.get('viewed_product_ids', [])
        if not isinstance(viewed_product_ids, list):
            return Response({"error": "viewed_product_ids must be a list"}, status=400)

        all_products = Product.objects.all()
        recommendations = get_recommendations(viewed_product_ids, all_products)

        viewed_categories = (
            Product.objects
            .filter(id__in=viewed_product_ids)
            .values_list('category', flat=True)
            .distinct()
        )
        categories = list(viewed_categories)
        message = "Recommended products for you"
        if categories:
            message = f"Since you viewed {', '.join(categories)} you might like these"

        serializer = ProductSerializer(recommendations, many=True)
        return Response({
            "message": message,
            "recommendations": serializer.data
        })

        
class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
