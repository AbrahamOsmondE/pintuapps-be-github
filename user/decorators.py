
def buyer_api(view_func):
    def wrapper_func(self,request,*args,**kwargs):
        if(request.user.user_type=="buyer"):
            return view_func(self,request,*args,**kwargs)
        raise ValueError("Not a buyer!")
    return wrapper_func

def seller_api(view_func):
    def wrapper_func(self,request,*args,**kwargs):
        if(request.user.user_type=="seller"):
            return view_func(self,request,*args,**kwargs)
        raise ValueError("Not a seller!")
    return wrapper_func

def all_api(view_func):
    def wrapper_func(self,request,*args,**kwargs):
        if(request.user.user_type=="seller" or request.user.user_type=="buyer" or request.user.user_type=="not_registered"):
            return view_func(self,request,*args,**kwargs)
        raise ValueError("Not a user!")
    return wrapper_func

def admin_api(view_func):
    def wrapper_func(self,request,*args,**kwargs):
        if(request.user.user_type=="admin"):
            return view_func(self,request,*args,**kwargs)
        raise ValueError("Not an admin!")
    return wrapper_func