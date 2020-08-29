# RICE CROP MONITORING USING SENTINEL-1
We develop this tool to automate the Mekong Delta rice mapping. We hope our data will help to rice monitoring and yield prediction. The map results will be published freely on the internet. You can get the map service via our API. 

Contact us: https://www.facebook.com/hcm.stac


### Create virtual environment
    python -m venv venv

### Activate virtual environment (windows)
    venv\Scripts\activate.bat


### Create bat file
    CALL venv\Scripts\activate
    your_python_file.py
    cmd /k
    
### Install packages
    pip install <package>
    
### Save all the packages in the file
    pip freeze > requirements.txt
   
### Install project dependencies
    pip install -r requirements.txt
 
### Show information about packages from the requiements.txt
    pip show <packagename>
    
    
### Check GDAL version
    import osgeo.gdal
    print(osgeo.gdal.__version__)

    
    
    
## License - ISC

Copyright (c) 2020 - STAC team.

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
