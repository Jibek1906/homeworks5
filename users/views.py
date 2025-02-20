from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, AuthSerializer, ConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import UserProfile

@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)
    user_profile = UserProfile.objects.create(user=user)
    user_profile.generate_confirmation_code()

    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})

@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid username or password'})

@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')

    try:
        user = User.objects.get(username=username)
        if user.profile.confirmation_code == confirmation_code:
            user.is_active = True
            user.save()
            return Response({'message': 'User confirmed successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)