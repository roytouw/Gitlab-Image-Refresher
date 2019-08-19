[![](https://images.microbadger.com/badges/version/esv7/gitlab-image-refresher.svg)](https://microbadger.com/images/esv7/gitlab-image-refresher "Get your own version badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/esv7/gitlab-image-refresher.svg)](https://microbadger.com/images/esv7/gitlab-image-refresher "Get your own image badge on microbadger.com")
# Gitlab-Image-Refresher
Polls Gitlab image registry for updates for images listed in config.json and updates containers and services
using these images. Developed for Ubuntu 18.04, other distributions or operating systems not tested.

<h4> Images </h4>
Images listed in config.json will be replaced by the new version upon detection of the new version.

<h4> Services </h4>
Services that run outdated images will be cleaned up by removing all stopped containers beloning to
the service, after which the service will be force-updated to run the newly pulled image.

<h4> Running Containers </h4>
Running containers belonging to a service will be updated by force-updating the containing service.
Containers not belonging to any service will be stopped and removed. For each stopped container a new one wil be ran with the updated image.

<h4> Stopped Containers </h4>
Stopped containers will be treated the same as running containers.

<h4> No Running or Stopped Containers Found </h4>
When no running or stopped containers with the image as listed in the config.json are found, upon detection of a new version of the image
a single container with this image will be ran. 

<h2>Usage</h2>
<li>Configure config.json<sup>1</sup></li>
Create a config.json file and replace the placeholders with your data.

```json
{
"config": {
    "interval": <interval-seconds>,
    "login": "<gitlab-login>",
    "password": "<gitlab-password>"
  },
  "registries": [
    {
      "user": "<user-name>",
      "project": "<project-name>",
      "apiToken": "<api-token>",
      "images": [
        {
          "tag": "<tag>"
        }
      ]
    },
    {
      "user": "<user-name>",
      "project": "<project-name>",
      "apiToken": "<api-token>",
      "images": [
        {
          "tag": "<tag>"
        },
        {
          "tag": "<tag2>"
        }
      ]
    }
  ]
}
```
<li>Make docker-compose.yml<sup>2</sup></li>
Create a docker-compose.yml file and replace the placeholders with your files.

```yml
version: '3.2'
services:
  gitlab-image-refresher:
    image: gitlab-image:refresher:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - <path-to-config.json>:/app/config.json
      - <path-to-cache.json>:/app/cache.json
      - <path-to-log.txt>:/app/cache.json
```

<li>Deploy Service</li>
Deploy service e.g. docker stack deploy -c docker-compose.yml refresher

<br /><br />

<sup>1</sup> To generate Gitlab private API token see: https://gitlab.com/profile/personal_access_tokens
Gitlab Image Refresher requires api rights to work.<br />
<sup>2</sup>cache.json and log.txt are optional for perseverance, use touch to create empty file. 
