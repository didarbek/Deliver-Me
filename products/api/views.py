# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_product_review(request):
#     serializer = ProductReviewSerializer(data={
#         'title': request.data['title'],
#         'description': request.data['description'],
#         'rating': request.data['rating'],
#         'product': request.data['product'],
#         'author': request.user.id
#     })
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['DELETE'])
# @permission_classes([IsReviewAuthorOrReadOnly])
# def delete_product_review(request, review_id: int):
#     review = get_object_or_404(ProductReview, id=review_id)
#
#     review.delete()
#
#     return Response({'message': 'Your review have been successfully deleted.'})


# @api_view(['PUT'])
# @permission_classes([IsAuthorOrReadOnly])
# def update_product(request, product_id: int):
#     product = get_object_or_404(Product, id=product_id)
#     serializer = ProductSerializer(product, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
