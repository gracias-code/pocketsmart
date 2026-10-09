import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.database import connect
from app.dependencies import current_user
from app.models.schemas import HomeRequest, PartyRequest
from app.services.recommendation_service import build

router=APIRouter()

def save(user_id,result,data):
    conn=connect()
    cur=conn.execute("INSERT INTO history(user_id,planner_type,budget,request_json,response_json) VALUES(?,?,?,?,?)",
                     (user_id,result["planner_type"],result["budget"],json.dumps(data),json.dumps(result)))
    conn.commit(); hid=cur.lastrowid; conn.close()
    return hid

@router.post("/generate-home")
def home(p:HomeRequest,user=Depends(current_user)):
    data=p.model_dump(); r=build("home",data); r["history_id"]=save(user["id"],r,data); return r

@router.post("/generate-party")
def party(p:PartyRequest,user=Depends(current_user)):
    data=p.model_dump(); r=build("party",data); r["history_id"]=save(user["id"],r,data); return r

@router.post("/generate-jewelry")
async def jewelry(
    budget:float, occasion:str, style:str="Elegant", outfit_color:str="", notes:str="",
    outfit_image:UploadFile|None=File(default=None), user=Depends(current_user)
):
    data={"budget":budget,"occasion":occasion,"style":style,"outfit_color":outfit_color,"notes":notes}
    image=None; mime=None
    if outfit_image:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}:
            raise HTTPException(400,"Use JPG, PNG or WEBP.")
        image=await outfit_image.read()
        if len(image)>5*1024*1024: raise HTTPException(400,"Image must be 5 MB or smaller.")
        mime=outfit_image.content_type
    r=build("jewelry",data,image,mime); r["history_id"]=save(user["id"],r,data); return r

@router.get("/recommendations-details/{history_id}")
def details(history_id:int,user=Depends(current_user)):
    conn=connect()
    row=conn.execute("SELECT * FROM history WHERE id=? AND user_id=?",(history_id,user["id"])).fetchone()
    conn.close()
    if not row: raise HTTPException(404,"Recommendation not found.")
    r=json.loads(row["response_json"]); r["history_id"]=row["id"]; r["created_at"]=row["created_at"]; return r

@router.get("/history")
def history(user=Depends(current_user)):
    conn=connect()
    rows=conn.execute("SELECT id,planner_type,budget,created_at FROM history WHERE user_id=? ORDER BY id DESC LIMIT 50",(user["id"],)).fetchall()
    conn.close()
    return {"items":[dict(x) for x in rows]}

@router.get("/session-info")
def session_info(user=Depends(current_user)): return {"logged_in":True,"user":user}

@router.get("/session-data")
def session_data(user=Depends(current_user)):
    conn=connect(); count=conn.execute("SELECT COUNT(*) FROM history WHERE user_id=?",(user["id"],)).fetchone()[0]; conn.close()
    return {"user":user,"recommendation_count":count}

@router.get("/health")
def health(): return {"status":"ok","service":"PocketSmart AI"}
