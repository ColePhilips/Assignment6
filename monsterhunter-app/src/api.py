from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://ColePhilips:MongoDBDragon22!@monsterhunterdb.3kgwi.mongodb.net/mhw_db?retryWrites=true&w=majority&appName=MonsterHunterDB"  # MongoDB URI
CORS(app)
mongo = PyMongo(app)
# Check if mongo is initialized
if mongo is None:
    print("MongoDB connection failed!")
else:
    print("MongoDB connection established.")
api = Api(app)

# Swagger for API documentation
swaggerui_blueprint = get_swaggerui_blueprint('/swagger', '/static/swagger.json', config={'app_name': "Monster Hunter API"})
app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

class Monster(Resource):
    # Create: POST /monsters
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        monster_type = data.get("type")
        
        if not name or not description:
            return {"message": "Name and description are required!"}, 400
        existing_monster = mongo.db.monsters.find_one({"name": name})
        if existing_monster:
            return {"message": "Monster with this name already exists!"}, 400
        
        # Insert monster into the database with a custom "id"
        monster = {
            "id": int(mongo.db.monsters.count_documents({}) + 3),  # Custom "id" generation
            "name": name,
            "description": description,
            "type": monster_type
        }
        result = mongo.db.monsters.insert_one(monster)
        
        return jsonify({
            "id": monster["id"],
            "name": name,
            "description": description,
            "type": monster_type
        })

    # Read: GET /monsters or GET /monsters/<id>
    def get(self, monster_id=0):
        if monster_id == 0:
            # Fetch all monsters
            monsters = mongo.db.monsters.find()
            result = []
            for monster in monsters:
                result.append({"id": monster["id"], "name": monster["name"], "description": monster["description"], "type": monster["type"]})
            return jsonify(result)
        else:
            # Fetch a specific monster by ID
            monster = mongo.db.monsters.find_one({"id": int(monster_id)})
            if not monster:
                return {"message": "Monster not found"}, 404
            return jsonify({"id": monster["id"], "name": monster["name"], "description": monster["description"], "type": monster["type"]})

    # Update: PUT /monsters/<id>
    def put(self, monster_id):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        monster_type = data.get("type")

        if not name or not description:
            return {"message": "Name and description are required fields"}, 400
        
        result = mongo.db.monsters.update_one(
            {"id": int(monster_id)},
            {"$set": {"name": name, "description": description, "type": monster_type}}
        )
        
        if result.matched_count == 0:
            return {"message": "Monster not found!"}, 404
        
        return jsonify({
            "id": monster_id,
            "name": name,
            "description": description,
            "type": monster_type
        })

    # Delete: DELETE /monsters/<id>
    def delete(self, monster_id):
        result = mongo.db.monsters.delete_one({"id": int(monster_id)})
        if result.deleted_count == 0:
            return {"message": "Monster not found!"}, 404
        return {"message": "Monster deleted successfully!"}, 200

# Set up the routes for the Monster resource
api.add_resource(Monster, "/monsters", "/monsters/<int:monster_id>")

if __name__ == "__main__":
    app.run(debug=True)