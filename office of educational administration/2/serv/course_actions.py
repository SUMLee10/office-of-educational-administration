from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html
from aiohttp_session import get_session

@web_routes.post("/action/course/createclassic")
async def createcourse(request):
    paramer = await request.post()
    years = paramer.get("years")
    date = "'" + paramer.get("date") + "'"
    clid="'"+paramer.get("clid")+"'"
    cid="'"+paramer.get("cid")+"'"
    #存在此记录则跳转错误页面
    if(getclassicforclass(cid,clid,years,date)==1):
        return web.HTTPFound(location="/error")
    #插入数据
    with db_block() as db:
        db.execute("""INSERT INTO course_stu VALUES("""+cid+""","""+clid+""","""+years+""","""+date+""")""")
    return web.HTTPFound(location="/course_create")
@web_routes.post("/course")
async def getclassiclist(request):
    studate = get_studate()
    paramer = await request.post()
    years = paramer.get("years")
    date = "'" + paramer.get("date") + "'"
    id = "'" + paramer.get("id") + "'"
    session = await get_session(request)
    sql="""SELECT s.no,c.name,c.sn FROM student as s inner join course_stu as cs on s.class_id=cs.class_id inner join course c on cs.cid=c.no
         where s.no="""+id+""" and cs.stu_year="""+years+""" and cs.stu_date="""+date
    if(session['icode']==2):
        class_id = "'" + paramer.get("cid") + "'"
        sql="""SELECT c.name FROM course_stu as cs inner join course c on cs.cid=c.no where cs.class_id="""+class_id+""" and cs.stu_year="""+years+""" and cs.stu_date="""+date+""" group by c.name;"""
    with db_block() as db:
        db.execute(sql)
        res=list(db)
    if (session['icode'] == 2):
        return render_html(request, 'course_list_teacher.html', items=res, studate=studate)
    return render_html(request, 'course_list.html',items=res,studate=studate)
def get_studate():
        res = ["上学期", "下学期"]
        return res
def getclassicforclass(cid,clid,year,date):
    with db_block() as db:
        db.execute("""SELECT COUNT(*) FROM course_stu where class_id="""+cid+""" and cid="""+clid+""" and stu_year="""+year+""" and stu_date="""+date)
        res=list(db)
    return res[0].count