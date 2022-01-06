"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const Http = require("http");
const Url = require("url");
const Mongo = require("mongodb");
var Routenplaner;
(function (Routenplaner) {
    let collection;
    let databaseUrl = "mongodb+srv://frontend:simple@cluster0.lalug.mongodb.net/routenplaner?retryWrites=true&w=majority";
    start_server(5001);
    connect_to_database(databaseUrl);
    function start_server(_port) {
        let server = Http.createServer();
        console.log("Server starting on port:" + _port);
        server.listen(_port);
        server.addListener("request", handleRequest);
    }
    function connect_to_database(_url) {
        return __awaiter(this, void 0, void 0, function* () {
            let options = { useNewUrlParser: true, useUnifiedTopology: true };
            let mongoClient = new Mongo.MongoClient(_url, options);
            yield mongoClient.connect();
            collection = mongoClient.db("routenplaner").collection("routen");
            console.log("Database connection ", collection != undefined);
        });
    }
    function handleRequest(_request, _response) {
        _response.setHeader("content-type", "text/html; charset=utf-8");
        _response.setHeader("Access-Control-Allow-Origin", "*");
        let url = Url.parse(_request.url, true);
        get_route(_request, _response);
    }
    function get_route(_request, _response) {
        return __awaiter(this, void 0, void 0, function* () {
            let results = collection.find();
            let routes = yield results.toArray();
            let route = routes[routes.length - 1];
            let addresses = Object(route)["route_data"];
            _response.writeHead(200, { 'Content-Type': 'application/json' });
            _response.write(JSON.stringify(addresses));
            _response.end();
        });
    }
})(Routenplaner = exports.Routenplaner || (exports.Routenplaner = {}));
//# sourceMappingURL=server.js.map