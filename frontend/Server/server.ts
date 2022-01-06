import * as Http from "http";
import * as Url from "url";
import * as Mongo from "mongodb";
export namespace Routenplaner {

    let collection: Mongo.Collection;
    let databaseUrl: string = "mongodb+srv://frontend:simple@cluster0.lalug.mongodb.net/routenplaner?retryWrites=true&w=majority";

    start_server(5001);
    connect_to_database(databaseUrl);

    function start_server(_port: number | string): void {
        let server: Http.Server = Http.createServer();
        console.log("Server starting on port:" + _port);

        server.listen(_port);
        server.addListener("request", handleRequest);
    }

    async function connect_to_database(_url: string): Promise<void> {
        let options: Mongo.MongoClientOptions = { useNewUrlParser: true, useUnifiedTopology: true };
        let mongoClient: Mongo.MongoClient = new Mongo.MongoClient(_url, options);
        await mongoClient.connect();
        collection = mongoClient.db("routenplaner").collection("routen");
        console.log("Database connection ", collection != undefined);
    }

    function handleRequest(_request: Http.IncomingMessage, _response: Http.ServerResponse): void {
        _response.setHeader("content-type", "text/html; charset=utf-8");
        _response.setHeader("Access-Control-Allow-Origin", "*");
        let url: Url.UrlWithParsedQuery = Url.parse(_request.url, true);
            get_route(_request, _response);

    }

    async function get_route(_request: Http.IncomingMessage, _response: Http.ServerResponse): Promise<void> {
        let results: Mongo.Cursor = collection.find();
        let routes: string[] = await results.toArray();
        let route = routes[routes.length-1];
        let addresses:string[] = Object(route)["route_data"];  
        _response.writeHead(200,{'Content-Type':'application/json'}) 
        _response.write(JSON.stringify(addresses));
            _response.end();

    }
}


