from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/grade")
async def view_list_grades(request):
    res= await get_grade_initinfo(request,None,None,None)
    return res
@web_routes.post("/grade")
async def view_list_grades(request):
    parmers=await request.post()
    years=""
    date=""
    cid=""
    if(parmers.get("years")!=None and parmers.get("date")!=None and parmers.get("cid")!=None):
        years = "'" + parmers.get("years") + "'"
        date = "'" + parmers.get("date") + "'"
        cid="'" + parmers.get("cid") + "'"
    res= await get_grade_initinfo(request,years,date,cid)
    return res

async def get_grade_initinfo(request,years,date,cid):
    sql1="""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """
    sql2="""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """
    sql3="""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """
    if(years!=None and date!= None and cid !=None):
        sql3="""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade,
            g.stu_date,
            g.stu_year
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        where g.stu_year=
        """+years+""" and g.stu_date="""+date+""" and s.class_id="""+cid+"""
        ORDER BY stu_sn, cou_sn"""
    with db_block() as db:
        db.execute(sql1)
        students = list(db)

        db.execute(sql2)
        courses = list(db)

        db.execute(sql3)

        items = list(db)
        classlist=get_class()
        studate=get_studate()
    return render_html(request, 'grade_list.html',
                       students=students,
                       courses=courses,
                       items=items,
                       classlist=classlist,
                       studate=studate)
def get_class():
    with db_block() as db:
        db.execute("""SELECT DISTINCT class_id FROM student""")
        res = list(db)
    return res
def get_studate():
    res = ["上学期","下学期"]
    return res
@web_routes.get('/grade/edit/{stu_sn}/{cou_sn}')
def view_grade_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT grade FROM course_grade
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, "grade_edit.html",
                       stu_sn=stu_sn,
                       cou_sn=cou_sn,
                       grade=record.grade)


@web_routes.get("/grade/delete/{stu_sn}/{cou_sn}")
def grade_deletion_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, 'grade_dialog_deletion.html', record=record)
