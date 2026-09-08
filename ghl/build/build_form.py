#!/usr/bin/env python3
"""Rewrite a GHL form as data via the builder's own save: POST services.leadconnectorhq.com/forms/{id}
with the full {name, formData} document and the browser Firebase token-id (channel APP, source WEB_USER).
Custom-field elements embed the custom-field record plus form keys (label, required, width, type=dataType.lower()).
  python build/build_form.py --base form_save_body.json --form-id ID --cf /tmp/cf.json --spec snapshots/event-rental/config/form_spec.json [--live]
"""
import argparse, json, os, sys, requests
ap=argparse.ArgumentParser(); ap.add_argument("--base",required=True); ap.add_argument("--form-id",required=True); ap.add_argument("--cf",required=True); ap.add_argument("--spec",required=True); ap.add_argument("--live",action="store_true"); a=ap.parse_args()
tok=os.getenv("GHL_TOKEN_ID","").strip()
if not tok: sys.exit("GHL_TOKEN_ID not set")
base=json.load(open(a.base)); cf={f["name"]:f for f in json.load(open(a.cf))["customFields"]}; spec=json.load(open(a.spec))
def std(label,tag,typ,ph,req,typelabel=None):
    return {"label":label,"tag":tag,"hiddenFieldQueryKey":tag,"type":typ,"typeLabel":typelabel or "Text","placeholder":ph,"required":req,"standard":True,"fieldWidthPercentage":100}
def custom(name,label,req,ph=""):
    r=cf[name]; key=r["fieldKey"].split(".")[-1]
    e={"Id":r["id"],"id":r["id"],"active":False,"allowCustomOption":False,"customFieldLabel":r["name"],"dataType":r["dataType"],"dateAdded":r.get("dateAdded",""),"description":"","documentType":"field","edit":False,
       "fieldKey":r["fieldKey"],"fieldWidthPercentage":100,"fieldsCount":0,"hiddenFieldQueryKey":key,"label":label,"locationId":r["locationId"],"model":r.get("model","contact"),"name":r["name"],"parentId":r.get("parentId",""),
       "placeholder":ph,"position":r.get("position",0),"required":req,"showInForms":True,"standard":False,"tag":r["id"],"type":r["dataType"].lower()}
    if r.get("picklistOptions"): e["picklistOptions"]=r["picklistOptions"]
    return e
fields=[]
for s in spec["fields"]:
    if s.get("standard"): fields.append(std(s["label"],s["tag"],s["type"],s.get("placeholder",""),s.get("required",False),s.get("typeLabel")))
    else: fields.append(custom(s["field"],s["label"],s.get("required",False),s.get("placeholder","")))
form=base["formData"]["form"]
old=form["fields"]; tc=next(f for f in old if f.get("tag")=="terms_and_conditions"); sub=next(f for f in old if f.get("type")=="submit"); foot=next(f for f in old if f.get("tag")=="header")
tc=dict(tc); tc["required"]=True; tc["placeholder"]=spec["consent_html"]; tc["preview"]=spec["consent_html"]; tc.pop("placeholder2",None)
sub=dict(sub); sub["label"]=spec["submit_label"]
foot=dict(foot); foot["label"]=spec["footer_html"]
form["fields"]=fields+[tc,sub,foot]
# --- brand chrome: header element (logo + title) on top, palette-driven styles
if spec.get("header"):
    hd=spec["header"]; logo=hd.get("logo_url","")
    html=("<p style=\"text-align: center; margin: 0 0 10px 0;\"><img src=\""+logo+"\" style=\"max-height: 72px; max-width: 240px;\"></p>" if logo.startswith("http") else "")
    html+="<h2 style=\"text-align: center; font-family: Inter; font-size: 26px; font-weight: 700; margin: 0 0 6px 0; color: #111111;\">"+hd["title"]+"</h2>"
    html+="<p style=\"text-align: center; font-family: Inter; font-size: 15px; color: #475467; margin: 0 0 8px 0;\">"+hd.get("subtitle","")+"</p>"
    head=dict(foot); head["label"]=html; head["hiddenFieldQueryKey"]="header_0"
    form["fields"]=[head]+form["fields"]
st=spec.get("style",{})
form["style"]=dict(form["style"]); form["style"].update({"background":st.get("background","FFFFFFFF"),"border":{"border":1,"color":"E4E7ECFF","radius":st.get("radius",16),"style":"solid"},"padding":{"bottom":28,"left":28,"right":28,"top":28,"extraPaddingComputingProcessed":True},"shadow":{"blur":24,"color":"1018281A","horizontal":0,"spread":0,"vertical":8}})
fs=dict(form["fieldStyle"]); fs.update({"border":{"border":1,"color":"D0D5DDFF","radius":10,"type":"solid"},"labelFontFamily":"Inter","labelFontWeight":600,"labelFontSize":14,"labelColor":st.get("labelColor","344054FF"),"placeholderFontFamily":"Inter","padding":{"bottom":12,"left":14,"right":14,"top":12}})
form["fieldStyle"]=fs
sub["bgColor"]=st.get("buttonBg",sub.get("bgColor")); sub["color"]=st.get("buttonText",sub.get("color")); sub["radius"]=999; sub["borderRadius"]=999; sub["fontSize"]=16; sub["weight"]=700; sub["padding"]={"bottom":14,"left":20,"right":20,"top":14}
form["formAction"]=dict(form["formAction"]); form["formAction"].update({"actionType":"2","thankyouText":spec["thankyou_html"],"redirectUrl":""})
base["name"]=spec["name"]
print(f"{spec['name']}: {len(form['fields'])} elements ({sum(1 for f in fields if not f.get('standard'))} custom fields)")
for f in form["fields"]: print("  ",(f.get("dataType") or f.get("type")).ljust(14),("*" if f.get("required") else " "),str(f.get("label"))[:60])
if not a.live: print("\ndry run - add --live to POST"); sys.exit(0)
H={"token-id":tok,"channel":"APP","source":"WEB_USER","Version":"2021-07-28","content-type":"application/json","accept":"application/json"}
r=requests.post(f"https://services.leadconnectorhq.com/forms/{a.form_id}",headers=H,data=json.dumps(base),timeout=60)
print("POST",r.status_code,r.text[:200] if not r.ok else "ok")
g=requests.get(f"https://services.leadconnectorhq.com/forms/{a.form_id}",headers=H,timeout=30).json()
fm=(g.get("form") or g.get("data") or g); print("stored name:",fm.get("name"),"| fields:",len(fm["formData"]["form"]["fields"]))
