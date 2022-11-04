from django.urls import path
from products.api.views.product_views import (
    ProductsListAPIView,
    CurrentUserProductsListAPIView,
    UserProductsListAPIView,
    ProductRetrieveAPIView,
    ProductCreateAPIView,
    ProductDeleteAPIView,
    ProductCategoriesListAPIView,
    get_recommendations
)
from products.api.views.product_review_views import (
    ProductReviewCreateAPIView,
    ProductReviewUpdateAPIView,
    ProductReviewDeleteAPIView,
    review_is_helpful
)
from products.api.views.product_image_views import (
    ProductImageCreateAPIView,
    ProductImageDeleteAPIView
)
from products.api.views.product_video_views import (
    ProductVideoCreateAPIView,
    ProductVideoDeleteAPIView
)
from products.api.views.product_question_views import (
    ProductQuestionCreateAPIView,
    ProductQuestionUpdateAPIView,
    ProductQuestionDeleteAPIView,
    like_question,
    dislike_question
)
from products.api.views.wishlist_views import (
    WishlistRetrieveAPIView,
    add_remove_wishlist
)
from products.api.views.product_coupon_views import (
    CurrentUserCouponsListAPIView,
    CouponCreateAPIView,
    CouponUpdateAPIView,
    CouponDeleteAPIView,
    redeem_coupon
)
from products.api.views.browsing_history import (
    get_history
)

app_name = 'products'

urlpatterns = [
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('products/my/', CurrentUserProductsListAPIView.as_view(), name='my_products'),
    path('products/user/<str:username>/', UserProductsListAPIView.as_view(), name='user_products'),
    path('products/<int:id>/', ProductRetrieveAPIView.as_view(), name='product_details'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('products/delete/<int:id>/', ProductDeleteAPIView.as_view(), name='product_delete'),
    path('products/categories/', ProductCategoriesListAPIView.as_view(), name='product_categories'),
    path('products/recommend/', get_recommendations, name='recommend_products'),

    path('products/image-upload/', ProductImageCreateAPIView.as_view(), name='product_image_create'),
    path('products/image-delete/<int:id>/', ProductImageDeleteAPIView.as_view(), name='product_image_delete'),

    path('products/video-upload/', ProductVideoCreateAPIView.as_view(), name='product_video_create'),
    path('products/video-delete/<int:id>/', ProductVideoDeleteAPIView.as_view(), name='product_video_delete'),

    path('products/question/create/', ProductQuestionCreateAPIView.as_view(), name='product_question_create'),
    path('products/question/update/<int:id>/', ProductQuestionUpdateAPIView.as_view(), name='product_question_update'),
    path('products/question/delete/<int:id>/', ProductQuestionDeleteAPIView.as_view(), name='product_question_delete'),
    path('products/question/like/', like_question, name='product_question_like'),
    path('products/question/dislike/', dislike_question, name='product_question_dislike'),

    path('product-review/create/', ProductReviewCreateAPIView.as_view(), name='product_review_create'),
    path('product-review/update/<int:id>/', ProductReviewUpdateAPIView.as_view(), name='product_review_update'),
    path('product-review/delete/<int:id>/', ProductReviewDeleteAPIView.as_view(), name='product_review_delete'),
    path('product-review/make-helpful/', review_is_helpful, name='product_review_make_helpful'),

    path('wishlist/', WishlistRetrieveAPIView.as_view(), name='wishlist'),
    path('wishlist/add/', add_remove_wishlist, name='wishlist_add'),

    path('user/coupons/', CurrentUserCouponsListAPIView.as_view(), name='user_coupons'),
    path('coupon/create/', CouponCreateAPIView.as_view(), name='coupon_create'),
    path('coupon/update/<int:id>/', CouponUpdateAPIView.as_view(), name='coupon_update'),
    path('coupon/delete/<int:id>/', CouponDeleteAPIView.as_view(), name='coupon_delete'),
    path('coupon/redeem/', redeem_coupon, name='coupon_redeem'),

    path('products/history/', get_history, name='get_history'),
]
