- Foraging Core API is a backend service developed based on Quarkus framework
     - Provide HTTP RESTful API based on [[Foraging core model]]
     - API design using HATEOAS
     - Use the architectural style of Smart Domain
-
- Core Technology Stack:
    - Basic: Quarkus + Kotlin
    - Web: JAX-RS + HATEOAS
    - Persistence: Mysql + Flyway + Hibernate
    - Test: junit5 + mockito + testcontainers + rest-assured
    - Deploy: Gradle + Docker + GraalVM + K8s

- Foraging Core API Architecture design:
  - ```mermaid
  C4Component
  title Foraging Core Api Architecture

              System(ui, "foraging-ui", "react", "whiteboard-like application")
              System_Ext(collaborative, "foraging-collaborative-server", "nestjs", "Collaboration service")
              
          
              System_Boundary(core, "foraing-core-api") {
                  Container_Boundary(api, "API") {
                      Component(auth, "Auth", "JWT", "Authentication based on JWT Header")
                      Component(api, "API", "JAX-RS + HATEOAS", "RESTful API")
                      Component(representation, "representation", "HAL", "HATEOAS response object")
          
                      Rel(ui, auth, "HTTP RESTful")
                      Rel(collaborative, auth, "HTTP RESTful")
                      Rel(auth, api, "filter")
                      Rel(api, representation, "response")
                      Rel(api, model, "call")
                  }
          
                  Container_Boundary(domain, "Domain") {
                      Container_Boundary(associations, "Associations") {
                          Component(hibernate, "Hibernate", "quarkus-hibernate", "Hibernate implementation of domain model association relationship")
                          Component(mappers, "mappers", "ORM", "The persistent real mapping relationship of the domain model")
                          Component(memory, "memory", "kotlin", "Associative Memory's Line of Sight")
          
                          Rel(model, hibernate, "HasOne/HasMany")
                          Rel(hibernate, mappers, "")
                          Rel(mappers, memory, "")
                      }
          
                      Component(description, "description", "kotlin", "Domain Model Value Objects")
                      Component(model, "model", "kotlin", "domain model")
          
                      Rel(model, description, "own")
                  }
              }
          
              System_Boundary(dbms, "storage") {
                  ContainerDb_Ext(redis, "Cache", "redis", "YDoc Cache")
                  ContainerDb(mysql, "Database", "Mysql", "persistent data")
              }
          
              
              BiRel(ui, collaborative, "Http / Web Socket")
              Rel(collaborative, redis, "sync")
              Rel(hibernate, mysql, "persist")
          ```
- Models and Relationships Between Models

    - There are 4 types of base models: Entity, HasMany, HasOne, Many
        - Entity: The basic interface of the model, each model needs to implement the Entity interface, which includes two attributes of identity and description, where identity represents the id of the model, and description represents the specific value attribute of the model, such as name, createdTime
         - HasMany: represents a one-to-many association between models
         - HasOne: Indicates a one-to-one association between models
         - Many: the abstract interface of [many] objects in a one-to-many relationship

    - Model design
        - FacilitatedActivity: the model of the workshop (workshop), related concepts are represented by FacilitatedActivity
         - Invitation: Invitation model, representing an invitation for Facilitated activity, an invitation includes user, role, createdTime and other information
         - User: User model, including user name, avatar and other information
         - Role: The model of the role. In the Foraging system, there are currently only two roles: Participant and Facilitator
    - Model Associated Object Design
        - FacilitatedActivities: A collection class of FacilitatedActivity, with findById, findAll and other behaviors
         - FacilitatedActivity.Invitations: The abstract interface of FacilitatedActivity and Invitation one-to-many association, inheriting HasMany, can define the behavior of related operations Invitation, such as add invitation, findAll invitations
         - Reference<User>: the implementation of the one-to-one association between Invitation and User, implement the HashOne<User> interface, indicating that there is a User in an Invitation
         - Reference<Role>: the implementation of the one-to-one association between Invitation and Role, and implement the HashOne<Role> interface, indicating that there is a Role in an Invitation
         - The relationship between FacilitatedActivity and User is realized through Invitation, FacilitatedActivity one-to-many Invitation, Invitation one-to-one User
    
    - The detailed model is represented in the class diagram:
        - Class Diagram
            - ![image.png](../assets/image_1683049437499_0.png)
            - ```mermaid
          ---
          title: Foraging Core Api
          ---
          classDiagram
              FacilitatedActivities "1" --> "*" FacilitatedActivity
              FacilitatedActivity *--   FacilitatedActivityDescription
              FacilitatedActivity *--   Invitations
              
              Invitations <|-- FacilitatedActivityInvitations
              Invitations : add(InvitationDescription description, User user, Role role)
              <<interface>> Invitations
          
              FacilitatedActivityInvitations "1" *-- "*" Invitation
              
              Invitation *-- InvitationDescription
              Invitation "1" *-- "1" User
              Invitation "1" *-- "1" Role
              
          
              User *-- UserDescription
              Role *-- RoleDescription
              RoleDescription *-- RoleName
          
              class FacilitatedActivity{
                  <<Entity>>
                  String identity
                  FacilitatedActivityDescription description
                  Invitations invitations
              }
          
              class FacilitatedActivityInvitations{
                  <<Associations.Hibernate>>
                  String identity
                  List invitations
              }
          
              class FacilitatedActivityDescription{
                  <<Value>>
                  String name
                  Instant createdTime
                  String space
              }
          
              class Invitation{
                  <<Entity>>
                  String identity
                  InvitationDescription description
                  HasOne<User> user
                  HasOne<Role> role
              }
          
              class InvitationDescription{
                  <<Value>>
                  Instant createdTime
              }
          
              class User{
                  <<Entity>>
                  String identity
                  UserDescription description
              }
          
              class UserDescription{
                  <<Value>>
                  String origin
                  String name
                  String photo
              }
          
              class Role{
                  <<Entity>>
                  String identity
                  RoleDescription description    
              }
          
              class RoleDescription{
                  <<Value>>
                  RoleName name   
              }
          
              class RoleName{
                  «enumeration»
                  Facilitator
                  Participant   
              }
          
              class FacilitatedActivities{
                  <<interface>>
                  Otpional<FacilitatedActivity> findById(String id)
              }
          ```

- Based on [[Foraging Core API architecture design]], the development idea of Foraging Core API is as follows:
     - API design
         - Design RESTful API (Path/Params/Request body/Response body) based on [[Foraging Core Model]]
         - Test API via QuarkusTest and RestAssured, use mockito stub related dependencies, such as Model and sub APIs
     - Model design
         - Build the model Model based on [[Foraging core model]], the content of the Model includes
             - Identity: the unique identifier of the model, usually a UUID of type String
             - Description: the specific data items of the model, such as Name, CreatedTime
             - Association: The relationship between models, usually HasMany and HasOne
                 - You can define specific association behaviors, such as getAll, findById, add, etc.
                 - The Association of the Model layer only has an abstract interface and does not have a specific implementation
         - Test Model by way of Junit5 unit test
     - Association implementation
         - Implementation of the Association interface in the Model layer
             -Using Hibernate as the ORM framework, by defining PersistEntity in mappers to map the relationship between Model and PersistEntity, and the conversion method of Model and PersistEntity to achieve data persistence
             - If there is a combination relationship between Models, such as embedded, Association is generally implemented in-memory
         - Testing Association via QuarkusTest and Testcontainer
     -Authentication
         - The Token of the Foraging Core API is in the form of JWT, and the Filter will check the authorization header to verify the user's identity information
         - Authentication uses Quarkus-Security to manage the Security Context, and you can use the annotation provided by Quarkus-Security in the API to do fine-grained permission control
         - API tests can use `@TestSecurity(authorizationEnabled = false)` to Skip Auth related controls.
     -Tips:
         - Each layer of test has Helper to encapsulate some reusable operations, such as creating a model, implementing Stub Association, etc.
         - Authentication related tasks do not need to be implemented again
- Combined with development ideas, the Foraging Core API process is as follows:
     - [[Use Mockito stub model to test API with QuarkusTest and RestAssured ]]
     - [[Use the Mockito stub model to test API access control with QuarkusSecurityTest and RestAssured]]
     - [[Using Mockito stub association, testing Model via Junit5]]
     - [[Use Testcontainer fake mysql, use QuarkusTest to verify Association persistence]]
