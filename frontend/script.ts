window.onload=()=>{
    const liste:HTMLElement = <HTMLElement>document.getElementById("liste")
    const karte = <HTMLElement>document.getElementById("karte")
    liste.addEventListener("click",()=>{liste.style.backgroundColor="#FFCC00";karte.style.backgroundColor="gray"});
    karte.addEventListener("click",()=>{karte.style.backgroundColor="#FFCC00";liste.style.backgroundColor="gray"});

}