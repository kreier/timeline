import os
import pandas as pd
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../db"))
SUPPORTED_LANG_FILE = os.path.join(BASE_DIR, "supported_languages.csv")

# in‑memory cache
DATA_CACHE = {}
ORIGINAL_CACHE = {}

# ---------- Helpers ----------

def load_supported_languages():
    df = pd.read_csv(SUPPORTED_LANG_FILE)
    df = df[df["dict"] == True]
    return df[["key", "language_str"]].to_dict(orient="records")


def dict_path(lang):
    return os.path.join(BASE_DIR, f"dictionary_{lang}.csv")


def load_dict(lang):
    path = dict_path(lang)
    if lang not in DATA_CACHE:
        if not os.path.exists(path):
            df = pd.DataFrame(columns=["key","text","english","tag","checked"])
        else:
            df = pd.read_csv(path)
        if "checked" not in df.columns:
            df["checked"] = False
        DATA_CACHE[lang] = df.copy()
        ORIGINAL_CACHE[lang] = df.copy()
    return DATA_CACHE[lang]


def save_dict(lang):
    DATA_CACHE[lang].to_csv(dict_path(lang), index=False)
    ORIGINAL_CACHE[lang] = DATA_CACHE[lang].copy()


def filter_df(df, tag):
    tag = tag.lower()
    if tag == "a6":
        return df[df["tag"].str.lower().isin(["a6-a","a6-b"])]
    if tag == "b9":
        return df[df["tag"].str.lower()=="b9"]
    if tag == "wiki":
        return df[df["tag"].str.lower()=="wiki"]
    if tag == "others":
        return df[df["tag"].str.lower().isin(["deprecated","scripture","span_bc","span_bce","span_ce"])]
    return df[df["tag"].str.lower()==tag]


# ---------- API ----------

@app.route("/api/languages")
def api_languages():
    return jsonify(load_supported_languages())


@app.route("/api/data")
def api_data():
    lang = request.args.get("lang","de")
    tag = request.args.get("tag","text")
    df = load_dict(lang)
    df = filter_df(df, tag)
    return jsonify(df[["key","text","english","checked"]].to_dict(orient="records"))


@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    d=request.json
    df=load_dict(d["lang"])
    df.loc[df["key"]==d["key"],"checked"]=bool(d["checked"])
    return jsonify({"ok":True})


@app.route("/api/edit_text", methods=["POST"])
def api_edit_text():
    d=request.json
    df=load_dict(d["lang"])
    df.loc[df["key"]==d["key"],"text"]=d["text"]
    return jsonify({"ok":True})


@app.route("/api/stats")
def api_stats():
    lang=request.args.get("lang","de")
    df=load_dict(lang).copy()
    df["tag"]=df["tag"].str.lower()
    groups={
        "text":["text"],
        "bible":["bible"],
        "b9":["b9"],
        "a6":["a6-a","a6-b"],
        "wiki":["wiki"],
        "others":["deprecated","scripture","span_bc","span_bce","span_ce"]
    }
    out={}
    for k,tags in groups.items():
        sub=df[df["tag"].isin(tags)]
        if len(sub)==0:
            out[k]=0
        else:
            out[k]=round(100*sub["checked"].fillna(False).astype(bool).sum()/len(sub),1)
    return jsonify(out)


@app.route("/api/changes")
def api_changes():
    lang=request.args.get("lang","de")
    cur=DATA_CACHE.get(lang)
    orig=ORIGINAL_CACHE.get(lang)
    if cur is None or orig is None:
        return jsonify([])

    merged=cur.merge(orig,on="key",suffixes=("_new","_old"))
    changed=merged[(merged["checked_new"]!=merged["checked_old"])|
                   (merged["text_new"]!=merged["text_old"])]

    return jsonify(changed[[
        "key",
        "checked_old","checked_new",
        "text_old","text_new"
    ]].to_dict(orient="records"))


@app.route("/api/export", methods=["POST"])
def api_export():
    lang=request.json["lang"]
    save_dict(lang)
    return jsonify({"saved":True})


# ---------- UI ----------

HTML="""
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>Editor</title>
<style>
body{font-family:Arial;margin:20px}
button{margin:3px;padding:6px 12px}
table{border-collapse:collapse;width:100%;margin-top:10px}
th,td{border:1px solid #ccc;padding:6px}
th{background:#eee}
.tagbtn.active{background:#4CAF50;color:white}
</style>
</head>
<body>
<h2>Dictionary Web Editor</h2>

<select id='lang'></select>
<span id='tags'></span>
<br><br>
<button onclick='showChanges()'>Check changes</button>
<button onclick='exportFile()'>Export dictionary</button>
<pre id='changes'></pre>

<table>
<thead>
<tr><th>Key</th><th>Text</th><th>English</th><th>Checked</th></tr>
</thead>
<tbody id='table'></tbody>
</table>

<script>
let currentTag="text";

const tagList=[
 {label:"Text",value:"text"},
 {label:"Bible",value:"bible"},
 {label:"B9",value:"b9"},
 {label:"A6",value:"a6"},
 {label:"wiki",value:"wiki"},
 {label:"Other",value:"others"}
];

async function makeTagButtons(){
 let lang=document.getElementById("lang").value||"de";
 let stats=await fetch(`/api/stats?lang=${lang}`).then(r=>r.json());
 let c=document.getElementById("tags");
 c.innerHTML="";
 tagList.forEach(t=>{
  let wrap=document.createElement("div");
  wrap.style.display="inline-block";
  wrap.style.textAlign="center";
  wrap.style.marginRight="6px";

  let b=document.createElement("button");
  b.innerText=t.label;
  b.className="tagbtn"+(t.value===currentTag?" active":"");
  b.onclick=()=>{currentTag=t.value;makeTagButtons();reload();};

  let p=document.createElement("div");
  p.style.fontSize="12px";
  p.innerText=(stats[t.value]??0)+"%";

  wrap.appendChild(b);
  wrap.appendChild(p);
  c.appendChild(wrap);
 });
}

async function loadLanguages(){
 let res=await fetch("/api/languages");
 let langs=await res.json();
 let sel=document.getElementById("lang");
 langs.forEach(l=>{
  let o=document.createElement("option");
  o.value=l.key;
  o.text=l.language_str;
  if(l.key==="de") o.selected=true;
  sel.appendChild(o);
 });
}

async function reload(){
 let lang=document.getElementById("lang").value;
 let res=await fetch(`/api/data?lang=${lang}&tag=${currentTag}`);
 let rows=await res.json();

 let tb=document.getElementById("table");
 tb.innerHTML="";

 rows.forEach(r=>{
  let tr=document.createElement("tr");

  let textCell=`<td contenteditable='true' data-key='${r.key}'>${r.text||""}</td>`;

  tr.innerHTML=`
   <td>${r.key}</td>
   ${textCell}
   <td>${r.english||""}</td>
   <td><input type='checkbox' ${r.checked?"checked":""}></td>`;

  tr.querySelector("input").onchange=async e=>{
   await fetch("/api/toggle",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({lang,key:r.key,checked:e.target.checked})
   });
   makeTagButtons();
  };

  tr.querySelector("[contenteditable]").onblur=async e=>{
   await fetch("/api/edit_text",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({lang,key:r.key,text:e.target.innerText})
   });
  };

  tb.appendChild(tr);
 });
}

async function showChanges(){
 let lang=document.getElementById("lang").value;
 let data=await fetch(`/api/changes?lang=${lang}`).then(r=>r.json());
 document.getElementById("changes").textContent=JSON.stringify(data,null,2);
}

async function exportFile(){
 let lang=document.getElementById("lang").value;
 await fetch("/api/export",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({lang})
 });
 alert("Dictionary saved to CSV.");
 makeTagButtons();
}

document.getElementById("lang").onchange=()=>{makeTagButtons();reload();};

loadLanguages().then(()=>{makeTagButtons();reload();});
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


# ---------- Run ----------

if __name__=="__main__":
    app.run(debug=True,port=5000)
