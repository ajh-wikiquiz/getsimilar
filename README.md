# getsimilar
Returns words similar to the text in descending order of similarity.

This is intended to be deployed as a web service.  
Try it out here:  
    - GET https://getimportant.herokuapp.com/similar?text=game  
    - GET https://getimportant.herokuapp.com/similar/game  
    - https://getimportant.herokuapp.com/graphql  


### Example input
```
game
```


### Example output
```
{
    "data": {
        "similar": [
            {
                "text": "gameshow",
                "similarity": 0.9542961120605469
            },
            {
                "text": "minigame",
                "similarity": 0.9395730495452881
            },
            ...
        ]
    },
}
```
