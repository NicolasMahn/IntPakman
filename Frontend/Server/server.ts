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
        let poststation:string|string[]  = url.query["poststation"];
        let district:string|string[] = url.query["district"];
        let date:string|string[] = url.query["date"];
            get_route( _response,Number(poststation),Number(district), date);

    }

    async function get_route(_response: Http.ServerResponse, _poststation:number,_district:number,_date:string|string[]): Promise<void> {
        let results: Mongo.Cursor = collection.find();
        let routes: string[] = await results.toArray();
        let final_routes:string[] = [];

        for(let element of routes){
            if(Object(element)["district"] ===_district && Object(element)["post_station"]===_poststation && Object(element)["date"]===_date){
                final_routes.push(element);
            }
        }
        if(typeof final_routes[0]!='undefined' && final_routes[0]){
            let addresses:string[] = Object(final_routes[0])["route_data"];  
            _response.writeHead(200,{'Content-Type':'application/json'}) 
            _response.write(JSON.stringify(addresses));
                _response.end();
        }
        else{
            _response.writeHead(400,{'Content-Type':'application/json'})  
            _response.write("No matching Data found :(");
            _response.end();
        }

    }
}


