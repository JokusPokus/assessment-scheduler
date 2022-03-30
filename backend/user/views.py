from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    if user.organization:
        organization = {
            'id': user.organization.id,
            'name': user.organization.name
        }
    else:
        organization = None

    return Response({
        'email': user.email,
        'organization': organization
    })
