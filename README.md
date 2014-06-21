Set up a service so that as soon as the file /var/log/sizes.log  
changes, the median response sizes for each response code are  
available via HTTP over port 8888 on localhost. The log file may  
be assumed to be in the apache/NCSA common log format. The service  
should return a JSON encoded response with the computed median  
size in the 'median_size' key. The response code for which the  
median size is to be returned should be expected as the only item  
in the path of the request URL  

For example, requesting  

        http://localhost:8888/200  

should return the median response size for the 200 response code,  
encoded as a JSON object, in a 'median_size' key, for example:  

        {"median_size": 4098}  

Some sample data is already available in /var/log/sizes.log  

