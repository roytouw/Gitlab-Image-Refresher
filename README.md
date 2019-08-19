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
<li>Configure config.json<sup>2</sup>, make sure config.json is in the same folder as main.py</li>

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
<li>Install Requirements.txt</li>
<li>Run main.py with sudo rights.<sup>3</sup></li>

<sup>1</sup> Hover tag in Gitlab Container Registry for full revision id.<br />
<sup>2</sup> To generate Gitlab private API token see: https://gitlab.com/profile/personal_access_tokens
Gitlab Image Refresher requires read_user, read_repository and read_registry rights to work.<br />
<sup>3</sup>Docker SDK requires sudo rights to interact with Docker daemon.
