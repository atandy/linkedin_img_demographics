# LinkedIn Image Demographics

This code will login to your LinkedIn account and conduct a search for you based on your Person search criteria. It will then iterate through all pages of results and pull the name and image of each Person. From there, you can run each image URL through Clarifai's Demographics API and get the masculinity/feminity scores, in addition to guesses at the Person's "multicultural_appearance". 

In the end, you can slice the data by masc/fem scores and appearance, which enables you to see the breakdown of particular people based on your search. For example, you could search for "Senior Software Engineer at Google" and be able to perform the analysis to see the appearance and gender breakdown in that particular role.


## Getting Started

* Download the repo.
* Set up Clarifai API and get a key
* Set up envivironment variables: CLARIFAIAPI_KEY, LINKEDIN_USERNAME, LINKEDIN_PASSWORD, SQLALCHEMY_DATABASE_URI
* Then run: 
    ```python run.py; python face_demographics.py; python analysis.py```

### Prerequisites

What things you need to install the software and how to install them

```
Patience with my code; I wrote this very quickly. 
```

## Running the tests

Lol

## Deployment

Even more LOL.

## Built With

* [ClarifaiAPI](http://www.clarifai.com) - The image demographics API
* [Pandas](https://pandas.pydata.org/) - For the data things.

## Contributing

You can contribute. I don't know how that would work yet, but you can. 

## Versioning

I don't know.

## Authors

* **Alex Tandy** - *Initial work*


## License

You can't use this without asking me.

## Acknowledgments

* The missed connection who I was trying to find via LinkedIn.