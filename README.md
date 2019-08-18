# Gitlab-Image-Refresher
Polls Gitlab image registry for updates for images listed in config.json and updates containers and services
using these images. Developed for Ubuntu 18.04, other distributions or operated systems not tested.


<h2>Usage</h2>
<li>Configure config.json<sup>2</sup>, make sure config.json is in the same folder as main.py</li>

```json
{
"config": {
    "interval": <interval-seconds>
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