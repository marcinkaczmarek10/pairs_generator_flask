
# Random pairs generator
![GitHub language count](https://img.shields.io/github/languages/count/marcinkaczmarek10/pairs_generator_flask) ![Website](https://img.shields.io/website?url=https%3A%2F%2Frandom-pairs-generator.herokuapp.com) [![Tests](https://github.com/marcinkaczmarek10/pairs_generator_flask/actions/workflows/python-app.yml/badge.svg)](https://github.com/marcinkaczmarek10/pairs_generator_flask/actions/workflows/python-app.yml) ![Codecov](https://img.shields.io/codecov/c/github/marcinkaczmarek10/pairs_generator_flask)

This is random pairs generator, web app based on flask framework. 
Purpose of this project is to generate random pairs, based on pool given by any user.
Then user can send email to a picked person. Website features authentication using Flask-Login.
There is also an option using API, it has HTTP basic auth. To acces other endpoints you need to attach token inside request header. Token is returned after succesful authentication.

The idea for this project came from christmas lottery, when a group of people was about to decide
who would buy a present for whom. This is the most optimum way to use this project, but there could be more use cases. 



## Demo

https://random-pairs-generator.herokuapp.com



## Features

- Authentication
- Reset password via email link
- Adding user's draw pool
- Generating random pairs from given pool
- Sending mails to selected pairs with user's title and body


## API Reference

#### Get authentication token

```http
  GET /api/login
```
This endpoint requires basic HTTP authentication, when succeded returns auth token.

### All of belowed endpoints require these headers:

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `api_token`      | `string` | **Required**. Token is generated at /api/login endpoint.|
| `Content-Type: aplication/json`      | `string` | **Required**. |

### Get results

```http
  GET /api/results
```
This endpoint returns all of user's results.

### Generate random pairs
```http
  POST /api/generate-pairs
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `person_name`| `string` | **Required**. |
| `person_email`| `string` | **Required**. |

 Generate random pairs from a given pool. Endpoint accept json format and it is required that pool comes in array.

### Send mails
```http
  POST /api/send-mail
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `draw_count`| `int` | **Required**.|
| `title`| `string` | **Required**. |
| `body`| `string` | **Required**. |

Sending emails to pairs in selected draw. 

### Delete result
```http
  DELETE /api/delete-results
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `draw_count`| `int` | **Required**.|

Delete result for a given draw. 



