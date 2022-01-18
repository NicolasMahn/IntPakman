var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var Routenplaner;
(function (Routenplaner) {
    window.addEventListener("load", handleLoad);
    let liste;
    let karte;
    let anzeigen;
    function handleLoad(_event) {
        return __awaiter(this, void 0, void 0, function* () {
            liste = document.getElementById("liste");
            karte = document.getElementById("karte");
            anzeigen = document.getElementById("anzeigen");
            liste.addEventListener("click", get_input);
            karte.addEventListener("click", show_route_on_map);
            anzeigen.addEventListener("click", get_input);
        });
    }
    function get_input() {
        let formData = new FormData(document.forms[0]);
        let numbers = [];
        for (let entry of formData) {
            numbers.push(entry[1]);
        }
        console.log(numbers);
        show_optimal_route(numbers);
    }
    function show_optimal_route(numbers) {
        return __awaiter(this, void 0, void 0, function* () {
            liste.style.backgroundColor = "#FFCC00";
            karte.style.backgroundColor = "gray";
            let poststation = numbers[0];
            let district = numbers[1];
            let date = numbers[2];
            let response = yield fetch("http://localhost:5001?district=" + district + "&poststation=" + poststation + "&date=" + date);
            let statuscode = response.status;
            if (statuscode === 200) {
                let responseText = yield JSON.parse(yield response.text());
                let table_array = [];
                for (let array of responseText) {
                    table_array.push(array);
                }
                generate_table(table_array);
            }
            else {
                alert(yield response.text());
                let table = document.querySelector("table");
                table.hidden = true;
            }
        });
    }
    function show_route_on_map() {
        karte.style.backgroundColor = "#FFCC00";
        liste.style.backgroundColor = "gray";
        let table = document.querySelector("table");
        table.hidden = true;
    }
    function generate_table(array) {
        let table = document.querySelector("table");
        table.hidden = false;
        if (table.rows.length <= 1) {
            generate_head(table);
            for (let element of array) {
                let tr = document.createElement("tr");
                table.appendChild(tr);
                for (let key in element) {
                    if (key === "street") {
                        let sendungsnummer = document.createElement('td');
                        let strasse = document.createElement('td');
                        let hausnummer = document.createElement('td');
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
    function generate_head(table) {
        let thead = document.createElement("thead");
        let tr = document.createElement("tr");
        let th = document.createElement('th');
        let th2 = document.createElement('th');
        let th3 = document.createElement('th');
        th.textContent = "Sendungsnummer";
        th2.textContent = "Straße";
        th3.textContent = "Hausnummer";
        table.appendChild(thead);
        thead.appendChild(tr);
        tr.appendChild(th);
        tr.appendChild(th2);
        tr.appendChild(th3);
    }
})(Routenplaner || (Routenplaner = {}));
//# sourceMappingURL=Routenplaner.js.map