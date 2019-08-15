# Gitlab-Image-Refresher

# In active development, not usable yet.
Refresh Docker Images in running and stopped containers hosted in Gitlab private image registires.

Will use config.json to see what images to poll for updates. Looks at the revision id<sup>1</sup> of listed
images in the Gitlab Container Registry.

<h2>Usage</h2>
<li>Configure config.json<sup>2</sup></li>

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
<li>Run main.py</li>

<sup>1</sup> Hover tag in Gitlab Container Registry for full revision id.<br />
<sup>2</sup> To generate Gitlab private API token see: https://gitlab.com/profile/personal_access_tokens
Gitlab Image Refresher requires read_user, read_repository and read_registry rights to work.