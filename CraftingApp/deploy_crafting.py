import os
import json
import requests

API_URL = "https://api.avrae.io/customizations/gvars/{}"

TOKEN = os.environ.get("AVRAE_TOKEN")

AVAILABLE_GVARS = [
    "3581ee0e-a689-4a8c-ae6b-2e985be492d4",
    "f9d408f5-2b61-4548-87c4-49a761b0a855",
    "c1c1638a-ef36-4af6-b7b8-634a02358708",
    "7e0b8a32-49e5-451d-bce1-a22ad4dd0cc6",
    "a1ebaa01-6b48-4052-b4cf-5055056c85aa",
    "f820733a-860c-4f60-86bb-5062228eb79d",
    "f60b8850-fd76-4103-be5e-fc2d5aa64b25",
    "4d94f1bd-a215-4009-a41e-aa24531761f8",
    "617fd614-8ed2-40c9-8d94-6f70a1cc513b",
    "379b1487-741d-469f-a30d-cedfd6379a3b",
    "066a85d6-1aa9-410d-89d5-47f006472762",
    "e764bc21-168f-42df-bffa-5bcd024cb5e1",
    "feaa6998-c8a0-4a98-9ee9-f2ae40eb4afa",
    "b0a52b91-9aa5-41bb-bd0a-16f822b66839",
    "1cdd1563-db06-4a00-b406-13bf3f0397a3",
    "742bc19a-0449-4fcf-896e-303d18563b4d",
    "e01a1445-a0fa-464d-9d38-866cf0613282",
    "dfb5f94e-9c69-4059-b69c-9f69b5c4d0b2",
    "3888bc8c-0b99-4705-ab66-9d526b5f0d04",
    "3fc5b2f5-1f14-476a-a84c-b51638c91fd3",
    "f9772fb0-77c7-45c8-aa1e-3c42a8e9ff0d",
    "f69e0e5a-27ac-4294-8adc-b509bfb9de8b",
    "2e7c140d-81ea-49df-a348-5e78461f3272",
    "1f6f968e-11aa-4574-99d6-c67024d372b5",
    "5a5040ba-0bb0-4458-bcd3-60d6d964b822",
    "ddc31d57-6f32-49eb-a533-13e75ff3524e",
    "5d91f458-8eb6-4b4c-b738-7221190ee4eb",
    "9c3802e8-d4dc-421e-956c-24a01ff90aa1",
    "b17d9a7a-f4a0-4366-95f3-5376cf93102f",
    "effeeefd-05bb-42ec-a654-488636642f0b",
    "ef3d68f6-dd01-4235-ad98-43d700775f6b",
    "3de7eab4-43e6-4cfc-979d-b43108d57366",
    "dab0879e-25e9-4dab-97d2-a7dcd2602a14",
    "b8a9701c-435e-4a68-b7b2-6bb71221fe59",
    "d4962764-16da-424b-ab05-0cc9e1c0c8d8",
    "f3cbd6ed-20ee-492f-a752-cc12a283cc21",
    "19a5d17f-58e6-4582-8cbc-03378af38ca6",
    "81823854-eed3-4ffc-9e05-ed027230b180",
    "f6a514c9-1ac1-4ed2-a750-efb90395d0ae",
    "d7d17def-4082-49ee-97d9-7d1e9b508f93",
    "cc252414-a30b-4ff7-a0fd-b2373466dc2b",
    "e9e0885d-0e10-416d-8742-fda93cc624c4",
    "6409335c-b043-4b2c-b605-ae0ce6bd8dd1",
    "9152f400-5e8d-4c42-8e6a-4e89e5da08b5",
    "8672ba8a-9888-4a87-84ef-5cc09a7fcb4c",
    "8f8bc5aa-7bf3-43ed-aa18-1531928e5902",
    "4f178345-3011-4d1f-83d1-4efe4ed943e1",
    "3112751d-6024-4a96-bce8-5512d63aeb2b",
    "33a7c31d-5a7a-4c9d-a654-b1aacc4de3d1",
    "f3e13c6d-6c10-494d-8cf2-2141455f21fa",
    "440ccb97-7855-4a76-983e-29a36c3ea03d",
    "6dfdcf08-6484-4866-82f9-f0bf7afe9f71",
    "5b21dcb8-ef5a-4357-a117-0570d7233f67",
    "6b0b98ff-f700-4ba0-805b-ad8af54978a2",
    "a8cc1398-c95a-4776-b133-7cefec09ad3a",
    "3a1777d6-e43d-405b-860f-867250af7c74",
    "8f6f6ffc-f85b-48c6-827d-0fbac2b8fb1c",
    "a981fe37-6c60-4a4a-a1b5-6df6d0ada1fa",
    "d896ce1b-f26d-44ab-a5ce-89061ac8d4f6",
    "636983d9-1ff1-4612-b4f0-81e735b42632",
    "2fc2268e-0154-4535-a575-aa473ad58175",
    "819f15a0-e958-404b-828a-6fd4473dfe85",
    "d8894494-d277-4336-ab33-755d072559c8",
    "102772b9-5ee2-4412-bc65-3fef7fd90efc",
]

ALL_RECIPES = {}

with open("./CraftingApp/crafting.json", "r") as f:
    ALL_RECIPES = json.load(f)

print("Loaded {} recipes".format(len(ALL_RECIPES)))

session = requests.Session()

session.headers.update(
    {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
)

# paginate groups of 200
gvar_index = 0
temp_gvar = {}
for key, value in ALL_RECIPES.items():

    temp_gvar[key] = value
    if len(temp_gvar) == 200:
        response = session.post(
            API_URL.format(AVAILABLE_GVARS[gvar_index]),
            json={"value": json.dumps(temp_gvar)},
        )
        temp_gvar = {}
        print("Status:", response.status_code)
        print("GVAR:", AVAILABLE_GVARS[gvar_index])
        print("Response:", response.text)
        gvar_index += 1

response = session.post(
    API_URL.format(AVAILABLE_GVARS[gvar_index]),
    json={"value": json.dumps(temp_gvar)},
)

print("Status:", response.status_code)
print("GVAR:", AVAILABLE_GVARS[gvar_index])
print("Response:", response.text)

response.raise_for_status()
