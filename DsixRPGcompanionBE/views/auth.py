from DsixRPGcompanionBE.models.user import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated User

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the User object or None if no User is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'uid': user.uid,
            'handle': user.handle,
            'bio': user.bio,
            'admin': user.admin,
            'game_master': user.game_master
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the User in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new User for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the levelupapi_user table
    user = User.objects.create(
        bio=request.data['bio'],
        uid=request.data['uid'],
        handle=request.data['handle'],
        game_master=request.data['gameMaster'],
        admin=request.data['admin']
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'bio': user.bio
    }
    return Response(data)
