# SASMEX RSS 

The website of SASMEX's RSS feed. The website consists of a map where the 
latest CAP alert can be viewed and downloaded, as well as a table where the
history of CAP files can be viewed and downloaded if necessary.


## Developing

To start the development sever:

```shell
git clone https://github.com/Daniel-Ibarrola/Sasmex-RSS.git
cd Sasmex-RSS
npm install
npm run dev
```

Run the tests (in another terminal):

```shell
npm run test
```

## Building

Build the website for production:

```shell
npm run build
npm run preview
```
The first command will create a dist folder with an index.html file that 
can be used by a webserver such as nginx as the root of the site.
