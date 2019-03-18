from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import *


#
# class MenuList(APIView)
#     def get(self,request,format=None):
#         menu = Menu.objects.all()
#         serializer = MenuSerializer(menu, many=True)
#         return Response(serializer.data)
#
#     def post(self,request,format=None):
#         print('log',request.data)
#         return Response(request.data)
#
#
# class MenuList(generics.ListAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#
#     def get(self, request, *args, **kwargs):
#         """
#         list函数自动返回字段queryset的serializer对象
#         """
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print('log', request.data)
#         return Response(request.data)
#
#
# class MenuDetail(generics.RetrieveAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
#     lookup_field = 'name'
#
#     def get(self, request, *args, **kwargs):
#         # menu = Menu.objects.get(name=self.kwargs['name'])
#         serializer = MenuSerializer(context={'request': request})
#         return Response(serializer.data)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    传入的pk值为菜名,查询菜的信息和做菜方法
    ReadOnlyViewSet提供list和detail
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        模糊  搜索菜,返回菜list
        """
        menu_name = kwargs['pk']
        menus = Menu.objects.filter(name__icontains=menu_name)
        i = 0
        while menus.count() == 0:  # 如果搜不到这个菜,就减一下名字
            menu_name = menu_name[1:] if i % 2 == 0 else menu_name[:-1]
            print(menu_name)
            i += 1
            menus = Menu.objects.filter(name__icontains=menu_name)
        menu = menus[0] if menus.count() > 0 else Menu()
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_random_menus(self, request):
        """
        根据user信息和推荐算法推荐菜
        :param request:
        :return:
        """
        import numpy as np
        menus_count = request.GET['count']  # 希望获取几个菜
        menus_count = int(menus_count)

        username = request.GET.get('username', 'zhaolizhi')  # 通过username查询用户的病,体质,职业,默认username为zhaolizhi
        user = MyUser.objects.get(username=username)

        if user.illness.all().count() is not 0:  # 如果病的数量不为0
            user_message_list = [user.illness.all(), user.occupation_name, user.physical_name]
        else:
            user_message_list = [user.occupation_name, user.physical_name]
            print('here', user_message_list)
        user_message_list = [message for message in user_message_list if message is not None]  # 去除掉user信息里面None的值

        # if (len(user_message_list) == 0 and hasattr(user_message_list[0], 'count') and user_message_list[
        #     0].count() == 0):  # 如果三个属性都是空
        if len(user_message_list) == 0:
            print('三个属性都是None')
            menus = Menu.objects.all()
        else:  # 如果体质 病理 职业都为空
            # 等概率推荐,随机从非空的病,体质,职业中抽取一个
            random_flag = np.random.randint(len(user_message_list))
            random_message = user_message_list[random_flag]
            if isinstance(random_message, Physique.objects.all()[0]):
                # Physique
                materials = random_message.cure_material.all()
                random_material = materials[np.random.randint(materials.count())]
                menus = random_material.menu_set.all()
            elif isinstance(random_message, Occupation.objects.all()[0]):
                # Occupation
                classifications = random_message.menuclassification_set.all()
                random_classification = classifications[np.random.randint(classifications.count())]
                menus = random_classification.menu_effect.all()
            else:
                # many illness
                illness_count = random_message.count()
                illness = random_message[np.random.randint(illness_count)]
                menus = illness.menu_classification.menu_effect.all()

        menus_count = menus_count if menus_count < menus.count() else menus.count()  # 希望选取的个数
        random_menus = np.random.choice(np.array(menus), menus_count)  # 从已有的menus中随机选出几个
        serializer = MenuSerializer(random_menus, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'])
    def get_menus_by_elements(self, request):
        """
        返回营养元素为0-elements 范围的菜谱
        :param request:
        :return:
        """
        import time
        localtime = time.localtime()
        week = int(time.strftime("%w", localtime))
        # 返回每天的营养元素允许量(本周剩下的量 / 本周剩余的天数)
        week_denominator = (7 - week + 1) if week != 0 else 1  # week = 0是周日,周日就不用处理了,直接分母为1

        # 通过传入的参数构造sql查询字符串
        post = request.POST
        menus = None
        sql = 'SELECT "mainapp_menu"."name", "mainapp_menu"."calorie", "mainapp_menu"."minutes", "mainapp_menu"."flavor", "mainapp_menu"."technology", "mainapp_menu"."image_url", "mainapp_menu"."practice", "mainapp_menu"."elements_id" FROM "mainapp_menu" INNER JOIN "mainapp_element" ON ("mainapp_menu"."elements_id" = "mainapp_element"."id") WHERE '
        query_sql = ''
        for k, v in post.items():
            if k == 'calorie':
                query_sql += ' AND "mainapp_menu"."calorie" <= ' + str(
                    float(v) / week_denominator) + ' AND "mainapp_menu"."calorie" > 0'
            else:
                query_sql += ' AND "mainapp_element"."' + k + '" <= ' + str(
                    float(v) / week_denominator) + ' AND "mainapp_element"."' + k + '" > 0'
        query_sql = sql + '( ' + query_sql[5:] + ' )'
        menus = Menu.objects.raw(query_sql)
        print('log sql', query_sql)
        print('log count', len(list(menus)))

        serializer = MenuSerializerLighter(menus, many=True)  # 轻量级的Menu
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'patch'])
    def get_menus_by_materials(self, request):
        """
        通过多个material组合找出这些material可以做的菜
        :param request:
        :return:
        """
        material_names = request.POST.getlist('material')
        print('param names', material_names)

        food_materials = []
        # 每个名字相近的食材 组合为一个query_set存到list中
        for m_name in material_names:  # 遍历用户POST的食材名字
            # 把名字相近的食材都从数据库读出来,比如蒜,大蒜
            m_qs = FoodMaterial.objects.filter(material_name__contains=m_name)
            food_materials.append(m_qs)

        print('food materials', food_materials)

        # 把第一个material_0(query set)从list中取出来
        material_0, food_materials = food_materials[0], food_materials[1:]
        # 首先查询material_0对应的菜
        query_set = Menu.objects.filter(cookquantity__material__in=material_0)
        # 然后再在material_0查询结果的基础上求其他material对应的菜的交集
        for materials in food_materials:
            query_set = query_set.intersection(Menu.objects.filter(cookquantity__material__in=materials))
        print('query set', query_set)

        # 如果组合菜太少
        if query_set.count() < 10:
            query_set = Menu.objects.filter(cookquantity__material__in=material_0)

        if query_set.count() == 0:
            return HttpResponse(status=404)
        else:
            serializer = MenuSerializer(query_set, many=True)
            return Response(serializer.data)


# class CookQuantityDetail(APIView):
#     def get(self, request, name):
#         menu = Menu.objects.get(name=name)
#         cook_quantities = CookQuantity.objects.filter(menu=menu)
#         serializer = CookQuantitySerializer(cook_quantities, many=True)
#         return Response(serializer.data)

# class CookQuantityDetail(generics.ListAPIView):
#     serializer_class = CookQuantitySerializer
#     lookup_field = 'name'  # 在url中寻找的参数,可以通过self.kwargs['name']获取
#
#     def get_queryset(self):
#         name = self.kwargs['name']
#         menu = Menu.objects.get(name=name)
#         return CookQuantity.objects.filter(menu=menu)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class CookQuantityViewSet(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        查询菜谱具体需要的食材和数量(暂时不需要了,直接集成到了MenuViewSet里面,让MenuSerializer本身就包含食材信息)
        :param pk:
        """
        print('log', pk)
        menu = Menu.objects.get(name=pk)
        cook_quantities = CookQuantity.objects.filter(menu=menu)
        serializer = CookQuantitySerializer(cook_quantities, many=True)
        return Response(serializer.data)


class FoodMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodMaterial.objects.all()
    serializer_class = FoodMaterialSerializer

    def retrieve(self, request, *args, **kwargs):
        material_name = kwargs['pk']
        food_materials = FoodMaterial.objects.filter(material_name__icontains=material_name)
        material = food_materials[0] if food_materials.count() > 0 else FoodMaterial()
        serializer = FoodMaterialSerializer(material)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     """
    #     查询食材可以做的菜
    #     :param pk: 食材名
    #     """
    #     food_material = FoodMaterial.objects.get(material_name=pk)
    #     cook_quantities = CookQuantity.objects.filter(material=food_material)
    #     serializer = CookQuantitySerializer(cook_quantities, many=True)
    #     return Response(serializer.data)


class MyUserViewSet(viewsets.ModelViewSet):
    """
    update PUT http://127.0.0.1:8000/myuser/test/  body传入更新后的数据
    retrieve GET http://127.0.0.1:8000/myuser/test1/
    create POST http://127.0.0.1:8000/myuser/  body传入创建的数据
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def add_eaten_history(self, request):
        """
        每次点一个菜,就把这个菜加入到History表中和当前的user关联
        :param request:
        :return:
        """
        username = request.POST['username']
        menu_name = request.POST['menu']
        user = MyUser.objects.filter(username=username)[0]
        menu = Menu.objects.filter(name=menu_name)[0]

        # 先删除以前的记录以免占用资源
        History.objects.filter(user=user, menu=menu).delete()
        new_history = History.objects.create(user=user, menu=menu)
        return Response(HistorySerializer(new_history).data)

    @action(detail=False, methods=['get'])
    def get_eaten_history(self, request):
        """
        每次点一个菜,就把这个菜加入到History表中和当前的user关联
        :param request:
        """
        username = request.GET['username']
        user = MyUser.objects.filter(username=username)[0]
        history = History.objects.filter(user=user).order_by('-time')
        return Response(HistorySerializer(history, many=True).data)

    @action(detail=False, methods=['post'])
    def eaten_menu(self, request):
        """
        吃了一个菜,就传过来这个菜名,然后动态改变用户已吃的营养元素的量
        :param request: 带有一个menu_name参数,一个username参数

        吃了一个菜,就传入摄入的elements,然后+= 存到user的elements里面
        :param request: 带有一个elements参数,一个username参数
        """
        username = request.POST['username']
        user = MyUser.objects.get(username=username)  # user对象
        # 根据user对象找到user对应的elements
        user_element = user.eaten_elements if user.eaten_elements != None else Element()

        # 根据POST传入的元素kv,创建一个Element对象
        eaten_elements = Element()
        for k, v in request.POST.items():
            if k != 'username':
                setattr(eaten_elements, k, float(v))
                print('log eaten_elements', getattr(eaten_elements, k))
        # print('log',user_element)
        # print('log',eaten_elements)

        user_element += eaten_elements
        user_element.save()
        user.eaten_elements = user_element
        user.save()

        return Response(MyUserSerializer(user).data)

        # menu_name = request.POST['menu_name']
        # menu_list = Menu.objects.filter(name=menu_name)
        # if (menu_list.count() > 0):
        #     # 首先获取到menu存在的elements信息
        #     menu = menu_list[0]
        #     menu_elements = menu.elements
        #     # 然后获取user的elements
        #     username = request.POST['username']
        #     user = MyUser.objects.get(username=username)
        #     user_element = user.eaten_elements if user.eaten_elements != None else Element()
        #
        #     # 加值,保存
        #     user_element += menu_elements
        #     # 把由material计算得到的卡路里换成直接爬到的卡路里
        #     user_element.calorie = user_element.calorie - menu_elements.calorie + menu.calorie
        #
        #     print('log', 'after add ', user_element.calorie)
        #
        #     user_element.save()
        #     user.eaten_elements = user_element
        #     user.save()
        #     return Response(MyUserSerializer(user).data)
        # else:
        #     return Http404('not found this menu : ' + menu_name)
        # return HttpResponse('test')


class MenuClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuClassification.objects.all()
    serializer_class = MenuClassificationSerializer
    lookup_field = 'classification'


class OccupationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    lookup_field = 'occupation_name'


class PhysiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Physique.objects.all()
    serializer_class = PhysiqueSerializer
    lookup_field = 'physical_name'


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        # form = UploadFileForm(data=request.POST, files=request.FILES)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponse('save file ')
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return HttpResponse(uploaded_file_url)

    return HttpResponse('test')


class IllnessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Illness.objects.all()
    serializer_class = IllnessSerializer
    lookup_field = 'menu_classification'


class TrickViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trick.objects.all()
    serializer_class = TrickSerializer

    @action(detail=False, methods=['get'])
    def get_random_tricks(self, request):
        import random
        import numpy as np
        size = self.queryset.count()
        count = request.GET['count']
        count = int(count)
        # sample : 从一个list中随机挑选n个数组成list
        random_index = random.sample(range(size), count)
        random_tricks = np.array(self.queryset)[random_index]
        serializer = TrickSerializer(random_tricks, many=True)
        return Response(serializer.data)

# [calorie,carbohydrate,fat ,protein,cellulose,vitaminA,vitaminB1,vitaminB2,vitaminB6,vitaminC,vitaminE,carotene,cholesterol,Mg,Ca,Fe,Zn,Cu,Mn,K ,P ,Na,Se,niacin ,thiamine]
