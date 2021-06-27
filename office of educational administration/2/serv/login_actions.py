from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from aiohttp_session import get_session

from .config import db_block, web_routes

@web_routes.post('/actions/login')
async def action_login(request):
    paramer=await request.post()
    id="'"+paramer.get("id")+"'"
    psw="'"+paramer.get("password")+"'"
    sql="""SELECT COUNT(*) FROM student where no="""+id+""" and password="""+psw
    result=exesql(sql)
    icode=0
    session = await get_session(request)
    if(result[0].count==1):
        #学生
        icode = 1
        session['icode'] = icode
        return web.HTTPFound(location="/course")
    else:
        sql = """SELECT COUNT(*) FROM teacher where tid=""" + id + """ and password=""" + psw
        result = exesql(sql)
    if (result[0].count==1):
        #教师
        icode = 2
        session['icode'] = icode
        return web.HTTPFound(location="/course_teacher")
    else:
        sql = """SELECT COUNT(*) FROM root where tid=""" + id + """ and password=""" + psw
        result = exesql(sql)
    if (result[0].count == 1):
        #管理员
        icode = 3
        session['icode'] = icode
        return web.HTTPFound(location="/grade")
def exesql(sql):
    with db_block() as db:
        db.execute(sql)
        result=list(db)
    return result