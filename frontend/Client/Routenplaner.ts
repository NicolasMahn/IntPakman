namespace Routenplaner {
    window.addEventListener("load", handleLoad);
    let liste:HTMLElement;
    let karte:HTMLElement;
    async function handleLoad(_event: Event): Promise<void> {
        liste= <HTMLElement>document.getElementById("liste");
        karte = <HTMLElement>document.getElementById("karte");
        liste.addEventListener("click", show_optimal_route);
        karte.addEventListener("click", show_route_on_map)
    }

    async function show_optimal_route(): Promise<void> {
        liste.style.backgroundColor = "#FFCC00";
        karte.style.backgroundColor = "gray";
        let response: Response = await fetch("http://localhost:5001");
        let responseText: any = await JSON.parse(await response.text());
        let table_array: any = [];
        for (let array of responseText) {
            table_array.push(array);
        }
        generate_table(table_array);
    }
    
    function show_route_on_map() {
        karte.style.backgroundColor = "#FFCC00";
        liste.style.backgroundColor = "gray";
        let table: HTMLTableElement = <HTMLTableElement>document.querySelector("table");
        table.hidden=true;
        
    }
    
    function generate_table(array: any) {
        let table: HTMLTableElement = <HTMLTableElement>document.querySelector("table");
        table.hidden=false;
        if (table.rows.length <= 1) {
            generate_head(table);
            for (let element of array) {
                let tr: HTMLElement = <HTMLElement>document.createElement("tr");
                table.appendChild(tr);
                for (let key in element) {
                    if (key === "street") {
                        
                        let sendungsnummer: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('td');
                        let strasse: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('td');
                        let hausnummer: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('td');
                        
                        sendungsnummer.textContent = Object(element)["sendungsnummer"];
                        strasse.textContent = Object(element)["street"];
                        hausnummer.textContent = Object(element)["house_number"];
                        tr.appendChild(sendungsnummer);
                        tr.appendChild(strasse);
                        tr.appendChild(hausnummer);
                    }
                    
                }
            }
        }
        
    }
    
    function generate_head(table:HTMLElement){
        let thead:HTMLTableSectionElement = <HTMLTableSectionElement>document.createElement("thead");
        let tr: HTMLElement = <HTMLElement>document.createElement("tr");
        let th: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('th');
        let th2: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('th');
        let th3: HTMLTableCellElement = <HTMLTableCellElement>document.createElement('th');
        th.textContent = "Sendungsnummer";
        th2.textContent="Straße";
        th3.textContent="Hausnummer";

        table.appendChild(thead);
        thead.appendChild(tr);
    
        tr.appendChild(th);
        tr.appendChild(th2);
        tr.appendChild(th3);

    }
}
