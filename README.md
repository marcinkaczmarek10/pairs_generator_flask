
# Random pairs generator

This is random pairs generator, web app based on flask framework. 
Purpose of this project is to generate random pairs, based on pool given by any user.
Then user can send email to picked person. Website features authentication using Flask-Login.
There is also an option using API, it is using HTTP basic auth. To acces other endpoints you need attach token inside request header. Token is returned afeter succesful authentication.

The idea for this project came from christmas lottery, when group of people were about to decide
who would buy a present for whom. This is the most optimum way to use this project, but there could be more use cases. 



## Demo

https://random-pairs-generator.herokuapp.com

* This website is not responsive yet.


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
This endpoint return all of user's results. It requires two headers: api_token and Content-Type: aplication/json

### Generate random pairs
```http
  POST /api/generate-pairs
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `person_name`| `string` | **Required**. |
| `person_email`| `string` | **Required**. |

 Generate random pairs from given pool. Endpoint accept json format and it is required that pool comes in array.

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

Delete results for given draw. 



