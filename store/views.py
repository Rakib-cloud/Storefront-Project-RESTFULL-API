
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.serializers import CollectionSerializer
from .models import Collection, Product
from .serializers import ProductSerializer


#=============================================================================================================
#Product List View,GET,POST
#=============================================================================================================
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
     queryset = Product.objects.select_related('collection').all() # get all products from database
     serializer = ProductSerializer(queryset, many=True, context={'request': request}) # serialize the product objects and pass many=True since it's a queryset
     return Response(serializer.data)
    
    elif request.method == 'POST':
        #Option 1: using raise_exception=True
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data # access the validated data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        #Option 2: using if-else block
        # OR you can do it this way too
        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response('ok')
        #     # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=============================================================================================================
#Product Detail View,GET,PUT,PATCH
#=============================================================================================================
@api_view(['GET','PUT','DELETE'])
def product_detail(request, id):
    product=get_object_or_404(Product, pk=id)
    #Option 1: using get_object_or_404 shortcut Get one object otherwise response set 404 not found
    if request.method=='GET':
        serializer=ProductSerializer(product) 
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data) #deserialize
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.orderitem_set.exists():
         return Response({"error":'Product can not be deleted associated with a product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
         product.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

   







# Option 2: you can use try-except block instead of get_object_or_404  ===FOR GET ONE OBJECT
#    try:
#      product=Product.objects.get(pk=id) # get product by id from database
#      serializer=ProductSerializer(product) #serialize the product object pass it to serializer
#      return Response(serializer.data) # return serialized data as json response
#    except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


#===============================================================================================================
#collection list (GET,POST)
#===============================================================================================================
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=============================================================================================================
# Collection Detail View (GET, PUT, DELETE)
#=============================================================================================================
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Optionally prevent deletion if there are products under this collection
        if collection.product_set.exists():
            return Response(
                {"error": "Cannot delete collection that contains products."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)