#Contribution Guide

The following is a contributing guide for the TravelRank project which includes information on the APIs used, dependencies and project structure.

####Table of Contents

[API Usage](#api-usage)

[Dependencies](#dependencies)

[Virtual Environment](#virtual-environment)

[Project Structure](#project-structure)

[Testing](#testing)

##API Usage
We have used the Amadeus self-service travel API and the Nominatim Geocoding API.
The Geocodes are generated with a simple GET request to the [base URL](https://nominatim.openstreetmap.org/search?q=KEY&format=json&polygon=1&addressdetails=1)

To use the Amadeus API with the project, generate the API key and secret using the instructions [here](https://developers.amadeus.com/quick-start-guide/category?id=97&durl=335&parentId=NaN). Replace the API_KEY and API_SECRET in the requests class with those generated. 

##Dependencies
You will need to install certain packages like Pandas, Amadeus SDK for Python, scikit-learn, Pickle and the Python requests library for this project.

##Virtual Environment
We recommend using a virtual environment for this project using either virtualenv with and IDE or Conda as the package manager. For those interested in using Conda, we have provided an environment.yml file. To create the Conda environment and activate it, use:

    $conda env create -f environment.yml
    $source activate TravelRank
If updating the virtual environment or adding a new feature, use 

    $conda env update -n=TravelRank

##Project Structure
The project is divided into the backend and frontend packages. The backend has been built using Python while the frontend is designed using HTML, CSS, and Flask.
The backend package contains all the classes like Requests, Utilities, and Ranking.

##Testing
For testing we are using pytests with unittests to test individual methods of the classes to ensure reliability.