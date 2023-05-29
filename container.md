# MongoDB in a container

In this guide it will be describe how to use an instance of MongoDB inside a
container together with the `qibodb` client (i.e. essentially how to use it
with `pymongo` package).

`podman` will be used to manage the container. Any other equivalent manager can
be used in its place (e.g. `docker`, that is CLI-compatible with `podman`, so
it is only needed to change the base command).

## Install and create DB

### Pull the official image

```sh
podman pull docker://mongo

# and check that the image has been correctly downloaded
podman images
```

### Instantiate the container

```sh
# make sure the external directory exists
mkdir data
# and move ownership to a container user
podman unshare chown 1000:1000 $(realpath data)

# create the container
podman run -dt --name qibodb -p 9160:27017 -v $(realpath data):/data/db:Z,U docker.io/library/mongo:latest
```

https://www.redhat.com/sysadmin/debug-rootless-podman-mounted-volumes

### Jump into the database

Mongo has a management shell, named `mongosh`, to enter it in the container just
run:

```sh
podman exec -it qibodb mongosh
```

## Acknowledgments

Partially inspired by https://mehmetozanguven.com/run-mongodb-with-podman/
