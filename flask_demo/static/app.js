const tabs=document.querySelectorAll(".tab");
tabs.forEach(button=>button.addEventListener("click",()=>{
  tabs.forEach(b=>b.classList.toggle("active",b===button));
  document.querySelectorAll(".page").forEach(p=>p.classList.toggle("active",p.id===button.dataset.page));
  window.scrollTo({top:0,behavior:"smooth"});
}));
const $=id=>document.getElementById(id);
let currentArticles=[];
let sourceLabel="";
async function run(mode){
  const buttons=[$("demoBtn"),$("liveBtn")];
  buttons.forEach(b=>b.disabled=true);
  $("status").className="status";
  $("status").textContent="Отримуємо відповідь Flask...";
  $("pipeline").hidden=true;
  try{
    const response=await fetch(mode==="live"?"/api/live":"/api/demo",{cache:"no-store"});
    const data=await response.json();
    if(!response.ok)throw new Error(data.error||"HTTP "+response.status);
    sourceLabel=data.source;
    currentArticles=data.articles||[];
    $("requestDescription").textContent=data.step_requests;
    $("parseDescription").textContent=data.step_bs4;
    $("htmlLength").textContent=data.statistics.html_length;
    $("linkCount").textContent=data.statistics.links;
    $("headingCount").textContent=data.statistics.headings;
    $("htmlExcerpt").textContent=data.html_excerpt;
    $("jsonOutput").textContent=JSON.stringify({source:data.source,articles:currentArticles},null,2);
    const tbody=$("resultRows");
    tbody.replaceChildren();
    for(const [i,article] of currentArticles.entries()){
      const tr=tbody.insertRow();
      tr.insertCell().textContent=String(i+1);
      tr.insertCell().textContent=article.title;
      tr.insertCell().textContent=article.date||"Не виявлено";
      const cell=tr.insertCell();
      const a=document.createElement("a");
      a.href=article.url;a.target="_blank";a.rel="noopener noreferrer";a.textContent="Джерело";
      cell.append(a);
    }
    if(!currentArticles.length){
      const tr=tbody.insertRow(),td=tr.insertCell();
      td.colSpan=4;td.textContent="Парсер не знайшов заголовків. HTML-структура могла змінитися.";
    }
    $("tableInfo").textContent="Записів: "+currentArticles.length+". Джерело: "+sourceLabel;
    $("pipeline").hidden=false;
    $("status").textContent="Отримано і проаналізовано HTML. Записів: "+currentArticles.length+".";
  }catch(err){
    $("status").className="status error";
    $("status").textContent="Не вдалося: "+err.message+" Оберіть навчальний режим.";
  }finally{buttons.forEach(b=>b.disabled=false)}
}
$("demoBtn").addEventListener("click",()=>run("demo"));
$("liveBtn").addEventListener("click",()=>run("live"));
$("csvBtn").addEventListener("click",()=>{
 if(!currentArticles.length){alert("Спочатку отримайте записи.");return}
 const quote=x=>'"'+String(x??"").replace(/"/g,'""')+'"';
 const rows=[["title","date","url"],...currentArticles.map(x=>[x.title,x.date,x.url])];
 const csv="\ufeff"+rows.map(row=>row.map(quote).join(",")).join("\r\n");
 const link=document.createElement("a");
 const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
 link.href=url;link.download="armyinform_training.csv";link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
$("checkQuiz").addEventListener("click",()=>{
 const ids=["q1","q2","q3","q4"];
 const answered=ids.filter(id=>$(id).value).length;
 const score=ids.filter(id=>$(id).value==="correct").length;
 $("quizResult").textContent="Правильно: "+score+" із 4. "+(answered<4?"Не всі питання заповнені.":score===4?"Чудово!":"Поверніться до пояснення структури проєкту.");
});