# Test Technique Unyc

## Preamble

The objective of this test is to develop a Django application respecting the following objectives:
- Use Django and Django Rest Framework (you can use the latest versions)
- Code in Python 3
- Use Django and DRF best practices
- Code as few lines as possible

This will allow us to assess your level of understanding of a specification, your ability to read and interpret the documentation, and the rigor and quality of your code. Of course, your level of experience on Django/DRF will be taken into account!

There is no single solution or *right* answer, your ability to find solutions and interpret the instructions is part of the exercise.

The use of git and github/bitbucket/gitlab is mandatory. When you are done you will need:
- Create an exit
- Put your code in a branch attached to the issue
- Create a merge request and send it to us in order to proceed with the code review and that we can put our comments on it.

*Merci de respecter la confidentialité de ce test et de ne pas le diffuser*.

## Instructions

The goal is to develop a Restful API used by a bar.

This bar references several types of beer. It has several counters which each have their own stock.

Customers (anonymous users) can order and staff (authenticated users) can manage SKUs and stock.

### The references

The `/api/references/` endpoint allows you to list beer references (whether they are in stock or not).

```
[
    {
        "pk": 1,
        "ref": "leffeblonde",
        "name": "Leffe blonde",
        "description": "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne présente plus !",
        "availability": "available"
    },
    {
        "pk": 2,
        "ref": "brewdogipa",
        "name": "Brewdog Punk IPA",
        "description": "La Punk IPA est une bière écossaise s'inspirant des tendances américaines en matière de brassage et du choix des houblons.",
        "availability": "outofstock"
    },
    {
        "pk": 3,
        "ref": "fullerindiapale",
        "name": "Fuller's India Pale Ale",
        "description": "Brassée pour l'export, la Fuller's India Pale Ale est la vitrine du savoir faire bien « british » de cette brasserie historique. ",
        "availability": "available"
    }
]
```

Clients can access this endpoint.
Only the staff can modify the references (any deletion should automatically delete the stocks described below).

The availability field is not stored in the database and must be defined dynamically.

You need to be able to sort, search and paginate the results.

*Optional - Add GET parameters for:*

- *specify a counter and therefore have different availability results since each bar has its own stock*
- *specify that you only want to see the references that are in stock*

### Bar counters

The `/api/bars/` endpoint returns the list of counters present in the bar (minimum 2).

```
[
    {
        "pk" : 1,
        "name": "1er étage"
    },
    {
        "pk" : 2,
        "name": "2ème étage"
    }
]
```

Clients have the right to access this endpoint.
Only staff can add, modify or delete entries via this endpoint (consider implementing POST and PUT).

You need to be able to sort and paginate the results.

### The stocks

It is advisable to model a *stock* which makes it possible to know the number of reference available for each counter.

The `/api/stocks/` endpoint allows you to list the references available in a counter's stock and their quantities.

```
[
    {
        "reference": 1,
        "bar": 1,
        "stock": 10
    },
    {
        "reference": 2,
        "bar": 1,
        "stock": 8
    },
    {
        "reference": 2,
        "bar": 2,
        "stock": 5
    },
    {
        "reference": 3,
        "bar": 2,
        "stock": 1
    }
]
```

Only staff has the right to access this endpoint which is read-only.

You need to be able to sort, filter and paginate the results.

### Classify counters

It is necessary to provide staff with information about the counters.

The `/api/statistics/` endpoint allows you to list bars according to their characteristics.

The expected characteristics are:
- all_stocks
- miss_at_least_one

```
[
    "all_stocks": {
        "description": "Liste des comptoirs qui ont toutes les références en stock",
        "bars": [1]
    },
    "miss_at_least_one": {
        "description": "Liste des comptoirs qui ont au moins une référence épuisée",
        "bars": [2]
    }
]
```

Only staff have the right to access this endpoint.

### The orders

The `/api/orders/` endpoint allows you to order beers at a given counter by making a `POST` with the following payload:

```
{
    "bar": 1,
    "items": [
        {
            "reference": 1,
            "count": 2
        },
        {
            "reference": 2,
            "count": 1
        },
        {
            "reference": 3,
            "count": 1
        }
    ]
}
```

All orders are final.

An entry in the `Orders` table must be created and `n` entries in the `OrderItems` table must be created.

Each creation in the `OrderItems` table should decrease the counter stock count for the reference. The code updating the stock must not be in the view, nor in the serializer, nor in the model. Django provides an elegant way to react to database object creation. If the stock drops below 2, a message should be displayed in the *logs*.

Only customers can order.

The result of this call must be a serialized order in the following form:
```
{
    "pk": 1,
    "bar": 1,
    "items": [
        {
            "reference": 1,
            "count": 2
        },
        {
            "reference": 2,
            "count": 1
        },
        {
            "reference": 3,
            "count": 1
        }
    ]
}
```

Only staff can list orders.

## To finish
Rights must be managed in groups.

To make it possible to use this application, you must add fixtures that can be loaded to bootstrap the application (users, bars, references, stocks).

Of course, tests using the fixtures are expected to validate the operation of the application.

Do not hesitate to integrate into the code all types of bonuses that could allow us to clearly understand your level (Dockerfile, kubernetes deployment, packaging, documentation..., the possibilities are endless ;-) ).

Bon test !
