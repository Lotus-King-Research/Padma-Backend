# Application Structure

The package [/app](https://github.com/Lotus-King-Research/Padma-Backend/tree/master/app) is structured as follows: 

- `pipelines` contains pipelines for each views where the data is produced
- `static` contains static files, such as images and javascript
- `templates` contains all the html templates that are rendered in the views
- `utils` contains various utilities that do not readily fit to other directories
- `views` contains the views that lead to rendering of the html in the browser
- `routes.py` contains all the routing information