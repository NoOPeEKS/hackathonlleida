# Web application for Restb.ai API

## How to use:
1. Install the needed dependencies:
    * `pip install django`
    * `pip install pandas`
    * `pip install requests`

2. Instatiate the Django server using the following command:
    * `python3 manage.py runserver`

3. Access the web application through http://127.0.0.1:8000

## Data processing

Contains the processing of the data obtained from different requests done to the Restb.ia APIs to improve the data showability, and the usage for posterior purposes as can be doing predictions or enginieering new columns from the obtained ones.

Some predictions have been done to exemplify the usage of the processed data and some of the code has been used on the web to show the data obtained from the requests.

## Experimentation

With the before mentioned data and a predictor model like the Random Forest regressor, we have tried to explain with to which elements the algorithms behind the APIs evaluated the object importance related to the rating it gives after the evaluation and how to improve the house rating the easiest and cheapest way. However the RFR feature extraction didn't give us satisfactory results so we could not extract any information to continue with the experiment we planed. However we still tried with an specific kind of labels, the ones related to floors, to see if we could see something diferent, still, it wasn't the case and we couldn't work with the obtained results.
