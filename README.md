# IMDB SEARCH


This project is can be used for two level access access(admin and user) and for search on the given data


# Features!

  - User can be login with admin access and user access
  - Admin can add movies(single or bulk) and user can view movies.
  - This project use two types of searches search on database and serch on elasticsearch
  - Admin can also view the analytics of the data inside the system

### Dependencies:
```sh 
Python 2.7
Flask
Peewee (ORM)
```


### Usages:
 - `Master user` is pre-initialized into the database, once the DB is initialized [link](http://google.com).
 - `Master user` can add multiple `ADMINS`
     ``` sh
     username: masterfynd
     password: masterpassword
     ```
 - `ADMIN` can add/delete/edit movies. Bulk upload api is also available for `ADMIN` user.
 - `Normal user` aka `customers` will have access to only search the movies.



## Algorithm
 
 - Whenever user register into the app the data is stored into the database with password being in `hash`
 - Now when the user logs in the hash of the password is converted into hash and will be matched with the hashed passowrd stored in database
 - This User can do both types of search database search and es search
 - If the user is admin it can add single movie or do a bulk add.
 
## Scalabiity

### Phase 1
- Static asset to be put on CDN
- To be hosted on Apache http or nginx web server

### Phase 2
- Database Optimization 
  - Indexing
  - Redusing Query cache size according to usecase
- Code level Optimization
- Caching logged user data to minimize database calls

### Phase 3
- Vertical Scaling
  - SSD insted of HDD
  - Increasing RAM, cores and CPU
  (vertical scaling to be done as per monitary cost optimization)
- Horizontal Scaling 
  - Put loadbalacer and multiple webserver instances.  





