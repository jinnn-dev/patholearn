import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
export const SuperTokensWebJSConfig = {
  enableDebugLogs: true,
  appInfo: {
    appName: 'Patholearn AUth',
    apiDomain: import.meta.env.VITE_AUTH_API_URL,
    websiteDomain: import.meta.env.VITE_WEBSITE_URL
  },
  recipeList: [Session.init({ sessionTokenFrontendDomain: '.janeee.de' }), EmailPassword.init()]
};
