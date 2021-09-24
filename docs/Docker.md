# Docker

[Download](https://github.com/Lotus-King-Research/Padma-Backend/archive/master.zip) the package and being in the same directory as the package:

```
sudo docker build .
IMAGE_ID=$(sudo docker image ls | head -2 | tail -1 | tr -s ' ' | cut -d ' ' -f3)
sudo docker run -p 5000:5000 $IMAGE_ID
```

You will now have Padma running locally and accessible with browser from http://0.0.0.0:5000. 

**NOTE:** Docker runs the production gunicorn server. For preferred development environment, see [here](Development.md).
