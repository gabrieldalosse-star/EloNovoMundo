import {initializeApp} from 'firebase/app';
import {getAuth,GoogleAuthProvider,signInWithPopup,signInWithEmailAndPassword,sendPasswordResetEmail,sendEmailVerification,signOut} from 'firebase/auth';
import {getFunctions,httpsCallable} from 'firebase/functions';
const e=import.meta.env;
export const configured=!!(e.VITE_FIREBASE_API_KEY&&e.VITE_FIREBASE_PROJECT_ID&&e.VITE_FIREBASE_AUTH_DOMAIN&&e.VITE_FIREBASE_APP_ID);
const app=configured?initializeApp({apiKey:e.VITE_FIREBASE_API_KEY,authDomain:e.VITE_FIREBASE_AUTH_DOMAIN,projectId:e.VITE_FIREBASE_PROJECT_ID,appId:e.VITE_FIREBASE_APP_ID}):null;
export const auth=app?getAuth(app):null;
const functions=app?getFunctions(app,e.VITE_FUNCTIONS_REGION||'southamerica-east1'):null;
export async function call<T=any>(name:string,data?:unknown):Promise<T>{if(!functions)throw Error('Firebase ainda não configurado.');return (await httpsCallable<unknown,T>(functions,name)(data)).data;}
export async function loginGoogle(){if(!auth)return;const provider=new GoogleAuthProvider();provider.setCustomParameters({prompt:'select_account'});await signInWithPopup(auth,provider)}
export async function loginEmail(email:string,password:string){if(auth)await signInWithEmailAndPassword(auth,email,password)}
export async function resetPassword(email:string){if(auth)await sendPasswordResetEmail(auth,email)}
export async function verifyEmail(){if(auth?.currentUser)await sendEmailVerification(auth.currentUser)}
export async function logout(){if(auth)await signOut(auth);else location.reload()}
