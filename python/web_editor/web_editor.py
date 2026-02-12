import os
import pandas as pd
from flask import Flask, jsonify, request, send_file, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../db"))
SUPPORTED_LANG_FILE = os.path.join(BASE_DIR, "supported_languages.csv")

# ---------- Helpers ----------

def load_supported_languages():
    df = pd.read_csv(SUPPORTED_LANG_FILE)
    df = df[df["dict"] == True]
    return df[["key", "language_str"]].to_dict(orient="records")


def dict_path(lang):
    return os.path.join(BASE_DIR, f"dictionary_{lang}.csv")


def load_dict(lang):
    path = dict_path(lang)
    if not os.path.exists(path):
        return pd.DataFrame(columns=["key", "text", "english", "tag", "checked"])
    df = pd.read_csv(path)
    if "checked" not in df.columns:
        df["checked"] = False
    return df


def save_dict(lang, df):
    df.to_csv(dict_path(lang), index=False)


# ---------- API ----------

@app.route("/api/languages")
def api_languages():
    return jsonify(load_supported_languages())


@app.route("/api/data")
def api_data():
    lang = request.args.get("lang", "de")
    tag = request.args.get("tag", "text").lower()

    df = load_dict(lang)
    tag = tag.lower()
    if tag == "a6":
        df = df[df["tag"].str.lower().isin(["a6-a","a6-b"])]
    elif tag == "b9":
        df = df[df["tag"].str.lower() == "b9"]
    elif tag == "wiki":
        df = df[df["tag"].str.lower() == "wiki"]
    elif tag == "others":
        df = df[df["tag"].str.lower().isin(["deprecated","scripture","span_bc","span_bce","span_ce"])]
    else:
        df = df[df["tag"].str.lower() == tag]

    return jsonify(df[["key", "text", "english", "checked"]].to_dict(orient="records"))


@app.route("/api/stats")
def api_stats():
    lang=request.args.get("lang","de")
    df=load_dict(lang)
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


@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    data = request.json
    lang = data["lang"]
    key = data["key"]
    value = data["checked"]

    df = load_dict(lang)
    df.loc[df["key"] == key, "checked"] = value
    save_dict(lang, df)

    return jsonify({"status": "ok"})


@app.route("/api/export")
def api_export():
    lang = request.args.get("lang", "de")
    return send_file(dict_path(lang), as_attachment=True)


# ---------- UI ----------

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Dictionary Editor</title>
<style>
body { font-family: Arial; margin: 20px; }
button { margin: 3px; padding: 6px 12px; }
table { border-collapse: collapse; width: 100%; margin-top: 10px; }
th, td { border: 1px solid #ccc; padding: 6px; }
th { background: #eee; }
.tagbtn.active { background: #4CAF50; color: white; }
</style>
</head>
<body>
<h2>Dictionary Web Editor</h2>

<select id="lang"></select>

<span id="tags"></span>

<br><br>
<button onclick="reload()">Check changes</button>
<button onclick="exportFile()">Export dictionary</button>

<table>
<thead>
<tr><th>Key</th><th>Text</th><th>English</th><th>Checked</th></tr>
</thead>
<tbody id="table"></tbody>
</table>

<script>
let currentTag = "text";

const tagList = [
    {label:"Text", value:"text"},
    {label:"Bible", value:"bible"},
    {label:"B9", value:"b9"},
    {label:"A6", value:"a6"},
    {label:"wiki", value:"wiki"},
    {label:"Other", value:"others"}
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
        b.className="tagbtn"+(t.value==currentTag?" active":"");
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
        if(l.key=="de") o.selected=true;
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
        tr.innerHTML=`
        <td>${r.key}</td>
        <td>${r.text||""}</td>
        <td>${r.english||""}</td>
        <td><input type="checkbox" ${r.checked?"checked":""}></td>`;

        tr.querySelector("input").onchange=async (e)=>{
            await fetch("/api/toggle",{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({
                    lang:lang,
                    key:r.key,
                    checked:e.target.checked
                })
            });
        };

        tb.appendChild(tr);
    });
}

function exportFile(){
    let lang=document.getElementById("lang").value;
    window.location=`/api/export?lang=${lang}`;
}

document.getElementById("lang").onchange=()=>{makeTagButtons();reload();};

loadLanguages().then(()=>{
    makeTagButtons();
    reload();
});
</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


# ---------- Run ----------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
