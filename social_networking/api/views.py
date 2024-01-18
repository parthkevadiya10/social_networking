
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit

from django.db.models import Q
from rest_framework import generics

from .serializers import UserSerializer, SignUpSerializer, LoginSerializer,FriendRequestSerializer
from .models import CustomUser,FriendRequest


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("a")

            user = authenticate(request, email=serializer.validated_data['email'].lower(), password=serializer.validated_data['password'])
            if user:
                login(request, user)
                print("@@@",user)
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response({'token': token})
            else:
                print("b")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestrictedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)



class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            query = self.request.query_params.get('query', '')
            queryset = CustomUser.objects.filter(email__icontains=query) | CustomUser.objects.filter(name__icontains=query)
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    print("@")
    @ratelimit(key='user', rate='3/m', block=True)
    def perform_create(self, serializer):
        print("a")
        sender = self.request.user
        print(sender)
        receiver = serializer.validated_data['receiver']
        print(receiver)
        if not FriendRequest.objects.filter(sender=sender, receiver=receiver, status='P').exists():
            serializer.save(sender=sender)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(sender=user, status='A').values_list('receiver', flat=True)
        return CustomUser.objects.filter(id__in=friends)

class PendingFriendRequestView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pending_requests = FriendRequest.objects.filter(receiver=user, status='P').values_list('sender', flat=True)
        return CustomUser.objects.filter(id__in=pending_requests)

class FriendRequestAcceptView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'A'
        instance.save()
        return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)

class FriendRequestRejectView(generics.DestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'R'
        instance.save()
        return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)
