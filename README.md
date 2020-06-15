# Property Advisor
(by [@ombharatiya](https://www.linkedin.com/in/ombharatiya))

- - -

### A demo app for a property advisor application using match feature:

**Check the deployed app here : [Property Advisor](https://property-advisor.herokuapp.com/).**

- - -
#### Problem Statement:

Agentdesks has a lot of properties from property sellers and searches requirements from property buyers which get added to a SQL database every day. Every day these multiple properties and search criteria get added through our application by agents. Write an algorithm to match these properties and search criteria as they come in based on 4 parameters such that each match has a  match percentage.

##### The 4 parameters are:

- Distance - radius (high weightage)
- Budget (high weightage)
- Number of bedrooms (low weightage)
- Number of bathrooms (Low weightage)
- Each match should have a percentage that indicates the quality of the match. Ex: if a property exactly matches a buyers search requirement for all 4 constraints mentioned above, it’s a 100% match.  
- Each property has these 6 attributes - Id, Latitude, Longitude, Price, Number of bedrooms, Number of bathrooms
- Each requirement has these 9 attributes - Id, Latitude, Longitude, Min Budget, Max budget, Min Bedrooms required, Max bedroom reqd, Min bathroom reqd, Max bathroom reqd.

#### Functional requirements:

1. All matches above 40% can only be considered useful.
2. The code should scale up to a million properties and requirements in the system.
3. Requirements can be without a min or a max for the budget, bedroom and a bathroom but either min or max would be surely present.
4. For a property and requirement to be considered a valid match, distance should be within 10 miles, the budget is +/- 25%, bedroom and bathroom should be +/- 2.
5. If the distance is within 2 miles, distance contribution for the match percentage is fully 30%
6. If the budget is within min and max budget, budget contribution for the match percentage is full 30%. If min or max is not given, +/- 10% budget is a full 30% match.
7. If bedroom and bathroom fall between min and max, each will contribute full 20%. If min or max is not given, match percentage varies according to the value.
8. The algorithm should be reasonably fast and should be quick in responding with matches for the users once they upload their property or requirement.

#### Assumptions made:

- Since it is not mentioned that the valid budget +/- 25% has to be taken from min/max budget value, I assumed the average value to calculate the +/- 25% and the added both sides.
- Assuming all the data will be provided
- Created 1000 properties mock data in database to match with the requirements.
  - assumed bedrooms & bathrooms between 1 to 6
  - assumed price between $ 1k to 10k
- Using [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) to calculate distance between two points in miles
   


#### Algorithm used:

I used linear proportion conversion algorithm to generate results.
Here's the formula for it:
```
OldRange = (OldMax - OldMin)  
NewRange = (NewMax - NewMin)  
NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
```

Here's the steps for one data: 
(example of price - budget matching):
- given min & max budget and price of a property
- calculate the average budget 
- define boundaries for valid to 100% matching condition
- using above expression to find the matching percentage
- returning data

#### Request Object Model:

```
property_request_object_example = {
    "lat": 18.3721392,
    "lon": 121.5111211,
    "minBedrooms": 1,
    "maxBedrooms": 2,
    "minBathrooms": 1,
    "maxBathrooms": 4,
    "minBudget": "8305.39",
    "maxBudget": "18305.39"
}

```

#### Calculations:

After indivisually calculating matching of every field, I'm then merging them according to the provided weightage:

```
DISTANCE_WEIGHT = 0.3
BUDGET_WEIGHT = 0.3
BATHROOM_WEIGHT = 0.2
BEDROOM_WEIGHT = 0.2

Result(in %age)  = distance_match * DISTANCE_WEIGHT
        + budget_match * BUDGET_WEIGHT
        + bedroom_match * BEDROOM_WEIGHT
        + bathroom_match * BATHROOM_WEIGHT

```

Refer this file to see all the business logic: [Business Logic](https://github.com/ombharatiya/property-advisor/blob/master/apiservices/core/RealState/driver.py)

- - - 

#### Deployment, Hosting & Demo work:

- **Created Django Project to add this functionalities into an app**
- **Created Server Side rendered UI Form and Result Property List**
- **Validation on Form Fields in UI itself to handle different case**
- **Using Docker for Deployement**
- **Hosted the code on Git**
- **Serving the App Container on Heroku cloud**

Thank you :)

Copyright @ombharatiya
- - -
