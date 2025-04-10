# Code Examples: _Middleware Lecture_

This respository contains some code examples w.r.t. different communication technologies

## GraphQL

GraphQL seeks to address the _N + 1_ request problem, i.e. that the available REST endpoints and their representations are not always sufficient
for the requester, who in turn then needs to issue multiple requests.
With GraphQL, front- and backend agree on a common schema once. The client can then dynamically define the expected
response entity by specifying a query based on the schema.

To try the example: Check out this code and navigate into the `graphql` folder below:
First run
```shell
poetry install
```
to download all dependencies.
Then, first inspect the classic HTTP endpoint:
```
cd graphql
poetry run fastapi dev api.py 
```
Afterwards, start the GraphQL server and inspect the URL that is poppin up:
```shell
poetry strawberry server schema.py
```

## gRPC

First, check out the code and the switch into the project.
Next, install dependencies with poetry:
```
poetry install
```
Then generate code with:
```shell
poetry run python -m grpc_tools.protoc -I./protos --python_out=grpc_demo --grpc_python_out=grpc_demo --pyi_out=grpc_demo protos/schema.proto
```
Now, you could try running both client and server (in two different shells):
```
poetry run python grpc_demo/server.py
poetry run python grps_demo/client.py
```

**Exercise Ideas:**
- Can you add methods for the other arithmetic opertions? You may have to extend the schema and re-generate the code.
- You may want to introduce exceptions into your results (division by zero)? What about changing the data type from integers to floating point numbers?
- What about schema evolution. Try generating a server with an old an newer schema versions? Are clients compatible?

## Serde Experiments

Make sure to have `jupyter` (lab) installed.
Then open `experiments.ipynb` in Jupyter and follow the instructions in order to set up a virtual envrionment.
Try playing around with different payload sizes and the effect on transmission speed.
You may want to add different serialization formats? Plot the results in a graph?
