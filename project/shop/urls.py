from django.urls import path
from .views import RubricList, RubricDetailView, GoodsView, Goods_add, UpdateGoodView, OrderView, DeleteGoodView, \
    AgreementFunc, DeleteCommentView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', RubricList.as_view(), name='main'),
    # path('comment_goods/<int:pk>', GoodsForMainPage.as_view(), name='main2'),
    path('<int:pk>/', RubricDetailView.as_view(), name='detail_goods'),
    path('comment_goods/<int:pk>/', GoodsView.as_view(), name='comment_goods'),
    path('add_goods/', Goods_add.as_view(), name='add_goods'),
    path('edit_goods/<int:pk>/', UpdateGoodView.as_view(), name='edit_goods'),
    path('delete_goods/<int:pk>/', DeleteGoodView.as_view(), name='delete_goods'),
    path('delete_comments/<int:pk>/', DeleteCommentView.as_view(), name='delete_comments'),
    path('add_order/<int:pk>/', OrderView.as_view(), name='add_order'),
    path('agreement/', AgreementFunc, name='agreement')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
