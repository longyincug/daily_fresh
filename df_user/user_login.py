from django.http import HttpResponseRedirect

# 验证用户是否登录，装饰器
def user_decorator_login(fun):
    def user_login(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return fun(request,*args,**kwargs)
        else:
            # 如果未登录则转到登录页面
            red = HttpResponseRedirect('/user/login/')
            # 同时要记录下来这个页面，以便登陆后再切换回来
            path = request.get_full_path() # get_full_path()方法，表示完整路径，包括额外的get参数
            red.set_cookie('pre_path',path)
            return red
    return user_login