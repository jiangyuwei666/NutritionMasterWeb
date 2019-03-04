from django.test import TestCase

from mainApp.models import FoodMaterial
from utils.read_dataset import *


class MaterialModelTests(TestCase):
    def material_name_repeat_save(self):
        """
        测试存储名字重复的FoodMaterial对象
        :return:
        """
        for i in range(4):
            FoodMaterial.objects.create(material_name='花生米')
        self.assertEquals(FoodMaterial.objects.count(), 1)

    def read_data(TestCase):
        """
        测试读入正常csv数据,添加表连接
        :return:
        """
        parse_menu()
