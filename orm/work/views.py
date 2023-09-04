from collections import UserDict
from pstats import Stats
import statistics
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from . models import Hero,Villain


from .models import Category, Comment, Like, Post
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    LikeSerializer,
    PostSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['POST'])
    def create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug')
        description_data = data.validated_data.get('description')

        obj = Category.objects.create(
            description = description_data, slug = slug_data, title = title_data
        )
        serializer = self.serializer_class(obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def save_data(self, request, *args, **kwargs):

        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug')
        description_data = data.validated_data.get('description')

        obj = Category()
        obj.title = title_data
        obj.slug = slug_data
        obj.description = description_data
        obj.save()

        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['POST'])
    def get_or_create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None)
        data.is_valid(raise_exception=True)

        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug')

        obj, _ =Category.objects.get_or_create(title=title_data, slug=slug_data)

        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    @action(detail=False, methods=['POST'])
    def bulk_create_data(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data or None, many=True)
        data.is_valid(raise_exception=True)

        new_data = []
        for row in data.validated_data:
                new_data.append(
                    Category(
                    title = row['title'],
                    slug = row['slug'],
                    description = row['description']
                    )
                )

        if new_data:
           new_data = Category.objects.bulk_create(new_data)
        

        return Response("successfully created data" ,status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['PATCH'])
    def add_category(self, request, pk, *args, **kwargs):
        
        categories_data = request.data.get("ids")

        instance = Post.objects.filter(pk=pk).first()

        # inefficient
        # for category in catagories:
        #     instance.category.add(category)

        categories_data = set(categories_data)
        instance.category.add(*categories_data)

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['PATCH'])
    def set_category(self, request, pk, *args, **kwargs):

        
        categories_data = request.data.get("ids")

        instance = Post.objects.filter(pk=pk).first()

        # instance.category.clear()
        # categories_data = set(categories_data)
        # instance.category.add(*categories_data)

        instance.category.set(categories_data)

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


from django.db.models import Q
class orm_document(viewsets.ModelViewSet):

    qs = User.objects.filter(Q(first_name__startswith='R')|Q(last_name__startswith='D'))#or
    queryset_3 = User.objects.filter(Q(first_name__startswith='R') & Q(last_name__startswith='D'))#and
    queryset = User.objects.filter(~Q(id__lt=5)) #not
    #union of two querysets from same or different models
    Hero.objects.all().values_list("fist_name", "last_name").union(Villain.objects.all().values_list("fist_name", "last_name"))

    # select some fields only in a queryset
    queryset = User.objects.filter(first_name__startswith='R').only("first_name", "last_name")
