import shutil

import pandas as pd
from mainapp.models import Occupation, FoodMaterial, Menu, CookQuantity, MenuClassification, Physique
import os
import django

os.environ.setdefault('DJANGO_SETTING_MODULE', 'mydjango.settings')
django.setup()

data_set_dir = 'C:\\Users\\Administrator\\Documents\\Study\\foodset\\'


# done
def parse_physique():
    list = ['瘀血质', '阴虚质', '阳虚质', '痰湿质', '湿热质', '气郁质', '气虚质', '平和质']
    for str in list:
        Physique.objects.create(physical_name=str)


def parse_physique_material():
    """
    解析体质-食材关系
    """
    table = pd.read_csv(data_set_dir + 'physique_material.csv', encoding='gbk')
    for i in range(len(table)):
        physique = Physique.objects.get(physical_name=table.loc[i]['physique'])
        material_str = table.loc[i]['material']
        if (type(material_str) is str):
            material_list = material_str.split('、')
            for material_name in material_list:
                # materials是QuerySet集合
                materials = FoodMaterial.objects.filter(material_name__contains=material_name)
                for material in materials:
                    physique.cure_material.add(material)
                    physique.save()


def parse_occupation_classification():
    """
    特殊职业和菜谱功能
    """
    file_path = data_set_dir + 'occupation_classification_new.csv'
    table = pd.read_csv(file_path, encoding='gbk')
    for i in range(len(table)):
        occupation_str = table.loc[i]['occupation'].strip()
        class_list = table.loc[i]['classification'].strip().split(',')
        occupation = Occupation(occupation_name=occupation_str)
        occupation.save()
        print(class_list)
        for class_str in class_list:
            if (not class_str.__eq__('')):
                menu_classification = MenuClassification.objects.get(classification=class_str)
                menu_classification.cure_occupation.add(occupation)
                menu_classification.save()


def parse_menu():
    """
    :param filename: 菜谱csv
    读取菜单csv的数据,填入的表:
    菜谱-做菜-食材表
    菜谱-效果-菜谱功能分类表
    :return:
    """
    dir = data_set_dir + 'menuset'
    done_move_dir = data_set_dir + 'done\\'

    csv_list = os.listdir(dir)
    menu_count = 0

    for menu_file in csv_list:
        print('log menu_file: ', menu_file)
        file_path = dir + '\\' + menu_file
        table = pd.read_csv(file_path, encoding='gbk', engine='python')
        table_size = len(table)
        for i in range(table_size):
            name = table['菜名'][i]

            menu_count += 1
            print('log ', menu_count, name)

            # calorie = table['卡路里'][i]
            calorie = -1
            flavor = table['口味'][i]
            technology = table['主要工艺'][i]
            practice = table['做法'][i]
            # image_url = table['图片url'][i]
            image_url = ''
            material_str = table['食材'][i]
            classification_str = table['分类'][i]

            menu = Menu(name=name, calorie=calorie, flavor=flavor, technology=technology,
                        practice=practice, image_url=image_url)
            try:
                menu.save()
            except Exception as e:
                print(menu.name, e)

            # 处理菜谱和食材,做菜之间的关系
            material_dict = get_material_and_quantity_dict(material_str)
            for material_name, quantity_str in material_dict.items():  # 遍历每个食材
                food_material = FoodMaterial(material_name=material_name)
                food_material.save()
                cook_quantity = CookQuantity(menu=menu, material=food_material, quantity=quantity_str)
                try:
                    cook_quantity.save()
                except Exception as e:
                    pass

            # 处理菜谱和功能分类之间的关系
            classification_list = get_classification_list(classification_str)
            for class_name in classification_list:
                menu_classification = MenuClassification(classification=class_name)
                menu_classification.save()
                menu_classification.menu_effect.add(menu)

            # 把读完后的文件放到另一个文件夹
            if (i + 1 == table_size):
                print('done ' + file_path + " move to " + done_move_dir)
                shutil.move(file_path, done_move_dir)


def get_classification_list(str):
    """
    ,川菜,老人食谱,不孕不育食谱,肾调养食谱

    把如上字符串解析为list
    """
    str = str.strip()
    list = str.split(',')
    list = list[1:]  # 去掉第一个空的
    return list


def get_material_and_quantity_dict(str):
    """
    ,150克:对虾,100克:花生仁(炸),50克:黄瓜

    把如上字符串解析为 {对虾:150, 花生仁(炸):100}的dict
    """
    dict = {}
    str = str.strip()
    list = str.split(',')
    for s in list:
        if not s.__eq__(''):
            map = s.split(':')
            if len(map) != 2:
                continue
            quantity = map[0]
            name = map[1]
            dict[name] = quantity
    return dict


# done
def create_occupation():
    """
    创建职业,done
    :return:
    """
    # list = ['农牧业','渔业','矿业','交通运输业','餐旅业','建筑工程业','制造业','新闻、出版、广告业','卫生','教师','金融业','IT业','体育']
    list = ['教师', '记者', '演员', '厨师', '医生', '护士', '司机', '军人', '律师', '商人', '会计', '程序员', '服务员', '作家', '模特', '导游', '歌手',
            '裁缝',
            '翻译', '法官', '保安', '花匠', '清洁工', '理发师', '消防员', '推销员', '运动员', '快递员', '外卖员', '主持人', '漫画家', '面点师', '美甲师', '保姆',
            '电力工程师', '化验员', '机长', '空姐', '画师', '动漫设计', '白领', '前台', '学生']
    for str in list:
        Occupation.objects.create(occupation_name=str)


def test_read_menu_file(filename):
    file_path = data_set_dir + 'menuset\\' + filename
    table = pd.read_csv(file_path, encoding='gbk', engine='python')
    table_size = len(table)
    done_move_dir = data_set_dir + 'done\\'

    menu_count = 0
    for i in range(table_size):
        name = table['菜名'][i]

        # calorie = table['卡路里'][i]
        calorie = -1
        flavor = table['口味'][i]
        technology = table['主要工艺'][i]
        practice = table['做法'][i]
        # image_url = table['图片url'][i]
        image_url = ''
        material_str = table['食材'][i]
        classification_str = table['分类'][i]

        menu = Menu(name=name, calorie=calorie, flavor=flavor, technology=technology,
                    practice=practice, image_url=image_url)
        try:
            menu.save()
            menu_count += 1
            print('log ', menu_count, name)
        except Exception as e:
            print(menu.name, e)

        # 处理菜谱和食材,做菜之间的关系
        material_dict = get_material_and_quantity_dict(material_str)
        for material_name, quantity_str in material_dict.items():  # 遍历每个食材
            food_material = FoodMaterial(material_name=material_name)
            food_material.save()
            cook_quantity = CookQuantity(menu=menu, material=food_material, quantity=quantity_str)
            try:
                cook_quantity.save()
            except Exception as e:
                pass

        # 处理菜谱和功能分类之间的关系
        classification_list = get_classification_list(classification_str)
        for class_name in classification_list:
            menu_classification = MenuClassification(classification=class_name)
            menu_classification.save()
            menu_classification.menu_effect.add(menu)

        # 把读完后的文件放到另一个文件夹
        if (i + 1 == table_size):
            print('done ' + file_path + " move to " + done_move_dir)
            shutil.move(file_path, done_move_dir)


def parse_menu_calorie_and_url():
    """
    收尾工作,读取一下url和卡路里
    """
    data_set_dir = 'C:\\Users\\Administrator\\Documents\\Study\\foodsetfinal\\'
    dir = data_set_dir + 'menu'
    done_move_dir = data_set_dir + 'done\\'

    csv_list = os.listdir(dir)
    menu_count = 0

    for menu_file in csv_list:
        print('log menu_file: ', menu_file)
        file_path = dir + '\\' + menu_file
        table = pd.read_csv(file_path, encoding='gbk', engine='python')
        table.fillna(0, inplace=True)
        table_size = len(table)
        for i in range(table_size):
            name = table['菜名'][i]
            menu_count += 1
            print('log ', menu_count, name)
            calorie = table['卡路里'][i]
            image_url = table['图片url'][i]
            menu = Menu.objects.filter(name=name)
            # 判断是不是没存这个菜
            if (menu.count() == 0):
                name = table['菜名'][i]
                calorie = table['卡路里'][i]
                flavor = table['口味'][i]
                technology = table['主要工艺'][i]
                practice = table['做法'][i]
                image_url = table['图片url'][i]
                material_str = table['食材'][i]
                classification_str = table['分类'][i]
                menu = Menu(name=name, calorie=calorie, flavor=flavor, technology=technology,
                            practice=practice, image_url=image_url)
                try:
                    menu.save()
                except Exception as e:
                    print(menu.name, e)
                # 处理菜谱和食材,做菜之间的关系
                material_dict = get_material_and_quantity_dict(material_str)
                for material_name, quantity_str in material_dict.items():  # 遍历每个食材
                    food_material = FoodMaterial(material_name=material_name)
                    food_material.save()
                    cook_quantity = CookQuantity(menu=menu, material=food_material, quantity=quantity_str)
                    try:
                        cook_quantity.save()
                    except Exception as e:
                        pass
                # 处理菜谱和功能分类之间的关系
                classification_list = get_classification_list(classification_str)
                for class_name in classification_list:
                    menu_classification = MenuClassification(classification=class_name)
                    menu_classification.save()
                    menu_classification.menu_effect.add(menu)
            else:
                menu = menu[0]
                if calorie == '海鲜焗饭':
                    calorie = -1
                menu.calorie = int(calorie)
                menu.image_url = image_url
                try:
                    menu.save()
                except Exception as e:
                    print(menu.name, e)

            # 把读完后的文件放到另一个文件夹
            if (i + 1 == table_size):
                print('done ' + file_path + " move to " + done_move_dir)
                shutil.move(file_path, done_move_dir)
