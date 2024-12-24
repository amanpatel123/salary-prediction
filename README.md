# salary-prediction

## Result and explaination
Test API - curl https://salary-prediction-yqrk.onrender.com/predict/salary/cohere/e3cb621a-75b8-467c-803c-4325fb0c1301

Models I tried 
- Random Forest and Linear Regression. Random forest was taking a lot of time to train (even on google collab) so had to stick with linear regression. But this can be improved
- Parsing from the web is not being done as of now. I will work on it as my next milestone
- Web api is hosted usin render - https://render.com/


Tempo's coding challenge

Using an online job posting, help us figure out what we should be paying our future hires! You may choose one of two paths (more full-stack or more backend+ML).

Sample Job Postings:
https://jobs.ashbyhq.com/cohere

Option 1

Build a model and API that takes a posting ID and returns the predicted salary.

You can use the following dataset to train your model (or another dataset if you prefer):
https://www.kaggle.com/c/job-salary-prediction/data

To download this dataset, create an account & agree to the terms of the competition, then scroll to the bottom right on the main page and click "Download All"

API Spec:
/predict/salary/<board_name>/<postingid> -> [ salaryAmount]

Test API Calls:
/predict/salary/cohere/e3cb621a-75b8-467c-803c-4325fb0c1301 -> Some Role $salary

Extra Bonus for Option 1: Send a working deployed server or web app


Option 2

Build a frontend that takes a posting URL and displays the contents of the job posting in a view that is well designed. The contents are then fed into an LLM API such as OpenAI which returns a predicted salary with an explanation of how it came to that conclusion. The LLM response should be streamed to the user.

The app should be deployed and have a URL that can be used to test it.

Extra Bonus for Option 2: Send a working chrome extension instead of a web app that shows the same information above when browsing a job posting


Summary

This challenge is designed to help us see where your strengths lie, and what role would be the best fit for you at Tempo!

What we want to see:
- What tools you use and how you use them
- Trade-offs: Time vs perfection
- If you get stuck - do you know the right question to ask. You can text me any time - 4163050720.
- Send us a runnable github repo or codebase (zip file)

