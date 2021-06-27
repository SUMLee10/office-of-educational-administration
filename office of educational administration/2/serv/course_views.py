from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html


@web_routes.get("/course")
async def view_course_list(request):
    studate = get_studate()
    return render_html(request, 'course_list.html',studate=studate)
@web_routes.get("/course_teacher")
async def view_course_list(request):
    studate = get_studate()
    classlist = get_class()
    return render_html(request, 'course_list_teacher.html',studate=studate,classlist=classlist)
@web_routes.get("/course_create")
async def view_course_list(request):
    studate = get_studate()
    classiclist=get_classic()
    classlist=get_class()
    return render_html(request, 'course_create.html',studate=studate,classiclist=classiclist,classlist=classlist)
def get_studate():
    res = ["上学期","下学期"]
    return res
def get_classic():
    with db_block() as db:
        db.execute("""SELECT DISTINCT no,name FROM course""")
        res = list(db)
    return res
def get_class():
    with db_block() as db:
        db.execute("""SELECT DISTINCT class_id FROM student""")
        res = list(db)
    return res