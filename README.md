# Introduction
## Proyect objectives
This project objective is to design and develop an application that facilitates the connection between hosts and customers, promoting a similar experience to Airbnb.
The users will be able to use this app to: list properties to rent and leave reviews and ratings about their experience. This approach ensures that not only hosts can monetize their 
spaces but also a way to give travelers various options that adapt to their necessities.

##Proyect scope
The scope of this project includes but is not limited to, the following functionalities.
  * List of properties: users can create, update, and delete. This includes a detailed description, prices, and amenities.
  * User management: the app will allow users to register, login, and manage their profile.
  * Review system: travelers will be able to leave reviews and ratings of the places they have visited, this will help other travelers when deciding on places to rent.
  * Searching and filtering properties: implements a way to filter properties according to different criteria such as location, price, amenities, and other characteristics

## Key components
This document facilitates a detailed description of the structure of this project, including the key components of the main classes, the relationship between them, and the flow of interaction
between the user and the underlying system. This aims to help the developer and the parts involved to understand the design and the implementation of the system.
Moreover, this document will serve as a guide for further improvements and the upkeep of the app. In times when new necessities and requirements appear, new functionalities will be able to integrate without 
compromising the stability and efficiency of the established system.

# High-Level Architecture
## Layer system
The system architecture is based on a layered approach and uses the facade pattern to simplify the interactions between the user and the system. It can be decomposed into three layers: presentation, business logic
and persistence. Each of these layers will play a distinctive and important role in ensuring that the application functions smoothly and that it accomplishes the requirements of the users

## Presentation Layer
###Description
This layer includes the user interface, it is where users interact with the system.
###Functionality
Its purpose is to receive the user request transmit it to the logic layer, and display to the user information. This includes:
  * user registration/login
  * property listing
  * user profile, where they can update their information
  * property publishing, where owners can list a series of associated amenities
  * reviews and rating of properties
  
## Business Logic Layer
###Facade
Adds a simplified interface to interact with the business logic, hiding the complexity of the system.

###Core Logic
It contains the logical core of the business and processes the essential operations, such as location creation, user management, and review integration. For example, if a user wants to comment on a property, the request will be processed here.

###Data access layer
Manages the persistence of data, and the communication with the database. It allows to storage and load of data, ensuring that the information remains coherent. The database contains information about users, properties, reviews, and ratings

# Business Logic Layer
## Description
This diagram presents the entities of the logical layer, showing their attributes and methods. Includes: Users, Places, Amenities, and Reviews.
  1. User Class
    Encapsulates all the essential information about the users, and also includes the methods necessary for managing user registration and modification. The inclusion of an admin attribute allows access to different types of permissions.
  2. Place Class
    This is fundamental in the system, for it represents the available properties for renting. Their methods allow full control of the place's information, ensuring the capacity to be created, updated, and deleted efficiently.
  3. Amenities Class
    The Amenity class is fundamental for enhancing the user experience on the HBnB platform. Amenities represent additional features of places, such as a pool, gym, Wi-Fi, etc. By allowing the creation, updating, and deletion of amenities,
    the system becomes more flexible and can adapt to different types of properties and their characteristics.
  5. Review Class
    It allows users to share their experiences about the places. This not only enriches the platform but also provides valuable information to future users. The ability to create, update, and delete reviews encourages interaction and feedback within the system.
##Design Decisions:  
The relationships between the classes have been defined to reflect the nature of the business. A user can create and manage multiple places, and each place can have multiple associated amenities. This means that when listing a place, not only can its description
and price be shown, but also the available amenities. Additionally, each place can receive multiple reviews, which allows users to share their experiences at different locations, and each review is tied to a user. This structure promotes data reuse and integrity.  

This class diagram provides a clear representation of how entities in the HBnB system are structured and related. The classes User, Place, Amenities, and Review are essential for the platform's functionality, allowing the management of users, accommodation listings,
and corresponding reviews. The design facilitates future system expansion and ensures that each component has a well-defined purpose and appropriate methods for handling it.

# API Interaction Flow
##User Registration

###Overview:
The sequence diagram illustrates the interaction flow between system components during the process of registering a new user. This process is crucial as it lays the foundation for users to access all application functionalities.

###Involved Actors:

  *User: The new user who wishes to register on the platform.
  *Presentation Layer: The user interface that receives user information.
  *Business Logic Layer: Responsible for processing the registration logic.
  *Persistence Layer: Handles storing the user's information in the database.
  
###Interaction Flow
  1. Registration Start:
  The user fills out a registration form in the Presentation Layer, providing their first name, last name, email address, and password.

  2. Registration Request:
  The Presentation Layer sends a request to the Business Logic Layer containing the new user's data.

  3. Data Validation:
  The Business Logic Layer receives the request and performs the following actions:
    *Validates that the provided data is correct (e.g., ensuring a valid email is provided).
    *If the validation fails, an error message is returned to the Presentation Layer.
    *The Persistence Layer checks if the user already exists in the database. If the user is found, an error message stating "user already exists" is sent to the Presentation Layer.
  4. User Creation:
  If the data is valid and the user is not already registered, the Business Logic Layer calls the Persistence Layer to create a new user record in the database.

  5. Database Storage:
  The Persistence Layer stores the user's information and generates a unique ID for the new user.
  Once this operation is completed, a success message is returned to the Business Logic Layer.

  6. Registration Confirmation:
  The Business Logic Layer sends a successful response to the Presentation Layer, indicating that the registration was completed.

  7. User Notification:
  The Presentation Layer displays a confirmation message to the user, informing them that their registration was successful and that they can now log in.

###Design Justification
The sequence diagram for user registration is essential to understand how data flows through the different layers of the application. This modular approach ensures that each component has clear responsibilities, making the system easier to maintain and scale. Additionally,
the data validation in the Business Logic Layer ensures that only valid and secure data is stored in the database, improving system integrity.

###Conclusion
This sequence diagram provides a visual representation of the user registration process in the HBnB application, highlighting the interactions between the different system components. It serves as a valuable tool for developers and stakeholders,
as it offers a clear understanding of how registration is performed and how user data is managed on the platform.

## Sequence Diagram: Creating a Place Listing

### Overview:
The sequence diagram illustrates the interaction flow between system components during the process of creating a new place listing by a user. This process is essential as it allows hosts to add available properties for rent on the platform.

### Interaction Flow
  1. Creation Start:
  The user completes a place creation form in the Presentation Layer, providing information such as title, description, price, location (longitude and latitude), and available amenities.

  2. Creation Request:
  The Presentation Layer sends a request to the Business Logic Layer with the new place’s data.

  3. Data Validation:
  The Business Logic Layer receives the request and performs the following actions:
    *Validates that all required fields are completed and that the data is correct (e.g., ensuring the price is a positive value).
    *If validation fails, an error message is returned to the Presentation Layer.
  
  4. Place Creation:
  If the data is valid, the Business Logic Layer calls the Persistence Layer to create a new place record in the database.

  5. Database Storage:
  The Persistence Layer stores the place’s information and generates a unique ID for the new listing.
  Once the operation is completed, a success message is returned to the Business Logic Layer.

  6. Creation Confirmation:
  The Business Logic Layer sends a successful response to the Presentation Layer, indicating that the place listing has been successfully created.

  7. User Notification:
  The Presentation Layer displays a confirmation message to the user, informing them that their listing has been successfully created and is now available for viewing by other users.

###Design Justification:
The sequence diagram for creating a place listing provides a clear view of how data is managed across the different layers of the application. This modular approach allows each component to have specific responsibilities, making system maintenance and scalability easier.
Additionally, the data validation in the Business Logic Layer ensures that only valid and accurate listings are stored in the database, improving system integrity.

###Conclusion:
This sequence diagram effectively illustrates the process of creating a new place listing in the HBnB application, highlighting the interactions between the various system components. It serves as a valuable tool for developers and stakeholders,
providing a clear understanding of how this process is executed and how place data is managed on the platform.

##Sequence Diagram: Review Submission

###Overview:
The sequence diagram illustrates the interaction flow between system components during the process of submitting a review by a user for a specific place. This process is essential for encouraging feedback and helping other users in their decision-making process.

###Interaction Flow
  1. Review Submission Start:
  The user completes a review form in the Presentation Layer, providing information such as the rating, comment, and possibly the place ID.

  2. Review Request:
  The Presentation Layer sends a request to the Business Logic Layer with the review details.

  3. Data Validation:
  The Business Logic Layer receives the request and performs the following actions:
    *Validates that all required fields are completed and that the rating is within the allowed range (e.g., between 1 and 5).
    *If validation fails, an error message is returned to the Presentation Layer.
     
  4. Review Creation:
  If the data is valid, the Business Logic Layer calls the Persistence Layer to create a new review record in the database.

  5. Database Storage:
  The Persistence Layer stores the review information, associates it with the corresponding place ID, and generates a unique ID for the review.
  Once the operation is completed, a success message is returned to the Business Logic Layer.

  6. Submission Confirmation:
  The Business Logic Layer sends a successful response to the Presentation Layer, indicating that the review has been successfully submitted.

  7. User Notification:
  The Presentation Layer displays a confirmation message to the user, informing them that their review has been successfully submitted and will be visible to other users.

### Design Justification:
The sequence diagram for review submission provides a clear representation of how data and interactions are managed across the different layers of the application. This modular approach ensures that each component has specific responsibilities,
making system maintenance and scalability easier. Additionally, data validation in the Business Logic Layer ensures that only valid and useful reviews are stored in the database, improving the quality of information available to other users.

### Conclusion:
This sequence diagram effectively illustrates the process of submitting a review in the HBnB application, highlighting the interactions between the various system components. It serves as a valuable tool for developers and stakeholders,
providing a clear understanding of how this process is carried out and how reviews are managed on the platform.

## Sequence Diagram: Request for a List of Places

### Overview:
The sequence diagram illustrates the interaction flow between system components during the process where a user requests a list of places based on certain criteria. This process is crucial in helping users find accommodation options that match their needs and preferences.

### Interaction Flow
  1. Search Start:
  The user enters search criteria in the Presentation Layer, such as location, price range, and desired amenities.

  2. Listing Request:
  The Presentation Layer sends a request to the Business Logic Layer with the user’s specified search criteria.

  3. Request Processing:
  The Business Logic Layer receives the request and performs the following actions:
    *Analyze the search criteria and construct a suitable query to retrieve the places that match those criteria.

  4. Database Query:
  The Business Logic Layer calls the Persistence Layer to obtain a list of places that meet the specified criteria.

  5. Data Retrieval:
  The Persistence Layer executes the query in the database and retrieves the places that match the search criteria.
  Once the operation is completed, the list of places is returned to the Business Logic Layer.

  6. Results Transmission:
  The Business Logic Layer sends the list of places to the Presentation Layer.
  
  7. Results Display:
  The Presentation Layer displays the list of places to the user, allowing them to explore the available options.

### Design Justification:
The sequence diagram for requesting a list of places provides a clear representation of how interactions between different system components are managed. This modular approach ensures that each component has specific responsibilities, facilitating the maintenance and scalability of the application.
The separation of search logic and data retrieval across the different layers optimizes each process, improving system efficiency.

### Conclusion:
This sequence diagram effectively illustrates the process of searching for and viewing places in the HBnB application, highlighting the interactions between the various system components. It serves as a valuable tool for developers and stakeholders,
providing a clear understanding of how the search process is carried out and how queries are managed on the platform.


