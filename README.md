### Dependencies:
* Flask

### To use the API:
Say your message is "May the force be with you". URL encode your input, and send a GET request like the following:
http://koalatcontent.com:8000/disfigure?phrase=May+the+force+be+with+you

That should get a response like:
{
  "phrase": "mAY ThE ForcE be WITh yoU"
}
