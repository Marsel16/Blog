""" utils.py """
def get_user_from_request(request):
    """Get user from request or return None"""
    return request.user if not request.user.is_anonymous else None
