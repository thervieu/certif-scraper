# certif-scraper

https://www.examtopics.com/exams/amazon/aws-certified-developer-associate-dva-c02/view/1/


## How to 
Create a directory with whatever name you want.
<br>
Download the html pages on the examtopics website and copy them to the previously created directory.
<br>
Run `python3 get-questions.py DIR_NAME`. This should create a file named DIR_NAME.json that has all the questions of the given html files.

You will need to manually verify the answers using the community's answers. I could not manage to automate this section, sorry.

Once this is done you can copy the file to `my-app/public` directory in the https://github.com/thervieu/certif.thervieu.fr

Finally change the loaded file in the `my-app/src/App.js` with your copied file.

Run the app locally using ``npm run start``.

If everything is done correctly, you will have a exam-like application.
This was developped in two hours. Revisions will not happen often.