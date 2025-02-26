# REST API Security with JWT and Keycloak

## Lab tasks (Friday 09-10/11)
- Provide REST API endpoints (public and private)
- Setup Keycloak IdP
- Setup clients, users, roles, and client scopes on Keycloak
- Integrate keycloak API for consuming JWT auth/authz token
- Configure keycloak as the 3rd party Identity Provider
- Set up CI/CD environment
- Test, test, test

## Example project for Auth/Authz using JWT for FastAPI RESTAPI and Keycloak IdP 
- To get started, visit and clone an example project at: https://github.com/tosdanoye/fastapi-keycloak-jwt
- The project contains a description to setup Keycloak IdP server and register services and users.
- In the GitHub workflow, you will find an example of how the test is setup to configure Keycloak, obtain token, and run the various tests.
- Check that the job passed but don't forget to set `USER1_PWD` and `USER2_PWD`as a GitHub Action secrets
- You may need to study the examples to replicate for your dynamic-frcm RESTAPI project. 