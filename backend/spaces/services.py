from .models.space import Space
from .models.request import Request
from myauth.models import User

def IsUserInSpace(obj:Space ,user:User) -> bool:
    '''
    Checks if user is in the space

    :params obj: Takes in the space object to check angaist , user:Takis in the user requested
    :type obj:Space , user: User

    :rtype: bool
    :return True if user is in the space and False otherwise
    '''
    if obj in User.objects.get(pk=user.id).space_set.all() or obj.creater == user :
        return True
    return False



def doesSpaceNameExist(name:str) -> bool:
    '''
    Checks if a space exist with a  name

    :params name: The name of the space
    :type name:str

    :rtype bool
    :return True if space exists and False otherwies
    '''
    try:
        space = Space.objects.filter(name=name)
        return True
    except:
        return False
