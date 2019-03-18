from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Element(models.Model):
    """
    营养元素,id为主码
    """
    calorie = models.FloatField(default=0)
    carbohydrate = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    cellulose = models.FloatField(default=0)
    vitaminA = models.FloatField(default=0)
    vitaminB1 = models.FloatField(default=0)
    vitaminB2 = models.FloatField(default=0)
    vitaminB6 = models.FloatField(default=0)
    vitaminC = models.FloatField(default=0)
    vitaminE = models.FloatField(default=0)
    carotene = models.FloatField(default=0)
    cholesterol = models.FloatField(default=0)
    Mg = models.FloatField(default=0)
    Ca = models.FloatField(default=0)
    Fe = models.FloatField(default=0)
    Zn = models.FloatField(default=0)
    Cu = models.FloatField(default=0)
    Mn = models.FloatField(default=0)
    K = models.FloatField(default=0)
    P = models.FloatField(default=0)
    Na = models.FloatField(default=0)
    Se = models.FloatField(default=0)
    niacin = models.FloatField(default=0)
    thiamine = models.FloatField(default=0)

    def __add__(self, other):
        calorie = (self.calorie + other.calorie)
        carbohydrate = self.carbohydrate + other.carbohydrate
        fat = self.fat + other.fat
        protein = self.protein + other.protein
        cellulose = self.cellulose + other.cellulose
        vitaminA = self.vitaminA + other.vitaminA
        vitaminB1 = self.vitaminB1 + other.vitaminB1
        vitaminB2 = self.vitaminB2 + other.vitaminB2
        vitaminB6 = self.vitaminB6 + other.vitaminB6
        vitaminC = self.vitaminC + other.vitaminC
        vitaminE = self.vitaminE + other.vitaminE
        carotene = self.carotene + other.carotene
        cholesterol = self.cholesterol + other.cholesterol
        Mg = self.Mg + other.Mg
        Ca = self.Ca + other.Ca
        Fe = self.Fe + other.Fe
        Zn = self.Zn + other.Zn
        Cu = self.Cu + other.Cu
        Mn = self.Mn + other.Mn
        K = self.K + other.K
        P = self.P + other.P
        Na = self.Na + other.Na
        Se = self.Se + other.Se
        niacin = self.niacin + other.niacin
        thiamine = self.thiamine + other.thiamine
        return Element(
            calorie=calorie,
            carbohydrate=carbohydrate,
            fat=fat,
            protein=protein,
            cellulose=cellulose,
            vitaminA=vitaminA,
            vitaminB1=vitaminB1,
            vitaminB2=vitaminB2,
            vitaminB6=vitaminB6,
            vitaminC=vitaminC,
            vitaminE=vitaminE,
            carotene=carotene,
            cholesterol=cholesterol,
            Mg=Mg,
            Ca=Ca,
            Fe=Fe,
            Zn=Zn,
            Cu=Cu,
            Mn=Mn,
            K=K,
            P=P,
            Na=Na,
            Se=Se,
            niacin=niacin,
            thiamine=thiamine)


class Occupation(models.Model):
    """
    职业
    """
    occupation_name = models.CharField(max_length=16, unique=True, primary_key=True)
    elements = models.OneToOneField(Element, on_delete=models.CASCADE, null=True, blank=True)
    bmi_classification = models.IntegerField(default=-1)

    def __str__(self):
        return self.occupation_name


class FoodMaterial(models.Model):
    """
    食材
    """
    material_name = models.CharField(max_length=64, primary_key=True)
    elements = models.OneToOneField(Element, on_delete=models.CASCADE, null=True, blank=True)

    # material_effect = models.ManyToManyField(Physique, through='MaterialEffect')  # 食材_效果_体质

    def __str__(self):
        return self.material_name


class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=128, primary_key=True)
    # physical_name = models.ForeignKey(Physique, on_delete=models.CASCADE, blank=True, null=True)
    calorie = models.IntegerField(default=-1)
    minutes = models.IntegerField(default=0)
    flavor = models.CharField(max_length=64)
    technology = models.CharField(max_length=16)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    practice = models.TextField(default='')
    cook_quantity = models.ManyToManyField(FoodMaterial, through='CookQuantity')  # 菜谱_做菜用量_食材
    elements = models.OneToOneField(Element, on_delete=models.CASCADE, null=True, blank=True)
    is_breakfast = models.IntegerField(default=0)  # 1是早餐,0是午晚餐   默认为0

    def __str__(self):
        return self.name


class MenuClassification(models.Model):
    """
    菜谱的功能分类
    """
    classification = models.CharField(max_length=16, primary_key=True)  # 分类名称
    cure_occupation = models.ManyToManyField(Occupation, blank=True, null=True)  # 菜谱功能分类_可治愈的职业_特殊职业
    menu_effect = models.ManyToManyField(Menu)

    def __str__(self):
        return self.classification


class Physique(models.Model):
    """
    体质
    """
    physical_name = models.CharField(max_length=64, primary_key=True)
    cure_material = models.ManyToManyField(FoodMaterial, blank=True, null=True)
    elements = models.OneToOneField(Element, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.physical_name


class Illness(models.Model):
    menu_classification = models.OneToOneField(MenuClassification, primary_key=True, on_delete=models.CASCADE)
    elements = models.OneToOneField(Element, on_delete=models.CASCADE, null=True, blank=True)


# class MaterialEffect(models.Model):
#     """
#     食材效果
#     """
#     food_material = models.ForeignKey(FoodMaterial, on_delete=models.CASCADE)
#     physique = models.ForeignKey(Physique, on_delete=models.CASCADE)
#     material_effect = models.IntegerField()
#
#     def __str__(self):
#         return self.food_material.material_name + " " + str(self.material_effect) + " " + self.physique.physical_name


class CookQuantity(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    material = models.ForeignKey(FoodMaterial, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.menu.name + " -- " + self.material.material_name + " -- " + str(self.quantity)

    class Meta:
        unique_together = ('menu', 'material')


#
# class PhysicalProperty(models.Model):
#     """
#     体质性状
#     """
#     property_name = models.CharField(max_length=64, primary_key=True)
#     physical_state = models.ManyToManyField(Physique)
#
#     def __str__(self):
#         return self.property_name


class MyUser(AbstractUser):
    physical_name = models.ForeignKey(Physique, on_delete=models.CASCADE, blank=True, null=True)
    occupation_name = models.ForeignKey(Occupation, on_delete=models.CASCADE, blank=True, null=True)
    sex = models.IntegerField(default=1)
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    illness = models.ManyToManyField(Illness, blank=True, null=True)
    bmi = models.IntegerField(default=-1)
    eaten_elements = models.OneToOneField(Element, on_delete=models.SET_NULL, null=True, blank=True)  # 已经吃过的营养元素量
    menu_history = models.ManyToManyField(Menu, through='History', blank=True, null=True)

    def __str__(self):
        return self.username


class Trick(models.Model):
    title = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title


class History(models.Model):
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(MyUser, on_delete=True)
    menu = models.ForeignKey(Menu, on_delete=True)

    def __str__(self):
        return self.user.username + ' ' + self.menu.name + ' ' + self.time.__str__()


class UploadFile(models.Model):
    file = models.FileField(upload_to='mainapp/media')

    def __str__(self):
        return self.file
