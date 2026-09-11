// import { CognitoUserPool } from "amazon-cognito-identity-js";

// const poolData = {
//   UserPoolId: "us-east-1_xHpsCa1lT", 
//    ClientId: "70v19uvs74g5b9iqr1catnt92b",
// };

// export default new CognitoUserPool(poolData);




// src/services/auth.js

// Extract token from Cognito Hosted UI redirect
export function getTokenFromUrl() {
  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);
  return params.get("id_token"); // or "access_token" depending on your Cognito config
}

// Logout via Cognito Hosted UI
export function logout() {
  const domainPrefix = "leave-mgmt-auth"; // replace with your Cognito domain prefix
  const region = "us-east-1_xHpsCa1lT"; // replace with your AWS region
  const clientId = "70v19uvs74g5b9iqr1catnt92b"; // replace with your Cognito App Client ID
  const redirectUri = "http://localhost:5173/"; // or Amplify app URL

  window.location.href = `https://${domainPrefix}.auth.${region}.amazoncognito.com/logout?client_id=${clientId}&logout_uri=${redirectUri}`;
}
