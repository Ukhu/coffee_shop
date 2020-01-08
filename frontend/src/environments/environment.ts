export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop-ukhu', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'a0upBPwnHRrvJSpT5AHsaIW3eWmqhNRN', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
