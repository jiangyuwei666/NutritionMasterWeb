from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from mainapp import views

app_name = 'mainapp'

router = DefaultRouter()
router.register('menus',views.MenuViewSet)
router.register('cookquantity',views.CookQuantityViewSet,base_name='cookquantity')
router.register('foodmaterial',views.FoodMaterialViewSet,base_name='foodmaterial')
router.register('myuser',views.MyUserViewSet)
router.register('menuclassification',views.MenuClassificationViewSet)
router.register('occupation',views.OccupationViewSet)
router.register('physique',views.PhysiqueViewSet)
router.register('illness',views.IllnessViewSet)
router.register('trick',views.TrickViewSet)

urlpatterns = [
    # path('menus/', views.MenuList.as_view(), name='menu-list'),
    # path('menus/<str:name>/', views.MenuDetail.as_view(), name='menu-detail'),
    # path('cookquantity/<str:name>/', views.CookQuantityDetail.as_view(), name='cook-quantity'),
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('filetest/',views.upload_file,name='filetest'),
]


