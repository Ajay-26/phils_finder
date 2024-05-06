# Phil's Finder - Booth Mini Hackathon 2024

## Deployment on Heroku

```
$ heroku create mini-hack-2024-phils-finder
$ git push heroku master # deploy code to heroku
$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
```