from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from .models import UserData, FriendRequest
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from django.db import models
from django.utils import timezone
# # view for registering users


class RegisterView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    def post(self, request):

        # if email is already in use
        if UserData.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserData.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        keyword = request.GET.get('keyword', '')
        page = request.GET.get('page', 1)

        if '@' in keyword:  # If the keyword contains '@', assume it's an email search
            users = UserData.objects.filter(email=keyword)
        else:  # Otherwise, search by name
            users = UserData.objects.filter(name__icontains=keyword)

        paginator = self.paginate_queryset(users)
        serializer = self.get_serializer(paginator, many=True)

        return self.get_paginated_response(serializer.data)

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def friends(self, request):
        friends = FriendRequest.objects.filter(
            (models.Q(from_user=request.user) | models.Q(to_user=request.user)),
            is_accepted=True,
            is_rejected=False
        ).exclude(models.Q(from_user=request.user) & models.Q(to_user=request.user))

        friend_users = [friend.from_user if friend.to_user == request.user else friend.to_user for friend in friends]
        serializer = UserSerializer(friend_users, many=True)  # Assuming you have a UserSerializer

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False, is_rejected=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def send_friend_request(self, request):
        to_user_id = request.data.get('to_user')
        to_user = UserData.objects.get(pk=to_user_id)
        from_user = request.user
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, is_accepted=False, is_rejected=False).exists():
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=to_user, to_user=from_user, is_accepted=False, is_rejected=False).exists():
            return Response({'detail': 'Friend request already received.'}, status=status.HTTP_400_BAD_REQUEST)

        if from_user == to_user:
            return Response({'detail': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        recent_requests = FriendRequest.objects.filter(
            from_user=request.user,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
        ).count()

        if recent_requests >= 3:
            return Response({'detail': 'You have reached the limit of 3 friend requests within a minute.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request = FriendRequest(from_user=request.user, to_user=to_user)
        friend_request.save()

        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def accept_friend_request(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.to_user != request.user or friend_request.is_accepted or friend_request.is_rejected:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.is_accepted = True
        friend_request.save()

        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def reject_friend_request(self, request, pk=None):
        friend_request = self.get_object()

        if friend_request.to_user != request.user or friend_request.is_accepted or friend_request.is_rejected:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.is_rejected = True
        friend_request.save()

        serializer = self.get_serializer(friend_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RejectFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_rejected=True)