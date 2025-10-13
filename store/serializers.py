from decimal import Decimal
from rest_framework import serializers
from store.models import Product,Collection


#model serializer for collection
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title'] # include products_count field in json response



#Normal Serializer
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
    


#Model Serializer
class ProductSerializer(serializers.ModelSerializer):
    #using meta class to specify model and fields to show in json response
    class Meta:
        model = Product #automatically this model create a serializer with all fields of Product model
        fields = ['id', 'title','description','slug','inventory', 'unit_price', 'price_with_tax', 'collection'] #specify fields to include in json response
        # fields = '__all__' # to include all fields of Product model
        # exclude = ['description'] # to exclude specific fields from json response
    # collection=CollectionSerializer()
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
        


# #Normal Serializer
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price=serializers.DecimalField(max_digits=6, decimal_places=2,source='unit_price')
#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')

#     #for collection object within product
#     collection=CollectionSerializer()

#     # For HyperlinkedRelatedField to work for each product's collection
#     # collection=serializers.HyperlinkedRelatedField(
#     #     queryset=Collection.objects.all(),
#     #     view_name='collection-detail'
#     # )
   

## Method to calculate tax
    def calculate_tax(self, product: Product):
        return product.unit_price * (Decimal('0.1'))