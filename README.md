# Plugin Framework

## Setup

Currently, only Ubuntu and Fedora are supported.

1. Download Krita. Use the Appimage version, not whatever is provided by package managers.
2. Install python. It is recommended to match whatever Krita uses internally, but anything 3.5+ should be fine.
3. Install this repo. Clone it, and then run:
```
python3 -m pip install path/to/folder 
```
This will automatically install dependencies.
4. Download the `client` repository, and copy it to Krita's plugin folder. On most systems, that should be `/home/hybrid/.local/share/krita/pykrita/client/`

## Running

1. Start the server, with `python3 -m sync.server`.
2. Start krita.
3. Open a sample doc. 

To run the provided `demo` action, do the following:
1. Open a new doc.
2. Create three layers: `content`, `style`, and `output`. Place your content and style images in the corrosponding layers.
3. Run the `demo` action at `scripts->actions->demo`.
4. Watch as the magic happens


## Requests

All requests follow the general structure:

```json
{
  "request": "SomethingSpecific",
  "data":{}
}
````

The data parameter depends on the request type.
Pickle is used to efficiently encode data for transmission.
