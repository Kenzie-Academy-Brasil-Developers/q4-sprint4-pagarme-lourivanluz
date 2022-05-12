from rest_framework.urls import path


from products.views import ProductView, ProductGetPatchView, ProductListSellerId

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<product_id>/", ProductGetPatchView.as_view()),
    path("products/seller/<seller_id>/", ProductListSellerId.as_view()),
]
