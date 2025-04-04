from __future__ import annotations
from datetime import datetime
import typing
import strawberry
 

@strawberry.type
class User:
    id: int 
    email: str
    subscriptions: list[Subscription]

@strawberry.type
class Subscription:
    created_at: datetime
    is_active: bool
    location: Location
    user: User

@strawberry.type
class Location:
    name: str 
    latitude: float 
    longitude: float 
    created_by: User
    subscriptions: list[Subscription]



# prefill some data

all_users = []
all_users.append(User(id=69, email="past@hvl.no", subscriptions=[]))
all_users.append(User(id=42, email="lmkr@hvl.no", subscriptions=[]))
all_locations = []
all_locations.append(Location(name="Kronstad", latitude=60.3677625, longitude=5.53563056, subscriptions=[], created_by=all_users[1]))
all_locations.append(Location(name="Voss Stajson", latitude=60.6290599, longitude=6.4087378, subscriptions=[], created_by=all_users[0]))
s1 = Subscription(user=all_users[0], is_active=False, created_at=datetime(2024, 1, 1), location=all_locations[0])
s2 = Subscription(user=all_users[0], is_active=True, created_at=datetime(2024, 1, 15), location=all_locations[1])
s3 = Subscription(user=all_users[1], is_active=True, created_at=datetime(2023, 12, 10), location=all_locations[0])
all_locations[0].subscriptions.append(s1)
all_locations[0].subscriptions.append(s3)
all_locations[1].subscriptions.append(s2)
all_users[0].subscriptions.append(s1)
all_users[0].subscriptions.append(s2)
all_users[1].subscriptions.append(s3)

 
 

def get_users():
    return all_users

def get_locations():
    return all_locations

 
@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=get_users)
    locations: list[User] = strawberry.field(resolver=get_locations)



schema = strawberry.Schema(query=Query)

