import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
export const SuperTokensWebJSConfig = {
  appInfo: {
    appName: 'Patholearn Auth',
    apiDomain: import.meta.env.VITE_AUTH_API_URL,
    websiteDomain: import.meta.env.VITE_WEBSITE_URL
  },
  recipeList: [
    Session.init({
      sessionTokenFrontendDomain: '.' + import.meta.env.VITE_AUTH_FRONTEND_DOMAIN,
      sessionTokenBackendDomain: '.' + import.meta.env.VITE_AUTH_FRONTEND_DOMAIN
    }),
    EmailPassword.init()
  ]
};
