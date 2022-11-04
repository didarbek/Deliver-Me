from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from products.models import ProductQuestion
from products.api.serializers.product_question_serializers import ProductQuestionSerializer


class ProductQuestionCreateAPIView(generics.CreateAPIView):
    queryset = ProductQuestion.objects.all()
    serializer_class = ProductQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductQuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = ProductQuestion.objects.all()
    serializer_class = ProductQuestionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if instance.user == request.user or request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response('You are not allowed to do this action', status=status.HTTP_403_FORBIDDEN)


class ProductQuestionDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ProductQuestionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = ProductQuestion.objects.filter(id=self.kwargs['id'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response('Your question has been successfully removed from the product.', status=status.HTTP_200_OK)

        return Response('You are not allowed to do this action', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_question(request):
    question = get_object_or_404(ProductQuestion, id=request.POST.get('question'))
    is_liked = False
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
        question.votes -= 1
        question.save()
        is_liked = False
    else:
        if question.dislikes.filter(id=request.user.id).exists():
            question.dislikes.remove(request.user)
            question.votes += 1
            question.save()
        question.likes.add(request.user)
        question.votes += 1
        question.save()
        is_liked = True

    serializer = ProductQuestionSerializer(question)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_question(request):
    question = get_object_or_404(ProductQuestion, id=request.POST.get('question'))
    is_disliked = False
    if question.dislikes.filter(id=request.user.id).exists():
        question.dislikes.remove(request.user)
        question.votes += 1
        question.save()
        is_disliked = False
    else:
        if question.likes.filter(id=request.user.id).exists():
            question.likes.remove(request.user)
            question.votes -= 1
            question.save()
        question.dislikes.add(request.user)
        question.votes -= 1
        question.save()
        is_disliked = True

    serializer = ProductQuestionSerializer(question)

    return Response(serializer.data, status=status.HTTP_200_OK)