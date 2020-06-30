from typing import Dict, Optional

from aiohttp import web


async def test_spec_file(swagger_file, aiohttp_client):
    async def get_all_pets(request, limit: Optional[int] = None):
        pets = []
        for i in range(limit or 3):
            pets.append({"id": i, "name": f"pet_{i}", "tag": f"tag_{i}"})
        return web.json_response(pets)

    async def create_pet(request, body: Dict):
        return web.json_response(body, status=201)

    async def get_one_pet(request, pet_id: int):
        if pet_id in (1, 2, 3):
            return web.json_response(
                {"id": pet_id, "name": f"pet_{pet_id}", "tag": f"tag_{pet_id}"}
            )
        return web.json_response(
            {"code": 10, "message": f"pet with ID '{pet_id}' not found"}, status=500
        )

    swagger = swagger_file()
    swagger.add_routes(
        [
            web.get("/pets", get_all_pets),
            web.get("/pets/{pet_id}", get_one_pet),
            web.post("/pets", create_pet),
        ]
    )

    client = await aiohttp_client(swagger._app)

    resp = await client.get("/pets", params={"limit": 1})
    assert resp.status == 200
    assert await resp.json() == [{"id": 0, "name": "pet_0", "tag": "tag_0"}]

    resp = await client.get("/pets")
    assert resp.status == 200
    assert await resp.json() == [
        {"id": 0, "name": "pet_0", "tag": "tag_0"},
        {"id": 1, "name": "pet_1", "tag": "tag_1"},
        {"id": 2, "name": "pet_2", "tag": "tag_2"},
    ]

    req = {"id": 10, "name": "pet", "tag": "tag"}
    resp = await client.post("/pets", json=req)
    assert resp.status == 201
    assert await resp.json() == req

    resp = await client.get("/pets/1")
    assert resp.status == 200
    assert await resp.json() == {"id": 1, "name": "pet_1", "tag": "tag_1"}

    resp = await client.get("/pets/1")
    assert resp.status == 200
    assert await resp.json() == {"id": 1, "name": "pet_1", "tag": "tag_1"}

    resp = await client.get("/pets/100")
    assert resp.status == 500
    assert await resp.json() == {"code": 10, "message": "pet with ID '100' not found"}


async def test_route_out_of_spec_file(swagger_file, aiohttp_client):
    async def handler(request):
        return web.json_response()

    swagger = swagger_file()
    swagger.add_route("POST", "/r", handler)

    client = await aiohttp_client(swagger._app)

    resp = await client.post("/r", json={"array": "whatever"})
    assert resp.status == 200
