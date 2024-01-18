from django.urls import path
from .views import SignUpView, LoginView, RestrictedView,UserSearchView,FriendListView,PendingFriendRequestView,FriendRequestCreateView,FriendRequestAcceptView,FriendRequestRejectView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('restricted/', RestrictedView.as_view(), name='restricted'),
    path('user/search/', UserSearchView.as_view(), name='user-search'),
    path('friend/list/', FriendListView.as_view(), name='friend-list'),
    path('friend/requests/', PendingFriendRequestView.as_view(), name='friend-requests'),
    path('friend/request/', FriendRequestCreateView.as_view(), name='friend-request'),
    path('friend/accept/<int:pk>/', FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('friend/reject/<int:pk>/', FriendRequestRejectView.as_view(), name='friend-request-reject'),
]
