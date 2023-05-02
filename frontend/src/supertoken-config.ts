import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
export const SuperTokensWebJSConfig = {
  appInfo: {
    appName: 'Patholearn AUth',
    apiDomain: import.meta.env.VITE_AUTH_API_URL
  },
  recipeList: [Session.init(), EmailPassword.init()]
};
