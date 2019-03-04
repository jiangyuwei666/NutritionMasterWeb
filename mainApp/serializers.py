from rest_framework import serializers
from mainApp.models import *


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class CookQuantitySerializer(serializers.ModelSerializer):
    # 这两行都可以注释掉,用默认值
    menu = serializers.ReadOnlyField(source='menu.name')
    material = serializers.ReadOnlyField(source='material.material_name')

    class Meta:
        model = CookQuantity
        # fields = '__all__'
        fields = ('menu', 'quantity', 'material')


class MenuClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuClassification
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    # many to many 关系中要用source指定数据来源
    cook_quantity = CookQuantitySerializer(source='cookquantity_set', many=True, read_only=True)  # 重写字段,用于展示详细信息
    # menu_classification = MenuClassificationSerializer(source='menuclassification_set',many=True,read_only=True) # 分类的超级详细信息
    menuclassification_set = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    elements = ElementSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = (
            'flavor', 'calorie', 'name','is_breakfast','technology', 'image_url', 'cook_quantity', 'practice',
            'menuclassification_set', 'elements',)
        # fields = '__all__'


class MenuSerializerLighter(serializers.ModelSerializer):
    """
    轻量级的MenuSerializer
    """

    class Meta:
        model = Menu
        fields = ('name', 'calorie', 'elements','image_url')


class FoodMaterialSerializer(serializers.ModelSerializer):
    elements = ElementSerializer(read_only=True)
    cook_quantity = CookQuantitySerializer(source='cookquantity_set', many=True, read_only=True)  # 重写字段,用于展示详细信息

    class Meta:
        model = FoodMaterial
        fields = ('material_name', 'cook_quantity', 'elements')


class OccupationSerializer(serializers.ModelSerializer):
    menuclassification_set = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    elements = ElementSerializer(read_only=True)

    class Meta:
        model = Occupation
        fields = ('occupation_name', 'menuclassification_set', 'elements', 'bmi_classification')


class PhysiqueSerializer(serializers.ModelSerializer):
    cure_material = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    elements = ElementSerializer(read_only=True)

    class Meta:
        model = Physique
        fields = ('physical_name', 'cure_material', 'elements')


class MyUserSerializer(serializers.ModelSerializer):
    # occupation_name = OccupationSerializer(source='occupation_set', many=False, read_only=False)
    # physical_name = PhysiqueSerializer(many=False, read_only=False)
    eaten_elements = ElementSerializer(read_only=True)

    physical_name = serializers.PrimaryKeyRelatedField(
        allow_empty=True,
        allow_null=True,
        required=False,
        many=False,
        read_only=False,
        queryset=Physique.objects.all()
    )

    class Meta:
        model = MyUser
        fields = '__all__'


class IllnessSerializer(serializers.ModelSerializer):
    menu_classification = MenuClassificationSerializer(read_only=True)
    elements = ElementSerializer(read_only=True)

    class Meta:
        model = Illness
        fields = ('menu_classification', 'elements')


class TrickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trick
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    menu = MenuSerializerLighter(read_only=True)
    class Meta:
        model = History
        fields = '__all__'
